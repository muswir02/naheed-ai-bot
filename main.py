from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# GEMINI API SETUP
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"  # <-- Yahan apni API Key paste karein
client = genai.Client(api_key=GEMINI_API_KEY)

NAHEED_KNOWLEDGE = """
System Role: Tum 'Naheed.pk' ke official 24/7 AI Customer Sales & Support Agent ho.

Knowledge Base:
1. Brand: Naheed.pk Pakistan's premier online department store.
2. Delivery Timings: Karachi Express Delivery 24 Hours. Nationwide Delivery 1-3 Business Days.
3. Shipping Charges: Standard Karachi Shipping Rs. 150. Free Delivery on orders above Rs. 4,000.
4. Payment Methods: Cash on Delivery (COD), Cards, JazzCash, EasyPaisa.
5. Return Policy: 7-Day easy hassle-free return or replacement.
6. Support: Phone: (021) 111-624-333 | Email: support@naheed.pk

Rules:
- Reply in polite, precise Roman Urdu or English.
- Keep answers under 2-3 concise sentences.
"""

class ChatInput(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "Naheed.pk AI Server is Active"}

@app.post("/api/chat")
def chat_with_naheed_ai(data: ChatInput):
    try:
        full_prompt = f"{NAHEED_KNOWLEDGE}\n\nUser Question: {data.message}\nNaheed AI Response:"
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )
        return {"reply": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))