# Step 1: Setup GROQ API key
import os
from dotenv import load_dotenv
from groq import Groq
import base64

# Load API key from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ API Key not found. Make sure it's set in your .env file.")

# Step 2: Convert image to required format
image_path = "acne.jpg"

def encode_image(image_path):
    """Encode image to base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Step 3: Setup multimodal LLM
query = "Analyze this skin condition."
model = "meta-llama/llama-4-scout-17b-16e-instruct"

def analyze_with_query(image_path, query):
    """Analyze an image using GROQ's multimodal LLM."""
    encoded_img = encode_image(image_path)
    client = Groq(api_key=GROQ_API_KEY)  # Initialize GROQ client

    # Prepare the message payload
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": query},  # User query
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_img}"}},  # Base64-encoded image
            ],
        }
    ]

    # Send request to GROQ API
    chat_completion = client.chat.completions.create(
        model=model,
        messages=messages
    )

    # Return the analysis result
    return chat_completion.choices[0].message.content

