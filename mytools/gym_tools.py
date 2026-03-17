import json
import os
from langchain_core.tools import tool
# Ensure this file exists in the same directory or provide the absolute path
DATASET_PATH = "exercises.json"

with open(DATASET_PATH, "r", encoding="utf8") as f:
    EXERCISES = json.load(f)

@tool
def calculate_bmi(weight: float, height: float):
    """Calculate BMI from weight (kg) and height (cm)."""
    bmi = weight / ((height/100) ** 2)
    return round(bmi, 2)
@tool
def recommend_exercise(target_muscle: str):
    """
    Returns an exercise matching the target muscle group from the local database.
    """
    # Map broad workout split terms to specific JSON muscle names
    muscle_map = {
        "arms": ["biceps", "triceps", "forearms"],
        "back": ["lats", "lower back", "middle back", "traps"],
        "legs": ["quadriceps", "hamstrings", "calves", "glutes"],
        "shoulders": ["shoulders"],
        "chest": ["chest"]
    }
    
    # Get the specific muscles to search for based on the broad target
    search_terms = muscle_map.get(target_muscle.lower(), [target_muscle.lower()])

    matches = []
    for e in EXERCISES:
        # Check if any of our specific search terms match the exercise's primary muscles
        exercise_muscles = [m.lower() for m in e.get("primaryMuscles", [])]
        if any(term in exercise_muscles for term in search_terms):
            matches.append(e)

    if not matches:
        return f"No exercises found for {target_muscle}."

    chosen = matches[0]

    return {
        "name": chosen.get("name", "Unknown"),
        "instructions": chosen.get("instructions", "No instructions available."),
        "gif": chosen.get("images", ["No image"])[0]
    }

@tool
def get_workout_split(last_muscle: str):
    """Returns next muscle group based on standard workout split."""
    split = {
        "legs": "shoulders",
        "shoulders": "back",
        "back": "chest",
        "chest": "arms",
        "arms": "legs"
    }
    return split.get(last_muscle.lower(), "legs")

@tool
def estimate_calories_burned(weight: float, minutes: int, intensity: str):
    """
    Estimate calories burned during workout.
    intensity = low / medium / high
    """
    mets = {
        "low": 4,
        "medium": 7,
        "high": 10
    }
    met = mets.get(intensity.lower(), 7)
    calories = met * weight * (minutes / 60)
    return round(calories, 1)