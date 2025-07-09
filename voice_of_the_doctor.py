import os
import elevenlabs
from dotenv import load_dotenv
from gtts import gTTS

# Load the ElevenLabs API key from environment variables
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

def text_to_speech_with_gtts(input_text, output_filepath):
    """
    Fallback function to convert text to speech using Google Text-to-Speech.

    Args:
        input_text (str): Text to convert to speech.
        output_filepath (str): Path to save the output MP3 file.
    """
    try:
        tts = gTTS(text=input_text, lang='en')
        tts.save(output_filepath)
        print(f"Audio successfully saved to {output_filepath} using gTTS")
        return None
    except Exception as e:
        print(f"An error occurred in gTTS: {e}")
        return f"An error occurred in gTTS: {e}"

def text_to_speech_with_elevenlabs(input_text, output_filepath):
    """
    Convert text to speech using ElevenLabs and save it as an MP3 file.
    Falls back to gTTS if ElevenLabs fails.

    Args:
        input_text (str): Text to convert to speech.
        output_filepath (str): Path to save the output MP3 file.
    """
    if not ELEVENLABS_API_KEY:
        print("ELEVENLABS_API_KEY not found, falling back to gTTS")
        return text_to_speech_with_gtts(input_text, output_filepath)

    try:
        # Create an instance of the ElevenLabs client
        client = elevenlabs.ElevenLabs(api_key=ELEVENLABS_API_KEY)

        # Generate the audio (the result is a generator object)
        print(f"Generating audio for text: {input_text}")  # Debugging line
        audio_generator = client.generate(
            text=input_text,
            voice="Aria",  # Ensure you're using the correct voice here
            output_format="mp3_22050_32",  # Request mp3 format
            model="eleven_turbo_v2"
        )

        # Convert the generator to bytes and save as an MP3 file
        with open(output_filepath, 'wb') as f:
            for chunk in audio_generator:
                f.write(chunk)  # Write chunks of the audio generator to the file

        print(f"Audio successfully saved to {output_filepath}")  # Debugging line
        return None
    except Exception as e:
        print(f"An error occurred in ElevenLabs TTS: {e}")
        print("Falling back to gTTS...")
        return text_to_speech_with_gtts(input_text, output_filepath)

# Test with a simple text to ensure everything works
if __name__ == "__main__":
    try:
        text_to_speech_with_elevenlabs("Hello, this is a test.", "test_output.mp3")
    except Exception as e:
        print(f"Error in text_to_speech_with_elevenlabs: {e}")
