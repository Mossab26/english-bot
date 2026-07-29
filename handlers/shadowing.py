import os
import tempfile
from gtts import gTTS
from telegram import Update
from telegram.ext import ContextTypes

async def handle_shadowing_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """يحول النص الإنجليزي المرسل إلى ملف صوتي للتدرب على النطق"""
    text = update.message.text.strip()

    if len(text) > 500:
        await update.message.reply_text("⚠️ الرجاء إرسال نص أقصر (500 حرف كحد أقصى).")
        return

    await update.message.reply_text("🎧 جارٍ تحويل النص إلى صوت...")

    try:
        tts = gTTS(text=text, lang='en')
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            tts.save(tmp_file.name)
            tmp_path = tmp_file.name

        with open(tmp_path, "rb") as audio_file:
            await update.message.reply_audio(audio_file, title="Shadowing Practice")

        os.remove(tmp_path)
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ أثناء تحويل النص إلى صوت: {e}")