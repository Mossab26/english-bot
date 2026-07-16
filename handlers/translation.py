from telegram import Update
from telegram.ext import ContextTypes
from utils import ask_gemini

def is_arabic(text: str) -> bool:
    """يكتشف إذا كان النص فيه حروف عربية"""
    return any('\u0600' <= ch <= '\u06FF' for ch in text)

async def handle_translation_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """يترجم النص المرسل حسب لغته"""
    text = update.message.text
    if is_arabic(text):
        prompt = f"ترجم النص التالي من العربية إلى الإنجليزية، أعطني الترجمة فقط بدون شرح:\n{text}"
    else:
        prompt = f"Translate the following text from English to Arabic, give only the translation:\n{text}"

    translation = ask_gemini(prompt)
    await update.message.reply_text(f"📝 الترجمة:\n{translation}")