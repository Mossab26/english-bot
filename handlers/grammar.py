from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

GRAMMAR_TOPICS = {
    "l1": {
        "title": "١. أساسيات الكلام",
        "content": (
            "🔤 أقسام الكلام الأساسية:\n\n"
            "1️⃣ Noun (اسم): يسمي شخصًا أو مكانًا أو شيئًا أو فكرة\nمثال: John, Paris, Table, Happiness\n\n"
            "2️⃣ Pronoun (ضمير): يحل محل الاسم\nمثال: He, She, It, They, Who\n\n"
            "3️⃣ Verb (فعل): يدل على حدث أو حالة\nمثال: Run, Eat, Is, Have, Think\n\n"
            "4️⃣ Adjective (صفة): تصف الاسم\nمثال: Big, Red, Smart, Beautiful\n\n"
            "5️⃣ Adverb (ظرف): يصف الفعل أو الصفة أو ظرفًا آخر\nمثال: Quickly, Very, Well, Too\n\n"
            "6️⃣ Preposition (حرف جر): يبين العلاقة (زمان/مكان/اتجاه)\nمثال: In, On, At, Under, By\n\n"
            "7️⃣ Conjunction (أداة ربط): تربط بين الكلمات أو الجمل\nمثال: And, But, Or, Because, Although\n\n"
            "8️⃣ Interjection (كلمة تعجب): تعبر عن انفعال مفاجئ\nمثال: Wow! Oh! Ouch!"
        )
    },
    "l2": {
        "title": "٢. الأزمنة",
        "content": (
            "⏰ أزمنة المضارع:\n"
            "• Simple Present: حقائق وعادات → I work. / She works.\n"
            "• Present Continuous: حدث الآن أو خطط مستقبلية → I am working now.\n"
            "• Present Perfect: فعل ماضٍ له أثر في الحاضر → I have worked here for 5 years.\n"
            "• Present Perfect Continuous: بدأ في الماضي ومستمر → I have been working all day.\n\n"
            "🕰️ أزمنة الماضي:\n"
            "• Simple Past: فعل مكتمل في وقت محدد → I worked yesterday.\n"
            "• Past Continuous: فعل مستمر قاطعه فعل آخر → I was working when you called.\n"
            "• Past Perfect: فعل تم قبل فعل ماضٍ آخر → I had worked before he arrived.\n"
            "• Past Perfect Continuous: مستمر حتى لحظة ماضية أخرى → I had been working for 2 hours when he came.\n\n"
            "🔮 أزمنة المستقبل:\n"
            "• Simple Future: قرار عفوي أو توقع → I will work tomorrow.\n"
            "• Future Continuous: مستمر في وقت مستقبلي محدد → I will be working at 8 PM.\n"
            "• Future Perfect: سيكتمل قبل وقت مستقبلي محدد → I will have worked by 6 PM.\n"
            "• Future Perfect Continuous: مستمر حتى لحظة مستقبلية → I will have been working for 10 hours by noon."
        )
    },
    "l3": {
        "title": "٣. الأفعال المساعدة والناقصة",
        "content": (
            "🛠️ Auxiliary Verbs: تساعد في تكوين الأزمنة والأسئلة والنفي\nمثال: Be, Do, Have → I am working. Do you like it?\n\n"
            "🔑 Modal Verbs: تعبر عن الإمكانية، الضرورة، القدرة، أو التأدب\nمثال: Can, Could, May, Might, Must, Should, Will, Would\n\n"
            "📌 قواعد مهمة:\n"
            "• Must = التزام داخلي (I must study.)\n"
            "• Have to = التزام خارجي (You have to wear a uniform.)\n"
            "• Should = نصيحة (You should see a doctor.)\n"
            "• May/Might = احتمال ضعيف (It might rain.)\n"
            "• Can = قدرة أو إذن (I can swim.)"
        )
    },
    "l4": {
        "title": "٤. المبني للمعلوم والمجهول",
        "content": (
            "📐 قاعدة تكوين المبني للمجهول:\nBE (في أي زمن) + Past Participle\n\n"
            "• Active (فاعل يقوم بالفعل): The chef cooks the food.\n"
            "• Passive (الفاعل يستقبل الفعل): The food is cooked by the chef."
        )
    },
    "l5": {
        "title": "٥. الجمل الشرطية",
        "content": (
            "0️⃣ Zero Conditional: حقائق علمية عامة\nIf + Present, Present → If you heat ice, it melts.\n\n"
            "1️⃣ First Conditional: احتمال حقيقي مستقبلي\nIf + Present, Will + Infinitive → If it rains, I will stay home.\n\n"
            "2️⃣ Second Conditional: افتراض غير واقعي بالحاضر\nIf + Past, Would + Infinitive → If I were you, I would go.\n\n"
            "3️⃣ Third Conditional: ندم على الماضي\nIf + Past Perfect, Would have + V3 → If I had studied, I would have passed."
        )
    },
    "l6": {
        "title": "٦. الكلام المنقول",
        "content": (
            "🔁 قاعدة التحول عند نقل الكلام:\n\n"
            "• Simple Present → Simple Past: \"I eat pizza.\" → He said he ate pizza.\n"
            "• Present Continuous → Past Continuous: \"I am eating.\" → He said he was eating.\n"
            "• Simple Past → Past Perfect: \"I ate.\" → He said he had eaten.\n"
            "• Present Perfect → Past Perfect: \"I have eaten.\" → He said he had eaten.\n"
            "• Will → Would: \"I will eat.\" → He said he would eat."
        )
    },
    "l7": {
        "title": "٧. الأسماء والضمائر",
        "content": (
            "🔢 معدودة وغير معدودة:\n"
            "• Countable: Apple, Car, Book → تقبل a/an والجمع\n"
            "• Uncountable: Water, Rice, Information → مع some/any/much، بلا جمع\n\n"
            "📌 أدوات التعريف: a/an = غير محدد | the = محدد ومعروف\n\n"
            "👤 جدول الضمائر:\n"
            "I → me / my / mine / myself\n"
            "You → you / your / yours / yourself\n"
            "He → him / his / his / himself\n"
            "She → her / her / hers / herself\n"
            "It → it / its / its / itself\n"
            "We → us / our / ours / ourselves\n"
            "They → them / their / theirs / themselves"
        )
    },
    "l8": {
        "title": "٨. حروف الجر",
        "content": (
            "🕐 In: للأشهر والسنوات (in 2020) | لأماكن مغلقة (in the room)\n"
            "📅 On: للأيام والتواريخ (on Monday) | لسطح شيء (on the table)\n"
            "⏰ At: لوقت محدد (at 5 PM) | لنقطة محددة (at the door)"
        )
    },
    "l9": {
        "title": "٩. تركيب الجملة",
        "content": (
            "📏 القاعدة: S + V + O\nمثال: Ahmed (S) eats (V) an apple (O).\n\n"
            "📚 أنواع الجمل:\n"
            "• Simple: جملة مستقلة واحدة → I like coffee.\n"
            "• Compound: جملتان مرتبطتان بأداة ربط → I like coffee, but she likes tea.\n"
            "• Complex: مستقلة + تابعة → I drink coffee because I am tired.\n\n"
            "🔗 FANBOYS: For, And, Nor, But, Or, Yet, So"
        )
    },
    "l10": {
        "title": "١٠. صيغ الأسئلة",
        "content": (
            "✅ أسئلة نعم/لا: تبدأ بـ Be/Do/Have/Modal\nAre you happy? / Did you go? / Can you swim?\n\n"
            "❓ أسئلة Wh-: What, Where, When, Why, Who, Which, How\nالتركيب: Wh- + Auxiliary + Subject + Verb؟\nWhere do you live?\n\n"
            "🔁 أسئلة الذيل:\nمثبتة → ذيل منفي: You are tired, aren't you?\nمنفية → ذيل مثبت: You don't smoke, do you?"
        )
    },
    "l11": {
        "title": "١١. المقارنة والتفضيل",
        "content": (
            "• قصيرة (Tall): Taller (than) | The tallest\n"
            "• طويلة (Beautiful): More beautiful (than) | The most beautiful\n"
            "• شاذة (Good): Better (than) | The best"
        )
    },
    "l12": {
        "title": "١٢. الجمل الموصولة",
        "content": (
            "👤 Who: للأشخاص → The man who called you is my brother.\n"
            "📦 Which: للأشياء → The book which I read was great.\n"
            "🔄 That: للأشخاص أو الأشياء → The book that I read was great.\n\n"
            "📌 Defining: ضرورية، بلا فواصل | Non-Defining: إضافية، مع فواصل\nMy brother, who lives in London, is a doctor."
        )
    },
    "l13": {
        "title": "١٣. المصدر واسم الفاعل",
        "content": (
            "🔵 Gerund (V-ing): كاسم، بعد حروف الجر، بعد أفعال معينة\nI enjoy swimming. / She is good at dancing.\nأفعال تليها: Enjoy, Avoid, Finish, Mind, Suggest\n\n"
            "🟢 Infinitive (to + V1): للغرض، بعد أفعال معينة، كفاعل\nI want to go. / He came to help.\nأفعال تليها: Want, Decide, Hope, Plan, Agree"
        )
    },
    "l14": {
        "title": "١٤. أخطاء شائعة",
        "content": (
            "❌ He go to school. → ✅ He goes to school.\n"
            "❌ I am agree. → ✅ I agree.\n"
            "❌ She don't like it. → ✅ She doesn't like it.\n"
            "❌ I have 20 years old. → ✅ I am 20 years old.\n"
            "❌ He is more taller. → ✅ He is taller.\n"
            "❌ If I was you... → ✅ If I were you...\n\n"
            "💡 نصائح: تعلّم الأنماط، اقرأ بفعالية، اكتب 5 جمل يوميًا، تحدث بلا خوف، وتذكر قاعدة Backshift عند نقل الكلام."
        )
    },
}

async def show_grammar_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    items = list(GRAMMAR_TOPICS.items())
    buttons = []
    for i in range(0, len(items), 2):
        row = [InlineKeyboardButton(items[i][1]["title"], callback_data=f"grammar_topic:{items[i][0]}")]
        if i + 1 < len(items):
            row.append(InlineKeyboardButton(items[i+1][1]["title"], callback_data=f"grammar_topic:{items[i+1][0]}"))
        buttons.append(row)
    buttons.append([InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")])
    await query.edit_message_text("📖 اختر المستوى الذي ترغب في مراجعته:", reply_markup=InlineKeyboardMarkup(buttons))

async def show_grammar_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    key = query.data.split(":")[1]
    topic = GRAMMAR_TOPICS[key]
    buttons = [[InlineKeyboardButton("🔙 رجوع للقائمة", callback_data="grammar_menu")]]
    await query.edit_message_text(f"📖 {topic['title']}\n\n{topic['content']}", reply_markup=InlineKeyboardMarkup(buttons))