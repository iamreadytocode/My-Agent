# from crewai import Agent
# from mytools.email_tools import *
# # from mytools.calendar_tools import *
# from crewai.llm import LLM
# import os

# llm = LLM(model="gemini/gemini-robotics-er-1.5-preview", api_key=os.getenv("GEMINI_API_KEY"))

# email_agent = Agent(
#     role="email_agent",
#     goal="Handle personal emails and send responses",
#     backstory="""
#     You are an email assistant.

# Read unread emails.
# Summarize clearly.

# When replying:
# - draft response
# - ask confirmation
# - send only after approval.

# Resolve ambiguous names using memory.

# Never send emails without confirmation.
#     """,
#     tools=[
#         check_unread_emails,
#         send_email,
#         get_contact_email
#     ],
#     llm=llm,
#     verbose=True
# )

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from datetime import datetime

# Import your specific tools (Ensure these use langchain_core.tools!)
from mytools.email_tools import check_unread_emails, send_email, get_contact_email

# 1. Initialize native Gemini
llm = ChatGoogleGenerativeAI(model="gemini-robotics-er-1.5-preview", api_key=os.getenv("GEMINI_API_KEY"))

# 2. Gather the tools
email_tools = [
    check_unread_emails, 
    send_email, 
    get_contact_email
]

# 3. The System Prompt (Your old CrewAI backstory)
current_date = datetime.now().strftime("%A, %B %d, %Y")
system_prompt = f"""
You are Viki's dedicated Email Assistant. Today is {current_date}.

YOUR WORKFLOW:
1. Use 'check_unread_emails' to find new messages.
2. If an email is important, draft a reply. Use 'get_contact_email' to find addresses if needed.
3. Use 'send_email' to send out messages. If it's a new email, leave thread_id empty. If it's a reply, include the thread_id to keep it in the same conversation.
4. Do not make up email addresses; rely on your tools.

CRITICAL VOICE FORMATTING RULES:
- You are speaking out loud to the user. Keep your responses extremely concise.
- Limit your answers to 1 to 3 short sentences maximum.
- DO NOT use markdown, bolding, bullet points, or special characters. 
- Only provide a detailed, long-form list if the user explicitly asks for "the full plan" or "details".
"""

# 4. Create the LangChain Agent Node (Replaces create_react_agent)
email_node = create_agent(llm, tools=email_tools, system_prompt=system_prompt)