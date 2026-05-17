from dotenv import load_dotenv
from google import genai
import os

print("🔍 Checking API Key...")

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ API Key পাওয়া যায়নি!")
    exit()

print("✅ API Key পাওয়া গেছে!")
print(f"Key শুরু হয়: {api_key[:20]}...")

client = genai.Client(api_key=api_key)

print("\n🧪 API Test করছি...")
print("👉 Model: gemini-2.5-flash\n")

# ✅ ঠিক model name দিয়ে test
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say 'Hello' in Bangla"
)

print(f"🤖 Response: {response.text}")
print("\n🎉 সব কিছু ঠিক আছে! API কাজ করছে!")