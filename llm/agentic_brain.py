import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

# 1. Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ CRITICAL ERROR: GEMINI_API_KEY not found in .env file.")

genai.configure(api_key=api_key)

# --- MODEL ARSENAL ---
# We map simple keywords to the powerful model IDs you have access to.
MODELS = {
    # --- Standard Daily Drivers ---
    "fast": "models/gemini-2.5-flash",          # Super fast, good for quick chats
    "smart": "models/gemini-2.5-pro",           # Excellent reasoning
    
    # --- The Heavy Hitters (God Mode) ---
    "ultra": "models/gemini-3-pro-preview",     # The smartest model available
    "flash_ultra": "models/gemini-3-flash-preview", # Insane speed + intelligence
    "experimental": "models/nano-banana-pro-preview", # The mysterious 'Banana' model
    
    # --- Specialized Creative ---
    "painter": "models/gemini-2.0-flash-exp-image-generation", # Specifically for creating images
}

def get_completion(prompt, image=None, system_instruction=None, model_type="fast"):
    """
    Universal Brain Function.
    
    Args:
        prompt (str): Text input.
        image (str/PIL.Image): Optional image for VIKI to see.
        system_instruction (str): Persona (e.g., "You are a Coder").
        model_type (str): Key from the MODELS dict (e.g., "fast", "ultra", "experimental").
    """
    try:
        # 1. Pick the model (default to 'fast' if key not found)
        # If you pass a raw model name (like "models/gemini-3..."), it uses that directly.
        model_name = MODELS.get(model_type, model_type)
        
        # 2. Configure the model
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_instruction
        )
        
        # 3. Prepare the payload (Text + Optional Image)
        content = [prompt]
        
        if image:
            if isinstance(image, str): # Load from file path
                img_obj = Image.open(image)
                content.append(img_obj)
            else: # Already an image object
                content.append(image)

        # 4. Generate
        response = model.generate_content(content)
        return response.text.strip()

    except Exception as e:
        return f"❌ Brain Error ({model_type}): {str(e)}"

def generate_image(prompt):
    """
    Uses the specialized model to CREATE images.
    """
    try:
        print(f"🎨 Painting: {prompt}...")
        model = genai.GenerativeModel(MODELS["painter"])
        response = model.generate_content(prompt)
        
        # Google's Image Gen returns a generated image object, usually inside parts
        # This handles saving it to a file automatically for you
        if response.parts:
            return response.parts[0] # Returns the raw image data
        else:
            return "❌ No image generated."
            
    except Exception as e:
        return f"❌ Image Gen Error: {str(e)}"

# --- TEST BLOCK ---
if __name__ == "__main__":
    print("--- 🧠 VIKI Ultimate Brain Test ---")
    
    # Test 1: Code with the new Flash Ultra (Gemini 3 Flash)
    print("\n1. Testing Code (Gemini 3 Flash)...")
    print(get_completion("Write a Python hello world loop", model_type="flash_ultra"))

    # Test 2: Deep Reasoning with Gemini 3 Pro
    print("\n2. Testing Logic (Gemini 3 Pro)...")
    print(get_completion("Explain quantum entanglement to a 5 year old", model_type="ultra"))

    # Test 3: The Mystery Model (Nano Banana)
    print("\n3. Testing Nano Banana...")
    print(get_completion("Who are you?", model_type="experimental"))

    print("\n✅ All systems operational.")