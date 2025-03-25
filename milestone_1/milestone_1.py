from openai import OpenAI
import base64
import os
import argparse
import time
from dotenv import load_dotenv

load_dotenv()  # Loads from .env file

api_key = os.getenv("OPENAI_API_KEY")

# Initialize the client to access OpenAI models
client = OpenAI(api_key=api_key)

# Define the default system prompt to prepend to the front
SYSTEM_PROMPT = """You are an AI that extracts and solves handwritten math problems
                    from images. Given an image of a handwritten math problem, output
                    only the steps and the final solution in plain text, without any
                    explanation or formatting. Do not use LaTex, Markdown, or any special
                    characters beyond standard arithmetic symbols."""

# Set up argument parser
parser = argparse.ArgumentParser(description="Send a message to OpenAI API with optional image")
parser.add_argument("--prompt", type=str, help="Additional user prompt (optional)")
parser.add_argument("--image", type=str, help="Path to image file (optional)")
parser.add_argument("--model", type=str, default="gpt-4o-mini", help="Model to use")
args = parser.parse_args()

# Initialize messages with system prompt
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": []}
]

# Add image if provided
if args.image:
    with open(args.image, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
    messages[1]["content"].append({
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
        }
    })

# Combine with user prompt if provided
user_prompt = args.prompt if args.prompt else "Please describe what you see in this image."
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
        max_tokens=300
    )
    end_time = time.time()

    print(response.choices[0].message.content)
    print(f"\nTime Taken: {end_time - start_time:.2f} seconds")
except Exception as e:
    print(f"Error: {e}")
