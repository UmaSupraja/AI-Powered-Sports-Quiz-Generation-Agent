from google import genai
from src.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL = "gemini-2.0-flash-lite"   # Change this for each test

print("Testing:", MODEL)

try:
    response = client.models.generate_content(
        model=MODEL,
        contents="Reply with only the word Hello."
    )

    print("\nSUCCESS")
    print(response.text)

except Exception as e:
    print("\nFAILED")
    print(type(e).__name__)
    print(e)