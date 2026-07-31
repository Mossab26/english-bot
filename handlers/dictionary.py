import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils import ask_gemini

DICT_FILE = "user_dictionaries.json"

def _load_all():
    if not os.path.exists(DICT_FILE):
        return {}
    try:
        with open(DICT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _save_all(data):
    with open(DICT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

async def show_dictionary_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    buttons = [
        [InlineKeyboardButton("➕ إضافة كلمة", callback_data="dict_add")],
        [InlineKeyboardButton("📋 عرض قاموسي", callback_data="dict_view")],
        [InlineKeyboardButton("🗑️ حذف كلمة", callback_data="dict_delete")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")],
    ]
    await query.edit_message_text(
        "📔 قاموسي الشخصي\nهنا يمكنك حفظ الكلمات الجديدة التي تتعلمها.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def activate_dict_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['mode'] = 'dict_add'
    await query.edit_message_text("✍️ أرسل الكلمة التي تريد إضافتها إلى قاموسك (عربية أو إنجليزية).")

async def activate_dict_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['mode'] = 'dict_delete'
    await query.edit_message_text("🗑️ أرسل الكلمة التي تريد حذفها من قاموسك.")

async def handle_dict_add_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    word = update.message.text.strip()

    prompt = f"""أعطني ترجمة مختصرة فقط بلا أي شرح إضافي للكلمة التالية:
- إذا كانت إنجليزية، أعطني ترجمتها للعربية الفصحى.
- إذا كانت عربية، أعطني ترجمتها للإنجليزية.
الكلمة: {word}
أجب بالترجمة فقط، كلمة أو عبارة قصيرة."""

    translation = ask_gemini(prompt)

    data = _load_all()
    user_words = data.get(user_id, [])

    if not any(w['word'].lower() == word.lower() for w in user_words):
        user_words.append({"word": word, "translation": translation})
        data[user_id] = user_words
        _save_all(data)
        await update.message.reply_text(f"✅ تمت إضافة \"{word}\" ({translation}) إلى قاموسك.")
    else:
        await update.message.reply_text(f"ℹ️ الكلمة \"{word}\" موجودة بالفعل في قاموسك.")

async def handle_dict_delete_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    word = update.message.text.strip()

    data = _load_all()
    user_words = data.get(user_id, [])
    new_words = [w for w in user_words if w['word'].lower() != word.lower()]

    if len(new_words) < len(user_words):
        data[user_id] = new_words
        _save_all(data)
        await update.message.reply_text(f"🗑️ تم حذف \"{word}\" من قاموسك.")
    else:
        await update.message.reply_text(f"⚠️ لم أجد \"{word}\" في قاموسك.")

async def show_dictionary_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = str(update.effective_user.id)
    data = _load_all()
    user_words = data.get(user_id, [])

    if not user_words:
        text = "📔 قاموسك فارغ حاليًا.\nاضغط على \"➕ إضافة كلمة\" لتبدأ."
    else:
        lines = [f"{i+1}. {w['word']} — {w['translation']}" for i, w in enumerate(user_words)]
        text = "📔 قاموسك الشخصي:\n\n" + "\n".join(lines)

    buttons = [[InlineKeyboardButton("🔙 رجوع", callback_data="mode_dictionary")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(buttons))