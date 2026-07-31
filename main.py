import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)

from handlers.translation import handle_translation_text
from handlers.chat import handle_chat_text
from handlers.grammar import show_grammar_menu, show_grammar_topic, GRAMMAR_TOPICS
from handlers.games import send_new_question, handle_game_answer
from handlers.reading import send_reading_text
from handlers.synonyms import handle_synonyms_text
from handlers.shadowing import handle_shadowing_text
from handlers.dictionary import (
    show_dictionary_menu, activate_dict_add, activate_dict_delete,
    handle_dict_add_text, handle_dict_delete_text, show_dictionary_list
)

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

WELCOME_MESSAGE = (
    "🌿🍃🌱 مرحبًا بكم في بوت الهابينست لتعلم اللغة الإنجليزية 🌱🍃🌿\n\n"
    "✨ بوت من إعداد: ياسر\n"
    "💚 شكر خاص لنادي كيمياء السعادة\n\n"
    "اختر القسم الذي ترغب فيه من الأزرار أدناه 👇"
)

def main_menu_buttons():
    return [
        [InlineKeyboardButton("🌍 الترجمة", callback_data="mode_translation")],
        [InlineKeyboardButton("📖 القواعد", callback_data="grammar_menu")],
        [InlineKeyboardButton("💬 الدردشة مع AI", callback_data="mode_chat")],
        [InlineKeyboardButton("🎮 الألعاب", callback_data="game_new")],
        [InlineKeyboardButton("📚 نصوص للقراءة", callback_data="reading_menu")],
        [InlineKeyboardButton("🔤 المرادفات والأضداد", callback_data="mode_synonyms")],
        [InlineKeyboardButton("🎧 Shadowing (تكرار النطق)", callback_data="mode_shadowing")],
        [InlineKeyboardButton("📔 قاموسي", callback_data="mode_dictionary")],
    ]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['mode'] = None
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=InlineKeyboardMarkup(main_menu_buttons()))

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['mode'] = None
    await query.edit_message_text("اختر القسم الذي ترغب فيه:", reply_markup=InlineKeyboardMarkup(main_menu_buttons()))

async def activate_translation_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['mode'] = 'translation'
    await query.edit_message_text("✍️ أرسل النص الذي ترغب في ترجمته (عربي أو إنجليزي).")

async def activate_chat_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['mode'] = 'chat'
    await query.edit_message_text("💬 اكتب أي جملة بالإنجليزية وسنتحدث معك ونصحح أخطاءك.")

async def activate_synonyms_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['mode'] = 'synonyms'
    await query.edit_message_text("🔤 أرسل الكلمة التي تريد معرفة مرادفاتها وأضدادها.")

async def activate_shadowing_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['mode'] = 'shadowing'
    await query.edit_message_text("🎧 أرسل نصًا إنجليزيًا (حتى 3000 حرف تقريبًا) وسأحوله إلى صوت.")

