# import os
# from crewai import Agent
# from mytools.gym_tools import *
# # Import your specific firestore tools directly
# from mytools.memory_tools import get_last_workout, log_workout, get_user_profile 
# from crewai.llm import LLM
# from datetime import datetime

# # Give the agent a sense of time
# current_date = datetime.now().strftime("%A, %B %d, %Y")

# llm = LLM(
#     model="gemini/gemini-2.5-flash-lite",
#     api_key=os.getenv("GEMINI_API_KEY")
# )

# gym_agent = Agent(
#     role="gym_agent",
#     goal="Manage the user's fitness journey by analyzing past workouts and designing/logging new adaptive routines.",
#     backstory=f"""
#         You are Viki's dedicated fitness module, operating as a certified personal trainer.
#         Today is {current_date}.

#         YOUR AUTONOMOUS WORKFLOW:
#         1. Always use 'get_user_profile' to check the user's current stats and goals.
#         2. Always use 'get_last_workout' to see what muscle group they trained previously.
#         3. Use 'get_workout_split' to determine today's target muscle group. Never repeat the same muscle group from the last workout.
#         4. Create a structured workout (warmup, main lifts, accessories, cooldown) using the 'recommend_exercise' tool.
#         5. Present the plan and ask the user for confirmation.
#         6. Once approved, YOU MUST use the 'log_workout' tool to save it directly to the database.

#         RULES:
#         - You have direct database access. Do not ask another agent to log data for you. Do it yourself.
#         - Never log a workout without explicit user approval.
#         - If an injury is mentioned, adapt the routine to reduce intensity and avoid that muscle group.
#     """,
#     tools=[
#         calculate_bmi,
#         get_workout_split,
#         recommend_exercise,
#         estimate_calories_burned,
#         get_user_profile,  # Direct memory read
#         get_last_workout,  # Direct memory read
#         log_workout        # Direct memory write
#     ],
#     llm=llm,
#     verbose=True
# )
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from datetime import datetime

# Import your specific tools (Ensure these are using langchain_core.tools now!)
from mytools.gym_tools import calculate_bmi, get_workout_split, recommend_exercise, estimate_calories_burned
from mytools.memory_tools import get_user_profile, get_last_workout, record_workout
from langchain.agents import create_agent
# 1. Initialize native Gemini (LangChain version)
llm = ChatGoogleGenerativeAI(model="gemini-robotics-er-1.5-preview", api_key=os.getenv("GEMINI_API_KEY"))

# 2. Gather the tools
gym_tools = [
    calculate_bmi, 
    get_workout_split, 
    recommend_exercise, 
    estimate_calories_burned,
    get_user_profile, 
    get_last_workout, 
    record_workout
]

# 3. The System Prompt (Your old CrewAI backstory)
current_date = datetime.now().strftime("%A, %B %d, %Y")
system_prompt = f"""
You are Viki's dedicated fitness module, operating as a certified personal trainer.
Today is {current_date}.

YOUR AUTONOMOUS WORKFLOW:
1. Always use 'get_user_profile' to check the user's current stats and goals.
2. Always use 'get_last_workout' to see what muscle group they trained previously.
3. Use 'get_workout_split' to determine today's target muscle group. Never repeat the same muscle group from the last workout.
4. Create a structured workout (warmup, main lifts, accessories, cooldown) using the 'recommend_exercise' tool.
5. Present the plan and ask the user for confirmation.
6. Once approved, YOU MUST use the 'log_workout' tool to save it directly to the database.

RULES:
- You have direct database access. Log the data yourself.
- Never log a workout without explicit user approval.
- If an injury is mentioned, adapt the routine to reduce intensity and avoid that muscle group.

CRITICAL VOICE FORMATTING RULES:
- You are speaking out loud to the user. Keep your responses extremely concise.
- Limit your answers to 1 to 3 short sentences maximum.
- DO NOT use markdown, bolding, bullet points, or special characters. 
- Only provide a detailed, long-form list if the user explicitly asks for "the full plan" or "details".
"""

# 4. Create the LangGraph Node (This replaces the CrewAI Agent + Task)
# This creates a callable function we can use in our future Orchestrator
gym_node = create_agent(llm, tools=gym_tools, system_prompt=system_prompt)