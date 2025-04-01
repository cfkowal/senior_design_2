from openai import OpenAI
import base64
import time
import os
import cv2
import numpy as np
from dotenv import load_dotenv


class ImagePromptSolver:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"
        self.messages = []

    def get_system_prompt(self, mode="describe"):
        if mode == "math":
            return """You are an AI that extracts and solves handwritten math problems
                      from images. Given an image of a handwritten math problem, output
                      only the steps and the final solution in plain text, without any
                      explanation or formatting. Do not use LaTex, Markdown, or any special
                      characters beyond standard arithmetic symbols."""
        else:
            return "Describe the image in detail."

    def encode_image_to_base64(self, image):
        if isinstance(image, np.ndarray):
            _, buffer = cv2.imencode('.jpg', image)
            return base64.b64encode(buffer).decode('utf-8')
        else:
            with open(image, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')

    def capture_image_from_camera(self):
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            raise RuntimeError("Error: Could not open webcam.")

        time.sleep(1)
        ret, frame = cap.read()
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        cap.release()

        if not ret:
            raise RuntimeError("Error: Failed to capture image from webcam.")
        
        return frame

    def build_messages(self, prompt, image=None, use_camera=False, mode="describe"):
        self.messages = [
            {"role": "system", "content": self.get_system_prompt(mode)},
            {"role": "user", "content": []}
        ]

        if use_camera:
            image_data = self.capture_image_from_camera()
            base64_image = self.encode_image_to_base64(image_data)
        elif image:
            base64_image = self.encode_image_to_base64(image)
        else:
            base64_image = None

        if base64_image:
            self.messages[1]["content"].append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
            })

        self.messages[1]["content"].append({
            "type": "text",
            "text": prompt if prompt else "Solve this math problem"
        })

    def send_request(self):
        try:
            start_time = time.time()
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                max_tokens=1000
            )
            end_time = time.time()

            result = response.choices[0].message.content
            return result, end_time - start_time

        except Exception as e:
            return f"Error: {e}", None

    def run(self, prompt=None, image_path=None, use_camera=False, model="gpt-4o-mini", mode="describe"):
        self.model = model
        self.build_messages(prompt=prompt, image=image_path, use_camera=use_camera, mode=mode)
        result, duration = self.send_request()
        return result
