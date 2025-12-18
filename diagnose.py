import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: API Key nahi mili! .env file check karo.")
else:
    print(f"✅ API Key mil gayi: {api_key[:5]}********")
    
    # Configure Google AI
    try:
        genai.configure(api_key=api_key)
        
        print("\n🔍 Google ke paas available models dhoond raha hu...")
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f" - Found: {m.name}")
                available_models.append(m.name)
        
        if not available_models:
            print("\n❌ Koi model nahi mila! Shayad API Key mein dikkat hai.")
        else:
            print("\n✅ Models mil gaye! Ab hum test karte hain...")
            # Pick the first available model to test
            test_model = "gemini-1.5-flash"
            print(f"🧪 Testing with {test_model}...")
            
            model = genai.GenerativeModel(test_model)
            response = model.generate_content("Hello, bas confirm karo ki tum chal rahe ho.")
            print(f"\n🤖 AI Response: {response.text}")

    except Exception as e:
        print(f"\n❌ Bhaari Error aaya: {e}")