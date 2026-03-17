# from crewai import Agent
# from mytools.calendar_tools import *
# from mytools.notification_tools import *
# from crewai.llm import LLM
# import os
# import datetime

# llm = LLM(
#     model="gemini/gemini-robotics-er-1.5-preview", 
#     api_key=os.getenv("GEMINI_API_KEY")
# )

# # Get current time context for the agent
# current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# calendar_agent = Agent(
#     role="calendar_agent",
#     goal="Manage user's time, tasks and reminders",
#     backstory=f"""
#     You are a scheduling assistant. 
#     The current date and time is {current_time}. Keep this in mind for all scheduling relative to 'today' or 'tomorrow'.

#     Create, update, and manage calendar events.
#     Always confirm before modifying calendar.

#     If conflict exists:
#     - notify user
#     - propose replacement

#     Set reminders automatically.
#     Never overwrite events without approval.
#     """,
#     tools=[
#         create_event,
#         list_events_on_date,
#         create_task,
#         send_notification, # Make sure this is imported correctly
#         reschedule_event,
#         delete_event
#     ],
#     llm=llm,
#     verbose=True
# )

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from datetime import datetime

from mytools.calendar_tools import list_events_on_date, create_event, reschedule_event, delete_event

llm = ChatGoogleGenerativeAI(model="gemini-robotics-er-1.5-preview", api_key=os.getenv("GEMINI_API_KEY"))

calendar_tools = [
    list_events_on_date, 
    create_event, 
    reschedule_event, 
    delete_event
]

current_date = datetime.now().strftime("%A, %B %d, %Y")
system_prompt = f"""
You are Viki's dedicated Calendar Assistant. Today is {current_date}.
Your location is Sargodha, Punjab, Pakistan (Asia/Karachi timezone).

YOUR WORKFLOW:
1. Manage the user's schedule strictly using Google Calendar.
2. If asked about the schedule, use 'list_events_on_date' before replying.
3. If asked to create, move, or cancel an event, ask the user for confirmation first.
4. Once confirmed, use the appropriate tool ('create_event', 'reschedule_event', 'delete_event').
5. NEVER save calendar events to the database. Google Calendar is the only source of truth.

CRITICAL VOICE FORMATTING RULES:
- You are speaking out loud to the user. Keep your responses extremely concise.
- Limit your answers to 1 to 3 short sentences maximum.
- DO NOT use markdown, bolding, bullet points, or special characters. 
- Only provide a detailed, long-form list if the user explicitly asks for "the full plan" or "details".
"""

calendar_node = create_agent(llm, tools=calendar_tools, system_prompt=system_prompt)