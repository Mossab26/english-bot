from telegram import Update
from telegram.ext import ContextTypes
from utils import ask_gemini

async def handle_chat_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """محادثة حرة مع تصحيح الأخطاء"""
    text = update.message.text
    prompt = f"""
You are an English conversation partner and teacher.
The student wrote: "{text}"

1. Reply naturally in English (2-3 sentences max).
2. If there are grammar/vocabulary mistakes, list them with corrections and a brief explanation in Arabic. If none, say "لا توجد أخطاء ✅".

Format exactly like this:
💬 الرد:
<reply in English>

✏️ التصحيح:
<corrections in Arabic, or "لا توجد أخطاء ✅">
"""
    reply = ask_gemini(prompt)
    await update.message.reply_text(reply)