import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# إعداد قاعدة البيانات
def setup_database():
    conn = sqlite3.connect('language_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tips (
            id INTEGER PRIMARY KEY,
            tip TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rules (
            id INTEGER PRIMARY KEY,
            rule TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY,
            resource_type TEXT NOT NULL,
            file_path TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# إضافة نصيحة
def add_tip(tip: str):
    conn = sqlite3.connect('language_bot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tips (tip) VALUES (?)', (tip,))
    conn.commit()
    conn.close()

# إضافة قاعدة
def add_rule(rule: str):
    conn = sqlite3.connect('language_bot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO rules (rule) VALUES (?)', (rule,))
    conn.commit()
    conn.close()

# إضافة مورد (ملف)
def add_resource(resource_type: str, file_path: str):
    conn = sqlite3.connect('language_bot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO resources (resource_type, file_path) VALUES (?, ?)', (resource_type, file_path))
    conn.commit()
    conn.close()

# دالة بدء المحادثة
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('أهلاً بك في بوت معهد اللغة الإنجليزية! استخدم الأوامر التالية:\n'
                              '/add_tip - لإضافة نصيحة\n'
                              '/add_rule - لإضافة قاعدة\n'
                              '/add_resource - لإضافة ملف PDF أو صوت أو فيديو\n'
                              '/tips - لعرض النصائح\n'
                              '/rules - لعرض القواعد\n'
                              '/resources - لعرض الموارد\n'
                              '/join_group - للانضمام إلى مجموعة واتساب\n'
                              '/collocations [كلمة] - عرض تعبيرات شائعة\n'
                              '/study_plan - تقديم خطة دراسية\n'
                              '/common_mistakes - عرض أخطاء شائعة\n'
                              '/language_resources - مشاركة موارد تعليمية\n'
                              '/conversation_starters - اقتراح مواضيع للنقاش\n'
                              '/grammar_exercises - تقديم تمارين نحوية\n'
                              '/cultural_facts - مشاركة حقائق ثقافية\n'
                              '/listening_exercises - تقديم تمارين استماع\n'
                              '/writing_tips - نصائح للكتابة\n'
                              '/idiomatic_expressions - عرض تعبيرات اصطلاحية\n'
                              '/language_exchange - اقتراح شريك لتبادل اللغات\n'
                              '/study_groups - معلومات حول مجموعات الدراسة\n'
                              '/news - مشاركة أخبار قصيرة\n'
                              '/language_jokes - نكات بسيطة\n'
                              '/progress_check - تقييم تقدمك.')

# دالة إضافة نصيحة
def add_tip_command(update: Update, context: CallbackContext) -> None:
    tip = ' '.join(context.args)
    if tip:
        add_tip(tip)
        update.message.reply_text('تم إضافة النصيحة بنجاح!')
    else:
        update.message.reply_text('يرجى إرسال النصيحة بعد الأمر.')

# دالة إضافة قاعدة
def add_rule_command(update: Update, context: CallbackContext) -> None:
    rule = ' '.join(context.args)
    if rule:
        add_rule(rule)
        update.message.reply_text('تم إضافة القاعدة بنجاح!')
    else:
        update.message.reply_text('يرجى إرسال القاعدة بعد الأمر.')

# دالة إضافة مورد
def add_resource_command(update: Update, context: CallbackContext) -> None:
    resource_type = context.args[0] if context.args else None
    if resource_type in ['pdf', 'audio', 'video']:
        update.message.reply_text('يرجى إرسال الملف الآن.')
        context.user_data['resource_type'] = resource_type
    else:
        update.message.reply_text('يرجى تحديد نوع المورد (pdf, audio, video).')

def handle_document(update: Update, context: CallbackContext) -> None:
    resource_type = context.user_data.get('resource_type')
    if resource_type:
        file = update.message.document
        file_path = f'./resources/{file.file_name}'
        file.download(file_path)
        add_resource(resource_type, file_path)
        update.message.reply_text('تم إضافة المورد بنجاح!')
        del context.user_data['resource_type']
    else:
        update.message.reply_text('يرجى استخدام الأمر /add_resource لتحديد نوع المورد أولاً.')

# دالة إرسال النصائح
def send_tips(update: Update, context: CallbackContext) -> None:
    conn = sqlite3.connect('language_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT tip FROM tips')
    tips = cursor.fetchall()
    if tips:
        tip_message = "\n".join([tip[0] for tip in tips])
        update.message.reply_text(tip_message)
    else:
        update.message.reply_text('لا توجد نصائح متاحة حالياً.')
    conn.close()

# دالة إرسال القواعد
def send_rules(update: Update, context: CallbackContext) -> None:
    conn = sqlite3.connect('language_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT rule FROM rules')
    rules = cursor.fetchall()
    if rules:
        rule_message = "\n".join([rule[0] for rule in rules])
        update.message.reply_text(rule_message)
    else:
        update.message.reply_text('لا توجد قواعد متاحة حالياً.')
    conn.close()

# دالة إرسال الموارد
def send_resources(update: Update, context: CallbackContext) -> None:
    conn = sqlite3.connect('language_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT resource_type, file_path FROM resources')
    resources = cursor.fetchall()
    if resources:
        resource_message = "\n".join([f"{res[0]}: {res[1]}" for res in resources])
        update.message.reply_text(resource_message)
    else:
        update.message.reply_text('لا توجد موارد متاحة حالياً.')
    conn.close()

# دالة زر الانضمام إلى مجموعة واتساب
def group_link(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("انضم إلى مجموعة واتساب", url="رابط_المجموعة")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('للانضمام إلى مجموعة واتساب، اضغط على الزر أدناه:', reply_markup=reply_markup)

# دالة عرض التعبيرات الشائعة
def collocations(update: Update, context: CallbackContext) -> None:
    word = ' '.join(context.args)
    if word:
        collocation_message = f"تعبيرات شائعة مرتبطة بـ '{word}': [مثال هنا]"
        update.message.reply_text(collocation_message)
    else:
        update.message.reply_text('يرجى إدخال كلمة للبحث عن التعبيرات الشائعة.')

# دالة تقديم خطة دراسية
def study_plan(update: Update, context: CallbackContext) -> None:
    plan = "خطة دراسية مقترحة:\n1. قراءة لمدة 30 دقيقة يومياً.\n2. ممارسة المحادثة مرتين في الأسبوع.\n3. كتابة مقال أسبوعي."
    update.message.reply_text(plan)

# دالة عرض الأخطاء الشائعة
def common_mistakes(update: Update, context: CallbackContext) -> None:
    mistakes = "أخطاء شائعة:\n1. استخدام 'is' بدلاً من 'are'.\n2. نسيان استخدام 's' في الجمع."
    update.message.reply_text(mistakes)

# دالة مشاركة موارد تعليمية
def language_resources(update: Update, context: CallbackContext) -> None:
    resources = "موارد تعليمية:\n1. تطبيق Duolingo\n2. موقع BBC Learning English"
    update.message.reply_text(resources)

# دالة اقتراح مواضيع للنقاش
def conversation_starters(update: Update, context: CallbackContext) -> None:
    topics = "مواضيع للنقاش:\n1. ما هو كتابك المفضل؟\n2. تحدث عن تجربة سفر ممتعة."
    update.message.reply_text(topics)

# دالة تقديم تمارين نحوية
def grammar_exercises(update: Update, context: CallbackContext) -> None:
    exercises = "تمارين نحوية:\n1. أكمل الجمل التالية...\n2. صحح الأخطاء في النص."
    update.message.reply_text(exercises)

# دالة مشاركة حقائق ثقافية
def cultural_facts(update: Update, context: CallbackContext) -> None:
    facts = "حقائق ثقافية:\n1. اللغة الإنجليزية هي اللغة الرسمية في 58 دولة."
    update.message.reply_text(facts)

# دالة تقديم تمارين استماع
def listening_exercises(update: Update, context: CallbackContext) -> None:
    exercises = "تمارين استماع:\nاستمع إلى هذا المقطع [رابط] وأجب عن الأسئلة."
    update.message.reply_text(exercises)

# دالة تقديم نصائح للكتابة
def writing_tips(update: Update, context: CallbackContext) -> None:
    tips = "نصائح للكتابة:\n1. اكتب بوضوح وبساطة.\n2. استخدم جمل قصيرة."
    update.message.reply_text(tips)

# دالة عرض تعبيرات اصطلاحية
def idiomatic_expressions(update: Update, context: CallbackContext) -> None:
    expressions = "تعبيرات اصطلاحية:\n1. 'Break the ice' تعني كسر الجليد.\n2. 'Piece of cake' تعني سهل جداً."
    update.message.reply_text(expressions)

# دالة اقتراح شريك لتبادل اللغات
def language_exchange(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('يمكنك العثور على شريك لتبادل اللغات عبر منصات مثل Tandem أو HelloTalk.')

# دالة معلومات حول مجموعات الدراسة
def study_groups(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('توجد مجموعات دراسة عبر الإنترنت يمكنك الانضمام إليها، تحقق من الفيسبوك أو المنصات التعليمية.')

# دالة مشاركة أخبار قصيرة
def news(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('أحدث الأخبار: [رابط الأخبار].')

# دالة مشاركة نكات بسيطة
def language_jokes(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('نكتة: لماذا لم يعبر الكتاب الشارع؟ لأنه كان خائفاً من أن يحصل على "فكرة خاطئة"!')

# دالة تقييم تقدم الطلاب
def progress_check(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('كيف تقيّم تقدمك في تعلم اللغة؟ [استبيان بسيط هنا].')

# إنشاء البوت
def main():
    setup_database()
    updater = Updater("7717188841:AAFwAGIfcsgcem0fx678cSUK6faKmNUuVWM")

    # إضافة المعالجات
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("add_tip", add_tip_command))
    updater.dispatcher.add_handler(CommandHandler("add_rule", add_rule_command))
    updater.dispatcher.add_handler(CommandHandler("add_resource", add_resource_command))
    updater.dispatcher.add_handler(CommandHandler("tips", send_tips))
    updater.dispatcher.add_handler(CommandHandler("rules", send_rules))
    updater.dispatcher.add_handler(CommandHandler("resources", send_resources))
    updater.dispatcher.add_handler(CommandHandler("join_group", group_link))
    updater.dispatcher.add_handler(CommandHandler("collocations", collocations))
    updater.dispatcher.add_handler(CommandHandler("study_plan", study_plan))
    updater.dispatcher.add_handler(CommandHandler("common_mistakes", common_mistakes))
    updater.dispatcher.add_handler(CommandHandler("language_resources", language_resources))
    updater.dispatcher.add_handler(CommandHandler("conversation_starters", conversation_starters))
    updater.dispatcher.add_handler(CommandHandler("grammar_exercises", grammar_exercises))
    updater.dispatcher.add_handler(CommandHandler("cultural_facts", cultural_facts))
    updater.dispatcher.add_handler(CommandHandler("listening_exercises", listening_exercises))
    updater.dispatcher.add_handler(CommandHandler("writing_tips", writing_tips))
    updater.dispatcher.add_handler(CommandHandler("idiomatic_expressions", idiomatic_expressions))
    updater.dispatcher.add_handler(CommandHandler("language_exchange", language_exchange))
    updater.dispatcher.add_handler(CommandHandler("study_groups", study_groups))
    updater.dispatcher.add_handler(CommandHandler("news", news))
    updater.dispatcher.add_handler(CommandHandler("language_jokes", language_jokes))
    updater.dispatcher.add_handler(CommandHandler("progress_check", progress_check))
    updater.dispatcher.add_handler(MessageHandler(Filters.document, handle_document))

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
