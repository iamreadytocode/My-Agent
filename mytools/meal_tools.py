import os

from langchain_core.tools import tool
from google import genai
from google.genai import types


# Initialize the client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

import mimetypes

@tool
def analyze_food_image(image_path: str):
    """
    Analyze food image and return nutrition estimate.
    """

    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        mime_type, _ = mimetypes.guess_type(image_path)
        mime_type = mime_type or "image/jpeg"

        response = client.models.generate_content(
            model="models/gemini-2.5-flash",   # better current choice
            contents=[
                types.Content(
                    parts=[
                        types.Part.from_text(
                            text="Identify this food and estimate calories/macros. Use ranges, not exact values."
                        ),
                        types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
                    ]
                )
            ]
        )

        return response.text

    except Exception as e:
        return f"Error analyzing image: {str(e)}"


@tool
def calculate_daily_calories(weight: float, height: float, age: int, activity: str):
    """
    Returns daily maintenance calories.
    """

    bmr = 10 * weight + 6.25 * height - 5 * age + 5

    multiplier = {
        "low": 1.2,
        "medium": 1.55,
        "high": 1.8
    }

    return round(bmr * multiplier.get(activity, 1.55))

@tool
def calculate_macros(calories: int, goal: str):
    """
    Returns protein/carbs/fat grams.
    """

    if goal == "fat_loss":
        protein = calories * 0.35 / 4
        carbs = calories * 0.35 / 4
        fat = calories * 0.3 / 9

    elif goal == "muscle_gain":
        protein = calories * 0.3 / 4
        carbs = calories * 0.5 / 4
        fat = calories * 0.2 / 9
    else:  # maintenance
        protein = calories * 0.3 / 4
        carbs = calories * 0.4 / 4
        fat = calories * 0.3 / 9    

    return {
        "protein_g": round(protein),
        "carbs_g": round(carbs),
        "fat_g": round(fat)
    }

@tool
def sum_day_calories(meals: list[dict]):  # <--- CHANGED THIS LINE
    """Sum calories from list of meals."""
    total = 0
    for m in meals:
        total += m.get("calories", 0)
    return total

@tool
def calculate_remaining_calories(target: int, consumed: int):
    """Return remaining daily calories."""
    return max(target - consumed, 0)
