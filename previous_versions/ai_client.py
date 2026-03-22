from google import genai
from google.genai.types import GenerateContentConfig

class AI_helper():
    def __init__(self):
        self.client = genai.Client(api_key="AIzaSyCVoPN42Izv2zJbZJE-wp9b-xV71DDh7wk")

    def answear_question(self, question):
        response = self.client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=question,
            config=GenerateContentConfig(
                system_instruction=[
                    "You're a study assistant to a child learning about the solar system.",
                    "Your mission is to respond to their questions with simple one sentence answers.",
                ])
            )
        return response.txt

