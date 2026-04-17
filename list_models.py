from dotenv import load_dotenv
from google import genai
import os

# Cargar variables del .env
load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("Error: GEMINI_API_KEY no configurada en .env")
    exit(1)

client = genai.Client(api_key=api_key)
print("Modelos disponibles en Gemini:")
for model in client.models.list():
    print(f"  - {model.name}")
