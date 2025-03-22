import os
import json
import openai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load .env file if available

print("OpenAI version:", openai.__version__)

class FamilyLLM:
    def __init__(self, data_path="data/family_data.json"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.api_key = self.client.api_key
        print(f"Loaded API Key: {self.api_key is not None}")
        
        try:
            with open(data_path, "r") as file:
                self.family_data = json.load(file)["family"]
            print(f"Family data loaded successfully from {data_path}")
        except Exception as e:
            print(f"Error loading family data: {e}")

    def get_family_list(self):
        return "\n".join([
        f"{member['name']} is a {member['profession']}" for member in self.family_data
    ])


    def get_family_professions(self):
        family_info = "\n".join([
            f"Name: {member['name']}\nProfession: {member['profession']}\n"
            for member in self.family_data
        ])
        
        prompt = f"""
Below is information about my family. For each member, provide a personalized career summary.

Please include:
1. Their likely day-to-day responsibilities based on their profession.
2. The top 5 technical and soft skills essential for them.
3. Recommended certifications or advanced degrees to grow further.
4. Strategic long-term career advice including leadership, networking, or entrepreneurship paths.
5. For retired members, meaningful post-retirement contributions like writing, speaking, or mentoring.

{family_info}
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant and career strategist."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            print("OpenAI response received.")
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return "Failed to retrieve data from OpenAI."
