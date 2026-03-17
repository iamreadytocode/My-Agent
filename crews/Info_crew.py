from crewai import Crew
from agents.NewsAgent import news_agent

info_crew = Crew(
    agents=[news_agent],
    verbose=True
)
