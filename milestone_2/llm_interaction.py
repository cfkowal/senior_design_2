from openai import OpenAI
import base64
import argparse
import time
import os
import cv2
import numpy as np
from dotenv import load_dotenv

load_dotenv()  # Loads from .env file

api_key = os.getenv("OPENAI_API_KEY")

# Initialize the client to access OpenAI models
client = OpenAI(api_key=api_key)
# Define the default system prompt to prepend to the front
SYSTEM_PROMPT2 = """You are an AI that extracts and solves handwritten math problems
                    from images. Given an image of a handwritten math problem, output
                    only the steps and the final solution in plain text, without any
                    explanation or formatting. Do not use LaTex, Markdown, or any special
                    characters beyond standard arithmetic symbols."""

SYSTEM_PROMPT = """Describe the image in detail."""

# Set up argument parser
parser = argparse.ArgumentParser(description="Send a message to OpenAI API with optional image")
parser.add_argument("--prompt", type=str, help="Additional user prompt (optional)")
parser.add_argument("--image", type=str, help="Path to image file (optional)")
parser.add_argument("--use_camera", action="store_true", help="Use webcam to capture image")
parser.add_argument("--model", type=str, default="gpt-4o-mini", help="Model to use")
args = parser.parse_args()

# Function to encode image to base64
def encode_image_to_base64(image):
    # If image is a numpy array (from webcam)
    if isinstance(image, np.ndarray):
        _, buffer = cv2.imencode('.jpg', image)
        return base64.b64encode(buffer).decode('utf-8')
    # If image is a file path
    else:
        with open(image, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

# Initialize messages with system prompt
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": []}
]

# Get image from webcam if requested
if args.use_camera:
    print("Capturing image from webcam...")
    
    # Initialize video capture
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()
    
    # Allow the camera to warm up
    time.sleep(1)
    
    # Capture a single frame
    ret, frame = cap.read()
    
    # Release the webcam
    cap.release()
    
    if not ret:
        print("Error: Failed to capture image from webcam.")
        exit()
    
    print("Image captured successfully!")
    
    # Add the captured image to messages
    base64_image = encode_image_to_base64(frame)
    messages[1]["content"].append({
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
        }
    })

# Add image from file if provided
elif args.image:
    base64_image = encode_image_to_base64(args.image)
    messages[1]["content"].append({
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
        }
    })

# Combine with user prompt if provided
user_prompt = args.prompt if args.prompt else "Solve this math problem"
messages[1]["content"].append({
    "type": "text",
    "text": user_prompt
})

# Send the query to the model and print the first response
try:
    start_time = time.time()
    response = client.chat.completions.create(
        model=args.model,
        messages=messages,
        max_tokens=1000
    )
    end_time = time.time()

    print(response.choices[0].message.content)
    print(f"\nTime Taken: {end_time - start_time:.2f} seconds")
except Exception as e:
    print(f"Error: {e}")
