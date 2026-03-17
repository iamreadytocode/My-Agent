from crewai import Crew
from agents.MealAgent import meal_agent

meal_crew = Crew(
    agents=[meal_agent],    
    verbose=True
)