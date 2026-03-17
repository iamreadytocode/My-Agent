from agents.NewsAgent import news_agent
from crewai import Task, Crew
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


task = Task(
    description="Get me top 3 tech news headlines today",
    expected_output="A list of 3 current tech headlines",
    agent=news_agent
)

crew = Crew(
    agents=[news_agent],
    tasks=[task]
)

print(crew.kickoff())
