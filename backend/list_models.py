import os
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

try:
    models = genai.list_models()
    for m in models:
        print(f"Model: {m.name}, generateContent: {'generateContent' in m.supported_generation_methods}")
except Exception as e:
    print(f"Error: {e}")
