# import sys
# import os
# from dotenv import load_dotenv 
# load_dotenv() 
# from orchestrator import process_user_input
# from voice.voice_manager import VoiceManager


# def main():
#     print("="*50)
#     print("🤖 Viki OS Initialization Complete")
#     print("="*50)
#     print("Instructions:")
#     print("- Type your message and press Enter for TEXT mode.")
#     print("- Type '/v' and press Enter to use VOICE mode.")
#     print("- Type 'exit' to shut down.")
#     print("="*50)

#     # Initialize your voice manager
#     voice = VoiceManager()  # Make sure this matches your actual class name and import
    
#     # Optional: Have Viki greet you on startup
#     voice.text_to_speech("Viki is online and ready.")

#     while True:
#         try:
#             # 1. Wait for user input
#             user_input = input("\nYou: ").strip()

#             # 2. Handle Shutdown
#             if user_input.lower() in ['exit', 'quit']:
#                 print("\nViki: Shutting down systems. Goodbye.")
#                 voice.text_to_speech("Shutting down systems. Goodbye.")
#                 break

#             # 3. Handle Voice Mode
#             elif user_input.lower() == '/v':
#                 print("\n🎤 [Microphone Active - Speak Now]")
                
#                 # Capture from the mic!
#                 text_from_audio = voice.listen() 
                
#                 # (Placeholder line has been completely removed)
                
#                 if not text_from_audio:
#                     print("⚠️ Didn't catch that. Returning to text mode.")
#                     continue
                    
#                 print(f"You (Voice): {text_from_audio}")
#                 print("⚙️ Viki is thinking...")
                
#                 # Route the transcribed audio to LangGraph
#                 response = process_user_input(text_from_audio)
                
#                 print(f"\nViki: {response}")
                
#                 # Speak the response out loud
#                 voice.text_to_speech(response)
#             # 4. Handle Text Mode
#             else:
#                 if not user_input:
#                     continue
                    
#                 print("⚙️ Viki is thinking...")
                
#                 # Route the text to LangGraph
#                 response = process_user_input(user_input)
                
#                 print(f"\nViki: {response}")

#         # Handle Ctrl+C gracefully so it doesn't print a massive red error during a demo
#         except KeyboardInterrupt:
#             print("\n\nViki: Force quit detected. Shutting down. Goodbye!")
#             sys.exit()
            
#         except Exception as e:
#             print(f"\n⚠️ An error occurred in the main loop: {str(e)}")

# if __name__ == "__main__":
#     main()

import sys
import os
from dotenv import load_dotenv 
load_dotenv() 

from orchestrator import process_user_input
from voice.voice_manager import VoiceManager

# Initialize the voice manager globally so it is ready the moment the Flet app imports this file
print("🤖 Initializing Viki Engine...")
voice = VoiceManager()

def get_viki_response(text_input: str) -> str:
    """
    Handles standard text input from the Flet text box.
    Routes the text to the LangGraph orchestrator and returns the response.
    """
    try:
        if not text_input or text_input.strip() == "":
            return "Please provide an input."
            
        print("⚙️ Viki is thinking...")
        response = process_user_input(text_input)
        return response
        
    except Exception as e:
        print(f"⚠️ Error in get_viki_response: {str(e)}")
        return f"An error occurred: {str(e)}"

def start_voice_interaction():
    """
    Triggered when the user clicks the Microphone button in Flet.
    Listens to the user, processes the text, speaks the response, 
    and returns both the transcribed text and Viki's response for the UI.
    """
    try:
        print("\n🎤 [Microphone Active - Speak Now]")
        # Capture from the mic
        text_from_audio = voice.listen() 
        
        if not text_from_audio:
            return None, "I didn't catch that. Could you please repeat?"

        print(f"You (Voice): {text_from_audio}")
        print("⚙️ Viki is thinking...")
        
        # Route the transcribed audio to LangGraph
        response = process_user_input(text_from_audio)
        
        print(f"\nViki: {response}")
        
        # Speak the response out loud natively
        voice.text_to_speech(response)
        
        return text_from_audio, response
        
    except Exception as e:
        print(f"⚠️ Error in start_voice_interaction: {str(e)}")
        return "Voice Error", f"An error occurred: {str(e)}"

def play_tts(text: str):
    """
    A helper function allowing the UI to trigger text-to-speech manually.
    """
    try:
        voice.text_to_speech(text)
    except Exception as e:
        print(f"⚠️ Error playing TTS: {str(e)}")

# --- STANDALONE TEST BLOCK ---
if __name__ == "__main__":
    # This block only runs if you execute `python viki_engine.py` directly in the terminal.
    # It acts as a safety net to debug your agents without needing to launch the UI.
    print("="*50)
    print("🤖 Viki Engine - Standalone Test Mode")
    print("="*50)
    
    test_input = input("\nTest text input (or type '/v' for voice): ").strip()
    
    if test_input.lower() == '/v':
        user_said, viki_replied = start_voice_interaction()
    else:
        response = get_viki_response(test_input)
        print(f"\nViki: {response}")
        play_tts(response)