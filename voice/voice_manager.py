import whisper
import speech_recognition as sr 
from pathlib import Path
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from elevenlabs import stream 
import os
import time
from elevenlabs import save
import pygame # <--- Import this at the top



class VoiceManager:
    def __init__(self):
        print("[Voice] Initializing Voice Manager...")
        
        # Setup ElevenLabs
        self.eleven_api_key = os.getenv("ELEVEN_API_KEY")
        if not self.eleven_api_key:
            raise ValueError("Error: ELEVEN_API_KEY not found in .env file.")
        
        self.client = ElevenLabs(api_key=self.eleven_api_key)
        self.voice_id = "JBFqnCBsd6RMkjVDRZzb" 

        # Setup Whisper locally
        print("[Voice] Loading local Whisper model (this may take a moment)...")
        self.whisper_model = whisper.load_model("small")
        
        # Setup Microphone
        self.recognizer = sr.Recognizer()
        
        print("[Voice] System Ready.")

# ... inside your VoiceManager class ...

    def text_to_speech(self, text):
        """Generates audio and plays it silently in the background."""
        try:
            # 1. Generate the audio
            audio = self.client.text_to_speech.convert(
                text=text,
                voice_id=self.voice_id,
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128",
            )
            
            # 2. Save it to a temporary file
            filename = "viki_temp_audio.mp3"
            save(audio, filename)
            
            # 3. Play it invisibly using Pygame's mixer
            pygame.mixer.init()
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            
            # Keep the script paused just long enough for Viki to finish talking
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
            # Free up the file so we can delete it or overwrite it next time
            pygame.mixer.quit()
            
            # Optional: Clean up the temp file so your folder stays tidy
            if os.path.exists(filename):
                os.remove(filename)
            
        except Exception as e:
            print(f"[TTS Error]: {e}")

    def speech_to_text(self, audio_filename):
        """Uses Local Whisper model to transcribe an audio file."""
        file_path = Path(audio_filename).resolve()

        if not file_path.exists():
            print(f"[STT Error] File not found: {file_path}")
            return ""

        try:
            result = self.whisper_model.transcribe(str(file_path))
            return result["text"].strip()
        except Exception as e:
            print(f"[STT Error] Whisper failed: {e}")
            return ""

    # def listen(self):
    #     """Captures audio from the mic, saves it, and transcribes it."""
    #     try:
    #         with sr.Microphone() as source:
    #             print("\n🎤 Listening... (Speak now)")
                
    #             # Dynamic energy threshold for ambient noise
    #             self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
    #             # Listen until silence is detected
    #             audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
    #             print("💾 Processing audio...")
                
    #             # Save to temporary file
    #             temp_filename = "temp_voice_input.wav"
    #             with open(temp_filename, "wb") as f:
    #                 f.write(audio.get_wav_data())
                
    #             # Transcribe using your existing Whisper method
    #             text = self.speech_to_text(temp_filename)
                
    #             # Clean up temp file (optional)
    #             # os.remove(temp_filename)
                
    #             return text
                
    #     except sr.WaitTimeoutError:
    #         print("⚠️ Listening timed out (No speech detected).")
    #         return ""
    #     except Exception as e:
    #         print(f"⚠️ Microphone error: {e}")
    #         return ""
    def listen(self):
        """Captures audio from the mic, saves it, and transcribes it."""
        try:
            with sr.Microphone() as source:
                print("\n🎤 Listening... (Speak now)")
                
                # --- PATIENCE SETTINGS ---
                # 1. Wait 2 full seconds of silence before ending the phrase
                self.recognizer.pause_threshold = 2.0 
                
                # 2. Helps filter out background noise in your environment
                self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
                
                # 3. Increase phrase_time_limit so you can speak for longer (e.g., 20 seconds)
                # timeout=7: how long Viki waits for you to START speaking
                audio = self.recognizer.listen(source, timeout=7, phrase_time_limit=20)
                
                print("💾 Processing audio...")
                
                # Save to temporary file
                temp_filename = "temp_voice_input.wav"
                with open(temp_filename, "wb") as f:
                    f.write(audio.get_wav_data())
                
                # Transcribe using your existing Whisper method
                text = self.speech_to_text(temp_filename)
                
                return text
                
        except sr.WaitTimeoutError:
            print("⚠️ Listening timed out (No speech detected).")
            return ""
        except Exception as e:
            print(f"⚠️ Microphone error: {e}")
            return ""

# import os
# import whisper
# from pathlib import Path
# from dotenv import load_dotenv

# # ElevenLabs Imports
# from elevenlabs.client import ElevenLabs
# from elevenlabs.play import play

# # Load API keys
# load_dotenv()

# class VoiceManager:
#     def __init__(self):
#         print("[Voice] Initializing Voice Manager...")
        
#         # Setup ElevenLabs
#         self.eleven_api_key = os.getenv("ELEVEN_API_KEY")
#         if not self.eleven_api_key:
#             raise ValueError("Error: ELEVEN_API_KEY not found in .env file.")
        
#         self.client = ElevenLabs(api_key=self.eleven_api_key)
#         # voide id for Adam voice
#         self.voice_id = "JBFqnCBsd6RMkjVDRZzb" 

#         # Setup Whisper locally
#         print("[Voice] Loading local Whisper model (this may take a moment)...")
#         self.whisper_model = whisper.load_model("small")
#         print("[Voice] System Ready.")

#     def text_to_speech(self, text):
#         """
#         Uses ElevenLabs API to generate and play audio.
#         """
#         try:
#             # Generate audio stream
#             audio = self.client.text_to_speech.convert(
#                 text=text,
#                 voice_id=self.voice_id,
#                 model_id="eleven_multilingual_v2",
#                 output_format="mp3_44100_128",
#             )
#             # Play audio
#             play(audio)
#         except Exception as e:
#             print(f"[TTS Error] ElevenLabs failed: {e}")

#     def speech_to_text(self, audio_filename):
#         """
#         Uses Local Whisper model to transcribe an audio file.
#         """
#         file_path = Path(audio_filename).resolve()

#         if not file_path.exists():
#             print(f"[STT Error] File not found: {file_path}")
#             return ""

#         try:
#             # Transcribe locally (no API cost)
#             result = self.whisper_model.transcribe(str(file_path))
#             return result["text"].strip()
#         except Exception as e:
#             print(f"[STT Error] Whisper failed: {e}")
#             return ""
        
