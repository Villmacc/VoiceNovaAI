import gradio as gr
import os

# Import custom functions
from brain_of_the_doctor import encode_image, analyze_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_elevenlabs

# System prompt for the AI doctor
SYSTEM_PROMPT = """
You have to act as a professional doctor. This is for learning purposes.
What's in this image? Do you find anything wrong with it medically?
If you make a differential diagnosis, suggest some remedies for them.
Do not add any numbers or special characters in your response.
Your response should be in one long paragraph.
Always answer as if you are speaking to a real person.
Do not say 'In the image I see...' but say 'With what I see, I think you have...'.
Do not respond as an AI model in markdown; your answer should mimic that of an actual doctor, not an AI bot.
Keep your answer concise (max 2 sentences). No preamble—start your answer right away, please.
"""

def process_input(audio_path, image_path):
    """
    Processes user audio and image to generate AI response and voice output.

    Args:
        audio_path (str): Path to the recorded audio file.
        image_path (str): Path to the uploaded image file.

    Returns:
        tuple: Transcribed text, AI response, and path to the generated audio file.
    """
    # Step 1: Convert speech to text
    if not audio_path:
        return "No audio provided.", "", None
    
    try:
        # Load GROQ API key from environment
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        if not GROQ_API_KEY:
            return "GROQ_API_KEY not found. Please check your .env file.", "", None

        # Transcribe audio
        transcribed_text = transcribe_with_groq(audio_path, GROQ_API_KEY)
    except Exception as e:
        return f"Error transcribing audio: {e}", "", None

    # Combine transcribed text with system prompt
    full_query = f"{SYSTEM_PROMPT} {transcribed_text}"

    # Step 2: Process image and AI analysis
    if not image_path:
        return transcribed_text, "No image provided.", None
    
    try:
        ai_response = analyze_with_query(image_path, full_query)
    except Exception as e:
        return transcribed_text, f"Error analyzing image: {e}", None

    # Step 3: Convert AI response to speech
    output_audio_path = "doctor_response.mp3"
    try:
        text_to_speech_with_elevenlabs(ai_response, output_audio_path)
    except Exception as e:
        return transcribed_text, ai_response, f"Error generating speech: {e}"

    return transcribed_text, ai_response, output_audio_path

    # Step 3: Convert AI response to speech
    output_audio_path = "doctor_response.mp3"
    try:
        text_to_speech_with_elevenlabs(ai_response, output_audio_path)
    except Exception as e:
        return transcribed_text, ai_response, f"Error generating speech: {e}"

    return transcribed_text, ai_response, output_audio_path

    # Step 3: Convert AI response to speech
    output_audio_path = "doctor_response.mp3"
    try:
        text_to_speech_with_elevenlabs(ai_response, output_audio_path)
    except Exception as e:
        return transcribed_text, ai_response, f"Error generating speech: {e}"

    return transcribed_text, ai_response, output_audio_path

    # Step 3: Convert AI response to speech
    output_audio_path = "doctor_response.mp3"
    try:
        text_to_speech_with_gtts(ai_response, output_audio_path)
    except Exception as e:
        return transcribed_text, ai_response, f"Error generating speech: {e}"

    return transcribed_text, ai_response, output_audio_path

# Create the Gradio interface
iface = gr.Interface(
    fn=process_input,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath", label="Record Your Voice"),
        gr.Image(type="filepath", label="Upload an Image")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(label="Doctor's Voice Response", autoplay=True)
    ],
    title="AI Doctor with Vision and Voice",
    description="Speak and upload an image. The AI doctor will analyze and respond with voice.",
    live=False  # Disable live updates for better performance
)

# Launch the interface
iface.launch(share=True, debug=True)