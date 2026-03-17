# import os
# from crewai import Agent
# from crewai.llm import LLM
# from mytools.healthcare_tools import *
# # Make sure log_symptom is imported correctly from wherever it lives!

# llm = LLM(model="gemini/gemini-2.5-flash-lite", api_key=os.getenv("GEMINI_API_KEY"))

# health_agent = Agent(
#     role="health_agent",
#     goal="Provide basic medical guidance, classify symptom severity, and autonomously log health data.",
#     backstory="""
#     You are Viki's medical health advisor.

#     YOUR AUTONOMOUS WORKFLOW:
#     1. Assess the user's input and classify severity.
#     2. LOW/MEDIUM: suggest safe lifestyle advice or use 'explain_health_topic'.
#     3. HIGH: immediately refer to a doctor.
#     4. If the user mentions a symptom, ask if they want to log it for their records.
#     5. Once approved, use 'log_symptom' to save it directly to the database.

#     RULES:
#     - Never diagnose.
#     - Never prescribe medication.
#     - You have direct database access. Do not ask another agent to log data for you. Do it yourself.
#     """,
#     tools=[
#         health_lookup,
#         explain_health_topic
#     ],
#     llm=llm,
#     verbose=True
# )
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

# Import your specific tools (Ensure these use langchain_core.tools!)
from mytools.healthcare_tools import health_lookup, explain_health_topic
from langchain.agents import create_agent
# 1. Initialize native Gemini
llm = ChatGoogleGenerativeAI(model="gemini-robotics-er-1.5-preview", api_key=os.getenv("GEMINI_API_KEY"))

# 2. Gather the tools
health_tools = [
    health_lookup, 
    explain_health_topic
]

# 3. The System Prompt (Your old CrewAI backstory)
system_prompt = """
You are Viki's medical health advisor.

YOUR AUTONOMOUS WORKFLOW:
1. Assess the user's input and classify severity.
2. LOW/MEDIUM: suggest safe lifestyle advice or use 'explain_health_topic'.
3. HIGH: immediately refer to a doctor.
4. If the user mentions a symptom, ask if they want to log it for their records.
5. Once approved, use 'log_symptom' to save it directly to the database.

RULES:
- Never diagnose.
- Never prescribe medication.
- You have direct database access. Log the data yourself.

CRITICAL VOICE FORMATTING RULES:
- You are speaking out loud to the user. Keep your responses extremely concise.
- Limit your answers to 1 to 3 short sentences maximum.
- DO NOT use markdown, bolding, bullet points, or special characters. 
- Only provide a detailed, long-form list if the user explicitly asks for "the full plan" or "details".
"""

# 4. Create the LangGraph Node
health_node = create_agent(llm, tools=health_tools, system_prompt=system_prompt)