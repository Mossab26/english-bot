from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# قائمة المواضيع فقط، بدون محتوى - سيتم إضافة الشرح لاحقا عبر الصور
GRAMMAR_TOPICS = {
    "tenses": {"title": "الأزمنة (Tenses)"},
    "plural": {"title": "الجمع (Plurals)"},
    "adjectives": {"title": "الصفات (Adjectives)"},
    "prepositions": {"title": "حروف الجر (Prepositions)"},
}

async def show_grammar_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    buttons = [
        [InlineKeyboardButton(t["title"], callback_data=f"grammar_topic:{k}")]
        for k, t in GRAMMAR_TOPICS.items()
    ]
    buttons.append([InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")])
    await query.edit_message_text("📖 اختر الموضوع الذي ترغب في مراجعته:", reply_markup=InlineKeyboardMarkup(buttons))

async def show_grammar_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    key = query.data.split(":")[1]
    topic = GRAMMAR_TOPICS[key]
    buttons = [[InlineKeyboardButton("🔙 رجوع للقائمة", callback_data="grammar_menu")]]
    # سيتم إرسال الشرح لاحقا في صورة من طرف الإدارة
    await query.edit_message_text(
        f"🌿 {topic['title']}\n\nسيُضاف الشرح قريبًا 🌱",
        reply_markup=InlineKeyboardMarkup(buttons)
    )