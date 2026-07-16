from telegram import Update
from telegram.ext import ContextTypes
from utils import ask_gemini

async def send_reading_text(update: Update, context: ContextTypes.DEFAULT_TYPE, level: str):
    query = update.callback_query
    await query.answer()

    level_map = {
        "beginner": "beginner (A1-A2)",
        "intermediate": "intermediate (B1-B2)",
        "advanced": "advanced (C1-C2)"
    }

    prompt = f"""
Write a short English reading passage (3-5 sentences) for a {level_map[level]} learner.
Then list 3 difficult words from the text with Arabic translation.

Format:
📖 النص:
<passage>

📌 كلمات صعبة:
- word: ترجمة
- word: ترجمة
- word: ترجمة
"""
    text = ask_gemini(prompt)
    await query.edit_message_text(text)