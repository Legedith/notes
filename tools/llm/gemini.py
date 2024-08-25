import google.generativeai as genai
import os
from dotenv import load_dotenv

class GeminiAI:
    def __init__(self, model_name="gemini-1.5-flash", system_instruction=None):
        load_dotenv()
        genai.configure(api_key=os.getenv("GEMINI_KEY"))
        if system_instruction:
            self.model = genai.GenerativeModel(model_name=model_name, system_instruction=system_instruction)
        else:
            self.model = genai.GenerativeModel(model_name=model_name)

    def generate_content(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text

# Example usage:
# gemini_ai = GeminiAI()
# response = gemini_ai.generate_content("Write a story about an AI and magic")
# print(response)