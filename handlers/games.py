import re
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils import ask_gemini

async def send_new_question(update, context: ContextTypes.DEFAULT_TYPE, chat_id):
    """يولد سؤال ملء فراغ جديد"""
    prompt = """
Generate one English fill-in-the-blank exercise for language learners.
Return ONLY valid JSON, no extra text, exactly like this:
{"sentence": "I ___ to school every day.", "options": ["go", "goes", "going"], "answer": "go"}
"""
    raw = ask_gemini(prompt)
    try:
        cleaned = re.sub(r"```json|```", "", raw).strip()
        data = json.loads(cleaned)
    except Exception:
        await context.bot.send_message(chat_id=chat_id, text="حدث خطأ فتوليد السؤال، حاول مرة أخرى.")
        return

    context.user_data['game_answer'] = data['answer']
    buttons = [[InlineKeyboardButton(opt, callback_data=f"game_answer:{opt}")] for opt in data['options']]
    buttons.append([InlineKeyboardButton("🔄 سؤال جديد", callback_data="game_new")])

    await context.bot.send_message(
        chat_id=chat_id,
        text=f"املأ الفراغ:\n\n{data['sentence']}",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def handle_game_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chosen = query.data.split(":")[1]
    correct = context.user_data.get('game_answer')

    if chosen == correct:
        await query.edit_message_text(f"✅ إجابة صحيحة! الكلمة: {correct}")
    else:
        await query.edit_message_text(f"❌ خاطئة. الإجابة الصحيحة: {correct}")

    await send_new_question(update, context, query.message.chat_id)