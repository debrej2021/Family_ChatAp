import os
from models.llm_model import FamilyLLM
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"API Key Loaded: {api_key}")
    if not api_key:
        raise ValueError("API key is not set in the environment variables.")
    
    print("API Key loaded successfully.")
    
    family_llm = FamilyLLM()
    print("Family LLM object created.")
    
    family_professions = family_llm.get_family_professions()
    print("Family professions fetched successfully.\n")
    
    print("🧑‍🤝‍🧑 Family Members and Their Professions:\n")
    print(family_professions)

    # ✅ Save to file inside main
    output_file = "output/family_career_summary.txt"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Create output folder if needed

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(family_professions)

    print(f"\n✅ Output saved to {output_file}")

if __name__ == "__main__":
    main()
