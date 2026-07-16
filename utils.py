import os
from groq import Groq
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

MODEL = "llama-3.3-70b-versatile"

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, min=2, max=20), reraise=True)
def _call_groq(prompt: str):
    return client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

def ask_gemini(prompt: str) -> str:
    """يرسل طلب للنموذج ويرجع النص فقط (خلينا نفس اسم الدالة باش ما نبدلوش باقي الملفات)"""
    try:
        response = _call_groq(prompt)
        return response.choices[0].message.content.strip()
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "rate" in error_msg.lower():
            return "⏳ الخدمة مزحومة حاليا، حاول بعد شوية."
        return f"حدث خطأ: {e}"