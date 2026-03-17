# from crewai import Agent
# from crewai.llm import LLM
# import os

# from mytools.news_tools import *

# llm = LLM(model="gemini/gemini-1.5-flash", api_key=os.getenv("GEMINI_API_KEY"))

# news_agent = Agent(
#     role="news_agent",
#     goal="Summarize daily news and explain topics",
#     backstory="""
#     You are a news analyst.

# If user asks overview:
# - return headlines.

# If user asks deep dive:
# - summarize articles.

# Be factual.

# No opinions unless asked.
#     """,
#     tools=[
#         fetch_daily_news,
#         deep_dive_news
#     ],
#     llm=llm,
#     verbose=True
# )
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from datetime import datetime
from mytools.news_tools import fetch_daily_news, deep_dive_news

# 1. Initialize native Gemini
llm = ChatGoogleGenerativeAI(model="gemini-robotics-er-1.5-preview", api_key=os.getenv("GEMINI_API_KEY"))

# 2. Gather the tools
news_tools = [
    fetch_daily_news,
    deep_dive_news
]

# 3. The System Prompt
current_date = datetime.now().strftime("%A, %B %d, %Y")
system_prompt = f"""
You are Viki's dedicated News and Information Agent.
Today is {current_date}.

YOUR WORKFLOW:
1. Fetch the latest and most relevant news based on the user's request using your tools.
2. Summarize the information clearly and concisely. Avoid overwhelming the user with text.
3. If the user asks for updates on a specific topic, prioritize that over general headlines.
4. Do not invent news or hallucinate facts. Only rely on the information returned by your tools.

CRITICAL VOICE FORMATTING RULES:
- You are speaking out loud to the user. Keep your responses extremely concise.
- Limit your answers to 1 to 3 short sentences maximum.
- DO NOT use markdown, bolding, bullet points, or special characters. 
- Only provide a detailed, long-form list if the user explicitly asks for "the full plan" or "details".
"""

# 4. Create the LangGraph Node
news_node = create_agent(llm, tools=news_tools, system_prompt=system_prompt)