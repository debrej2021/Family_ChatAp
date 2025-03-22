import os
from models.llm_model import FamilyLLM
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key is not set in the environment variables.")
    print("✅ API Key loaded successfully.")

    family_llm = FamilyLLM()
    print("🤖 Family Assistant Ready! Type your questions below.")
    print("💡 Type 'exit' or 'quit' to end the chat and save the conversation.\n")

    # Initialize conversation context
    messages = [
        {"role": "system", "content": "You are a friendly assistant that helps answer questions about the user's family and their careers."},
        {"role": "user", "content": "Here is my family:\n" + family_llm.get_family_list()}
    ]

    while True:
        user_input = input("🧑 You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        messages.append({"role": "user", "content": user_input})

        try:
            response = family_llm.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                max_tokens=700,
                temperature=0.7
            )
            reply = response.choices[0].message.content.strip()
            print(f"\n🤖 Assistant: {reply}\n")
            messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            print(f"❌ Error calling OpenAI API: {e}")
            break

    # Save chat history to file
    output_path = "output/chat_history.txt"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        for msg in messages:
            if msg["role"] == "user":
                file.write(f"🧑 You: {msg['content']}\n")
            elif msg["role"] == "assistant":
                file.write(f"🤖 Assistant: {msg['content']}\n")

    print(f"\n📁 Chat saved to {output_path}")
    print("👋 Goodbye!")

if __name__ == "__main__":
    main()
