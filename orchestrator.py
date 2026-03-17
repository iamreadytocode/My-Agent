import os
from typing import TypedDict, Annotated, Sequence, Literal
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Import your brand new LangGraph Agent Nodes
from agents.GymAgent import gym_node
from agents.MealAgent import meal_node
from agents.HealthAgent import health_node
from agents.NewsAgent import news_node
from agents.CalendarAgent import calendar_node
from agents.EmailAgent import email_node

# 2. Define Viki's Memory State
class VikiState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    next_agent: str

# 3. Define the routing schema for the Supervisor
class RouteDefinition(BaseModel):
    next_agent: Literal["gym", "meal", "health", "news", "calendar", "email", "FINISH"] = Field(
        description="The agent to route to, or FINISH if a simple conversational reply is enough."
    )

# 4. Build the Supervisor (The Brain)
def supervisor_node(state: VikiState) -> dict:
    """Reads the user input and decides which agent should handle it."""
    # We use a fast, cheap model for routing
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", api_key=os.getenv("GEMINI_API_KEY"))
    
    # Force the LLM to output ONLY one of our specific route choices
    router_llm = llm.with_structured_output(RouteDefinition)
    
    system_prompt = """
    You are the Supervisor for Viki, a personal assistant. 
    Look at the user's latest message and decide which specialized agent should handle it.
    - 'gym': Workouts, fitness routines, logging exercise.
    - 'meal': Food analysis, macros, calorie counting, logging meals.
    - 'health': Symptoms, medical questions, health advice.
    - 'news': Current events, weather, headlines, general lookups.
    - 'calendar': Scheduling, checking dates, making events.
    - 'email': Checking inbox, sending messages.
    - 'FINISH': If it's a simple greeting or casual chat that needs no tools.
    - 'If the user says something general like "What's up?" or "Goodbye?", respond with FINISH and a friendly message.
    """
    
    # Combine prompt with the user's messages
    messages = [{"role": "system", "content": system_prompt}] + state["messages"]
    
    # Get the decision
    decision = router_llm.invoke(messages)
    
    return {"next_agent": decision.next_agent}

# 5. Build the LangGraph State Machine
workflow = StateGraph(VikiState)

# Add all the "rooms" (Nodes) to the graph
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("gym", gym_node)
workflow.add_node("meal", meal_node)
workflow.add_node("health", health_node)
workflow.add_node("news", news_node)
workflow.add_node("calendar", calendar_node)
workflow.add_node("email", email_node)

# Draw the entry point
workflow.add_edge(START, "supervisor")

# Set up the conditional routing doors
workflow.add_conditional_edges(
    "supervisor",
    lambda state: state["next_agent"], # Look at the string the supervisor output
    {
        "gym": "gym",
        "meal": "meal",
        "health": "health",
        "news": "news",
        "calendar": "calendar",
        "email": "email",
        "FINISH": END # If no agent is needed, exit graph
    }
)

# After any agent does its job, the workflow ends
workflow.add_edge("gym", END)
workflow.add_edge("meal", END)
workflow.add_edge("health", END)
workflow.add_edge("news", END)
workflow.add_edge("calendar", END)
workflow.add_edge("email", END)

# Compile the final system
viki_app = workflow.compile()

# 6. The Application Wrapper (What you pasted earlier!)
# Add this global variable right above the function
chat_memory = []

def process_user_input(user_text: str) -> str:
    global chat_memory
    
    # 1. Add the user's new message to the memory log
    chat_memory.append(("user", user_text))
    
    # 2. Pass the ENTIRE memory to the graph, not just the single sentence
    initial_state = {
        "messages": chat_memory,
        "next_agent": "supervisor"
    }
    
    # Run the graph
    result = viki_app.invoke(initial_state)
    
    # Extract the raw content from the final message
    raw_content = result["messages"][-1].content
    
    # Clean the output
    if isinstance(raw_content, list):
        final_response = "\n".join([item["text"] for item in raw_content if "text" in item])
    else:
        final_response = raw_content
        
    # 3. Save Viki's response back to memory so she remembers it for next time!
    chat_memory.append(("assistant", final_response))
    
    return final_response