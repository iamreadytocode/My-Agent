from crewai import Crew
from agents.GymAgent import gym_agent

gym_crew = Crew(
    agents=[gym_agent],
    verbose=True
)