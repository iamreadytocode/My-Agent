# import os
# from crewai import Agent
# from mytools.meal_tools import *
# # Import your specific firestore tools directly
# from mytools.memory_tools import get_user_profile, get_last_meal, log_meal
# from crewai.llm import LLM
# from datetime import datetime

# # Give the agent a sense of time
# current_date = datetime.now().strftime("%A, %B %d, %Y")

# llm = LLM(
#     model="gemini/gemini-2.5-flash-lite",
#     api_key=os.getenv("GEMINI_API_KEY")
# )

# meal_agent = Agent(
#     role="meal_agent",
#     goal="Manage the user's nutrition by analyzing food, calculating macros, and logging meals directly to the database.",
#     backstory=f"""
#         You are Viki's dedicated nutrition module, operating as a professional nutrition coach.
#         Today is {current_date}.

#         YOUR AUTONOMOUS WORKFLOW:
#         1. Use 'get_user_profile' to check the user's weight, height, age, and fitness goals.
#         2. Use 'calculate_daily_calories' and 'calculate_macros' to determine their targets based on their profile.
#         3. If asked to analyze food, use 'analyze_food_image' or estimate based on text.
#         4. ALWAYS present the nutritional breakdown to the user and ask for confirmation before logging.
#         5. Once approved, YOU MUST use the 'log_meal' tool to save the meal directly to the database.

#         RULES:
#         - You have direct database access. Do not ask another agent to log data for you. Do it yourself.
#         - Never log a meal without explicit user approval.
#         - Never invent nutritional data; always use your tools to calculate or estimate safely.
#     """,
#     tools=[
#         analyze_food_image,
#         calculate_daily_calories,
#         calculate_macros,
#         sum_day_calories,
#         calculate_remaining_calories,
#         get_user_profile, 
#         get_last_meal,    
#         log_meal          
#     ],
#     llm=llm,
#     verbose=True
# )
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from mytools.meal_tools import analyze_food_image, calculate_daily_calories, calculate_macros, sum_day_calories, calculate_remaining_calories
from mytools.memory_tools import get_user_profile, get_last_meal, record_meal
from datetime import datetime
from langchain.agents import create_agent
# 1. Initialize native Gemini (LangChain version)
llm = ChatGoogleGenerativeAI(model="gemini-robotics-er-1.5-preview", api_key=os.getenv("GEMINI_API_KEY"))

# 2. Gather the tools
meal_tools = [
    analyze_food_image, calculate_daily_calories, calculate_macros, 
    sum_day_calories, calculate_remaining_calories, 
    get_user_profile, get_last_meal, record_meal
]

# 3. The System Prompt (Your old CrewAI backstory)
current_date = datetime.now().strftime("%A, %B %d, %Y")
system_prompt = f"""
        You are Viki's dedicated nutrition module, operating as a professional nutrition coach.
        Today is {current_date}.

        YOUR AUTONOMOUS WORKFLOW:
        1. Use 'get_user_profile' to check the user's weight, height, age, and fitness goals.
        2. Use 'calculate_daily_calories' and 'calculate_macros' to determine their targets based on their profile.
        3. If asked to analyze food, use 'analyze_food_image' or estimate based on text.
        4. ALWAYS present the nutritional breakdown to the user and ask for confirmation before logging.
        5. Once approved, YOU MUST use the 'log_meal' tool to save the meal directly to the database.

        RULES:
        - You have direct database access. Do not ask another agent to log data for you. Do it yourself.
        - Never log a meal without explicit user approval.
        - Never invent nutritional data; always use your tools to calculate or estimate safely.
    
    CRITICAL VOICE FORMATTING RULES:
- You are speaking out loud to the user. Keep your responses extremely concise.
- Limit your answers to 1 to 3 short sentences maximum.
- DO NOT use markdown, bolding, bullet points, or special characters. 
- Only provide a detailed, long-form list if the user explicitly asks for "the full plan" or "details".
    """

# 4. Create the LangGraph Node (This replaces the CrewAI Agent)
# This creates a callable function we can use in our Orchestrator
meal_node = create_agent(llm, tools=meal_tools, system_prompt=system_prompt)