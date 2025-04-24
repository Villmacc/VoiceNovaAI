# Step 1a: Setup Text-to-Speech (TTS) with gTTS
import os
from gtts import gTTS
import subprocess
import platform

# def text_to_speech_with_gtts(input_text, output_filepath):
#     """
#     Convert text to speech using gTTS and save it as an MP3 file.
#     Autoplay the generated audio file.

#     Args:
#         input_text (str): Text to convert to speech.
#         output_filepath (str): Path to save the output MP3 file.
#     """
#     try:
#         # Create gTTS object
#         audioobj = gTTS(
#             text=input_text,
#             lang="en",
#             slow=False
#         )
#         # Save the audio file
#         audioobj.save(output_filepath)
#         print(f"Audio saved to {output_filepath}")

#         # Autoplay the file using subprocess
#         autoplay_audio(output_filepath)

#     except Exception as e:
#         print(f"An error occurred in gTTS: {e}")

# Step 1b: Setup Text-to-Speech (TTS) with ElevenLabs
import elevenlabs
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

# Load ElevenLabs API key from .env
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY is not set. Please check your .env file.")

def text_to_speech_with_elevenlabs(input_text, output_filepath):
    """
    Convert text to speech using ElevenLabs and save it as an MP3 file.
    Autoplay the generated audio file.

    Args:
        input_text (str): Text to convert to speech.
        output_filepath (str): Path to save the output MP3 file.
    """
    try:
        # Create an instance of the ElevenLabs client
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

        # Generate audio
        audio = client.generate(
            text=input_text,
            voice="Aria",
            output_format="mp3_22050_32",
            model="eleven_turbo_v2"
        )
        # Save the audio file
        elevenlabs.save(audio, output_filepath)
        print(f"Audio saved to {output_filepath}")

        # Autoplay the file using subprocess
        autoplay_audio(output_filepath)

    except Exception as e:
        return f"An error occurred in ElevenLabs: {e}"

# def autoplay_audio(file_path):
#     """
#     Autoplay an audio file based on the operating system.

#     Args:
#         file_path (str): Path to the audio file.
#     """
#     try:
#         if platform.system() == "Windows":
#             subprocess.run(["start", "", file_path], shell=True)  # ✅ Uses default player
#         elif platform.system() == "Darwin":  # macOS
#             subprocess.run(["afplay", file_path])
#         elif platform.system() == "Linux":  # Linux
#             subprocess.run(["aplay", file_path])  # Use 'aplay' for Linux
#         else:
#             raise OSError("Unsupported Operating System")
#     except Exception as e:
#         return f"An error occurred while playing the audio: {e}"

# Example usage
# if __name__ == "__main__":
#     input_text = "Hi, this is Dr AI. How can I assist you today?"

#     # Test gTTS
#     #text_to_speech_with_gtts(input_text, output_filepath="gtts_testing_autoplay.mp3")

#     # Test ElevenLabs
#     text_to_speech_with_elevenlabs(input_text, output_filepath="elevenlabs_testing_autoplay.mp3")