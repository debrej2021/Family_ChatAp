import openai
import os

# Load your OpenAI API key

# List available models using the correct API method
try:
    models = openai.models.list()  # Correct method for OpenAI v1.0.0+
    print("Available models:")
    for model in models.data:  # Accessing the models data correctly
        print(model.id)  # Print model IDs
except Exception as e:
    print(f"Error retrieving models: {e}")