async def show_reading_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    buttons = [
        [InlineKeyboardButton("🟢 مبتدئ", callback_data="reading_level:beginner")],
        [InlineKeyboardButton("🟡 متوسط", callback_data="reading_level:intermediate")],
        [InlineKeyboardButton("🔴 متقدم", callback_data="reading_level:advanced")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")],
    ]
    await query.edit_message_text("📚 اختر مستواك:", reply_markup=InlineKeyboardMarkup(buttons))

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get('mode')
    if mode == 'translation':
        await handle_translation_text(update, context)
    elif mode == 'chat':
        await handle_chat_text(update, context)
    elif mode == 'synonyms':
        await handle_synonyms_text(update, context)
    elif mode == 'shadowing':
        await handle_shadowing_text(update, context)
    elif mode == 'dict_add':
        await handle_dict_add_text(update, context)
    elif mode == 'dict_delete':
        await handle_dict_delete_text(update, context)
    else:
        await update.message.reply_text("الرجاء استخدام الأمر /start واختيار قسم أولًا 🌿")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data

    if data == "main_menu":
        await show_main_menu(update, context)
    elif data == "mode_translation":
        await activate_translation_mode(update, context)
    elif data == "mode_chat":
        await activate_chat_mode(update, context)
    elif data == "mode_synonyms":
        await activate_synonyms_mode(update, context)
    elif data == "mode_shadowing":
        await activate_shadowing_mode(update, context)
    elif data == "mode_dictionary":
        await show_dictionary_menu(update, context)
    elif data == "dict_add":
        await activate_dict_add(update, context)
    elif data == "dict_delete":
        await activate_dict_delete(update, context)
    elif data == "dict_view":
        await show_dictionary_list(update, context)
    elif data == "grammar_menu":
        await show_grammar_menu(update, context)
    elif data.startswith("grammar_topic:"):
        await show_grammar_topic(update, context)
    elif data == "game_new":
        await update.callback_query.answer()
        await send_new_question(update, context, update.callback_query.message.chat_id)
    elif data.startswith("game_answer:"):
        await handle_game_answer(update, context)
    elif data == "reading_menu":
        await show_reading_menu(update, context)
    elif data.startswith("reading_level:"):
        level = data.split(":")[1]
        await send_reading_text(update, context, level)

# ------- أوامر تظهر في المربع الأزرق -------
async def cmd_translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['mode'] = 'translation'
    await update.message.reply_text("✍️ أرسل النص الذي ترغب في ترجمته (عربي أو إنجليزي).")

async def cmd_grammar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    items = list(GRAMMAR_TOPICS.items())
    buttons = []
    for i in range(0, len(items), 2):
        row = [InlineKeyboardButton(items[i][1]["title"], callback_data=f"grammar_topic:{items[i][0]}")]
        if i + 1 < len(items):
            row.append(InlineKeyboardButton(items[i+1][1]["title"], callback_data=f"grammar_topic:{items[i+1][0]}"))
        buttons.append(row)
    await update.message.reply_text("📖 اختر المستوى الذي ترغب في مراجعته:", reply_markup=InlineKeyboardMarkup(buttons))

async def cmd_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['mode'] = 'chat'
    await update.message.reply_text("💬 اكتب أي جملة بالإنجليزية وسنتحدث معك ونصحح أخطاءك.")

async def cmd_games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_new_question(update, context, update.message.chat_id)

async def cmd_reading(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("🟢 مبتدئ", callback_data="reading_level:beginner")],
        [InlineKeyboardButton("🟡 متوسط", callback_data="reading_level:intermediate")],
        [InlineKeyboardButton("🔴 متقدم", callback_data="reading_level:advanced")],
    ]
    await update.message.reply_text("📚 اختر مستواك:", reply_markup=InlineKeyboardMarkup(buttons))

async def cmd_synonyms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['mode'] = 'synonyms'
    await update.message.reply_text("🔤 أرسل الكلمة التي تريد معرفة مرادفاتها وأضدادها.")

async def cmd_shadowing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['mode'] = 'shadowing'
    await update.message.reply_text("🎧 أرسل نصًا إنجليزيًا (حتى 3000 حرف) وسأحوله إلى صوت.")

async def cmd_dictionary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("➕ إضافة كلمة", callback_data="dict_add")],
        [InlineKeyboardButton("📋 عرض قاموسي", callback_data="dict_view")],
        [InlineKeyboardButton("🗑️ حذف كلمة", callback_data="dict_delete")],
    ]
    await update.message.reply_text("📔 قاموسي الشخصي:", reply_markup=InlineKeyboardMarkup(buttons))

async def post_init(application: Application):
    commands = [
        BotCommand("start", "🌿 القائمة الرئيسية"),
        BotCommand("translate", "🌍 الترجمة"),
        BotCommand("grammar", "📖 القواعد"),
        BotCommand("chat", "💬 الدردشة مع AI"),
        BotCommand("games", "🎮 الألعاب"),
        BotCommand("reading", "📚 نصوص للقراءة"),
        BotCommand("synonyms", "🔤 المرادفات والأضداد"),
        BotCommand("shadowing", "🎧 Shadowing"),
        BotCommand("dictionary", "📔 قاموسي"),
    ]
    await application.bot.set_my_commands(commands)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("translate", cmd_translate))
    app.add_handler(CommandHandler("grammar", cmd_grammar))
    app.add_handler(CommandHandler("chat", cmd_chat))
    app.add_handler(CommandHandler("games", cmd_games))
    app.add_handler(CommandHandler("reading", cmd_reading))
    app.add_handler(CommandHandler("synonyms", cmd_synonyms))
    app.add_handler(CommandHandler("shadowing", cmd_shadowing))
    app.add_handler(CommandHandler("dictionary", cmd_dictionary))

    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("البوت شغال... اضغط Ctrl+C للتوقف")
    app.run_polling()

if __name__ == "__main__":
    main()