# Step 1: Setup audio recorder (ffmpeg & portaudio)
import os
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO

# Manually set FFmpeg path (update this to your FFmpeg installation path)
os.environ["FFMPEG_BINARY"] = r"C:\ffmpeg-2025-02-20-git-bc1a3bfd2c-full_build\ffmpeg-2025-02-20-git-bc1a3bfd2c-full_build\bin\ffmpeg.exe"

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Record audio from the microphone and save it as an MP3 file.
    
    Args:
        file_path (str): Path to save the recorded audio file.
        timeout (int): Max time to wait for speech (in seconds).
        phrase_time_limit (int): Max duration of speech (in seconds).
    
    Returns:
        bool: True if recording and saving were successful, False otherwise.
    """
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")

            # Record audio
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")

            # Convert to MP3
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            logging.info(f"Audio saved to {file_path}")

            return True  # Success

    except Exception as e:
        logging.error(f"Error recording audio: {e}")
        return False  # Failure

# Step 2: Setup speech-to-text (STT) for transcription
from dotenv import load_dotenv
from groq import Groq

# Load GROQ API key from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set. Please check your .env file.")

stt_model = "whisper-large-v3-turbo"

def transcribe_with_groq(audio_filepath, GROQ_API_KEY):
    """
    Transcribe audio using GROQ's speech-to-text API.

    Args:
        audio_filepath (str): Path to the audio file to transcribe.
        GROQ_API_KEY (str): GROQ API key.

    Returns:
        str: The transcribed text.
    """
    client = Groq(api_key=GROQ_API_KEY)

    if not os.path.exists(audio_filepath):
        raise FileNotFoundError(f"Audio file '{audio_filepath}' not found. Please record audio first.")

    try:
        with open(audio_filepath, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-large-v3-turbo",
                file=audio_file,
                language="en"
            )
        return transcription.text
    except Exception as e:
        raise Exception(f"Error transcribing audio: {e}")
    
if __name__ == "__main__":
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    audio_filepath = "patient_voice_test.mp3"
    transcribed_text = transcribe_with_groq(audio_filepath, GROQ_API_KEY)
    print("Transcribed Text:", transcribed_text)


