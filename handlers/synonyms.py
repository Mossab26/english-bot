from telegram import Update
from telegram.ext import ContextTypes
from utils import ask_gemini

async def handle_synonyms_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """يعطي مرادفات وأضداد للكلمة المرسلة"""
    word = update.message.text.strip()

    prompt = f"""
الكلمة: "{word}"

أعطني:
1) من 5 إلى 8 مرادفات لهذه الكلمة
2) من 3 إلى 5 أضداد لهذه الكلمة

إذا كانت الكلمة إنجليزية: أعطني المرادفات والأضداد بالإنجليزية مع ترجمة عربية موجزة لكل واحدة.
إذا كانت الكلمة عربية: أعطني المرادفات والأضداد بالفصحى.

أجب بهذا التنسيق بالضبط:
🔤 المرادفات:
<قائمة مرقمة>

↔️ الأضداد:
<قائمة مرقمة>
"""
    result = ask_gemini(prompt)
    await update.message.reply_text(f"📘 \"{word}\":\n\n{result}")