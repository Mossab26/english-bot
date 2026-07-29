from telegram import Update
from telegram.ext import ContextTypes
from utils import ask_gemini

async def handle_synonyms_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """يعطي مرادفات للكلمة المرسلة"""
    word = update.message.text.strip()

    prompt = f"""
أعطني من 5 إلى 8 مرادفات للكلمة التالية: "{word}"
إذا كانت الكلمة إنجليزية: أعطني المرادفات بالإنجليزية مع ترجمة عربية موجزة لكل واحدة.
إذا كانت الكلمة عربية: أعطني المرادفات بالفصحى.
أجب بقائمة مرقمة بسيطة فقط، بلا أي مقدمة أو شرح زائد.
"""
    result = ask_gemini(prompt)
    await update.message.reply_text(f"🔤 مرادفات \"{word}\":\n\n{result}")