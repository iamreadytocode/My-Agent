from crewai import Crew
from agents.CalendarAgent import calendar_agent

productivity_crew = Crew(
    agents=[calendar_agent],
    verbose=True
)
