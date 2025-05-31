import os
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

# إضافة مورد
def add_resource(resource_type: str, file_path: str):
    conn = sqlite3.connect('language_bot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO resources (resource_type, file_path) VALUES (?, ?)', (resource_type, file_path))
    conn.commit()
    conn.close()

# عرض النصائح
def send_tips(update: Update, context: CallbackContext) -> None:
    conn = sqlite3.connect('language_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT tip FROM tips')
    tips = cursor.fetchall()
    conn.close()

    if tips:
        response = '\n\n'.join([tip[0] for tip in tips])
        update.message.reply_text(response)
    else:
        update.message.reply_text("لا توجد نصائح حالياً.")

# عرض القواعد
def send_rules(update: Update, context: CallbackContext) -> None:
    conn = sqlite3.connect('language_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT rule FROM rules')
    rules = cursor.fetchall()
    conn.close()

    if rules:
        response = '\n\n'.join([rule[0] for rule in rules])
        update.message.reply_text(response)
    else:
        update.message.reply_text("لا توجد قواعد حالياً.")

# عرض الموارد
def send_resources(update: Update, context: CallbackContext) -> None:
    conn = sqlite3.connect('language_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT resource_type, file_path FROM resources')
    resources = cursor.fetchall()
    conn.close()

    if resources:
        for resource in resources:
            if resource[1].endswith('.pdf'):
                update.message.reply_document(open(resource[1], 'rb'))
            elif resource[1].endswith(('.mp3', '.wav')):
                update.message.reply_audio(open(resource[1], 'rb'))
            elif resource[1].endswith(('.mp4', '.avi')):
                update.message.reply_video(open(resource[1], 'rb'))
    else:
        update.message.reply_text("لا توجد موارد حالياً.")

# تحميل الملفات المرسلة
def handle_document(update: Update, context: CallbackContext) -> None:
    file = update.message.document.get_file()
    file_path = os.path.join('downloads', update.message.document.file_name)
    os.makedirs('downloads', exist_ok=True)
    file.download(file_path)
    add_resource('document', file_path)
    update.message.reply_text('تم حفظ الملف بنجاح!')

# دوال الأوامر الخاصة بالإضافة
def add_tip_command(update: Update, context: CallbackContext) -> None:
    if context.args:
        tip = ' '.join(context.args)
        add_tip(tip)
        update.message.reply_text('تمت إضافة النصيحة.')
    else:
        update.message.reply_text('الرجاء كتابة نصيحة بعد الأمر.')

def add_rule_command(update: Update, context: CallbackContext) -> None:
    if context.args:
        rule = ' '.join(context.args)
        add_rule(rule)
        update.message.reply_text('تمت إضافة القاعدة.')
    else:
        update.message.reply_text('الرجاء كتابة القاعدة بعد الأمر.')

def add_resource_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('أرسل الملف مباشرة وسنقوم بحفظه.')

# دوال الأوامر الأخرى
def group_link(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('للانضمام إلى مجموعة واتساب: https://chat.whatsapp.com/example')

def collocations(update: Update, context: CallbackContext) -> None:
    if context.args:
        word = context.args[0]
        update.message.reply_text(f'Collocations with "{word}":\nmake a decision\ncatch a cold\ntake a risk')
    else:
        update.message.reply_text('الرجاء كتابة كلمة بعد الأمر.')

def study_plan(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('خطة دراسية:\n1. قراءة يومية\n2. مشاهدة فيديوهات\n3. محادثة نصف ساعة')

def common_mistakes(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('أخطاء شائعة:\n❌ He do\n✅ He does\n❌ I am agree\n✅ I agree')

def language_resources(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('مواقع مفيدة:\n- Duolingo\n- BBC Learning English\n- EnglishClass101')

def conversation_starters(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('مواضيع للنقاش:\n- السفر\n- التكنولوجيا\n- الثقافة')

def grammar_exercises(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('تمارين نحوية:\n- Exercise 1: Present Simple\n- Exercise 2: Past Tense')

def cultural_facts(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('حقائق:\n🇬🇧 البريطانيون يشربون أكثر من 165 مليون كوب شاي يومياً!')

def listening_exercises(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('تمارين استماع:\n- VOA Learning English\n- TED Talks')

def writing_tips(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('نصائح للكتابة:\n- راجع القواعد\n- استخدم جمل قصيرة\n- تجنب التكرار')

def idiomatic_expressions(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('تعبيرات اصطلاحية:\n- Break the ice\n- Hit the books\n- Under the weather')

def language_exchange(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('يمكنك العثور على شريك لغة عبر مواقع مثل: Tandem, HelloTalk')

def study_groups(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('مجموعات الدراسة تُنظم كل أسبوع. انضم لمجموعتنا على Telegram!')

def news(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('📰 خبر اليوم:\nScientists discover new English dialect in Antarctica!')

def language_jokes(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('😂 نكتة:\nWhy did the verb break up with the noun?\nBecause they had no agreement!')

def progress_check(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('📊 لتقييم تقدمك:\n- هل تحسّن نطقك؟\n- هل تستطيع فهم محادثة كاملة؟')

# دالة البدء
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('أهلاً بك في بوت معهد اللغة الإنجليزية! استخدم الأوامر التالية:\n'
                              '/add_tip - لإضافة نصيحة\n'
                              '/add_rule - لإضافة قاعدة\n'
                              '/add_resource - لإضافة ملف\n'
                              '/tips - لعرض النصائح\n'
                              '/rules - لعرض القواعد\n'
                              '/resources - لعرض الموارد\n'
                              '/join_group - الانضمام للمجموعة\n'
                              '/collocations [كلمة] - تعبيرات شائعة\n'
                              '/study_plan - خطة دراسية\n'
                              '/common_mistakes - أخطاء شائعة\n'
                              '/language_resources - موارد تعليمية\n'
                              '/conversation_starters - مواضيع للنقاش\n'
                              '/grammar_exercises - تمارين نحوية\n'
                              '/cultural_facts - حقائق ثقافية\n'
                              '/listening_exercises - تمارين استماع\n'
                              '/writing_tips - نصائح كتابة\n'
                              '/idiomatic_expressions - تعبيرات اصطلاحية\n'
                              '/language_exchange - تبادل لغوي\n'
                              '/study_groups - مجموعات دراسة\n'
                              '/news - أخبار\n'
                              '/language_jokes - نكات\n'
                              '/progress_check - تقييم التقدم')

# تشغيل البوت
def main():
    setup_database()
    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN:
        print("❌ لم يتم العثور على التوكن. تأكد من ضبط متغير البيئة BOT_TOKEN.")
        return

    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add_tip", add_tip_command))
    dp.add_handler(CommandHandler("add_rule", add_rule_command))
    dp.add_handler(CommandHandler("add_resource", add_resource_command))
    dp.add_handler(CommandHandler("tips", send_tips))
    dp.add_handler(CommandHandler("rules", send_rules))
    dp.add_handler(CommandHandler("resources", send_resources))
    dp.add_handler(CommandHandler("join_group", group_link))
    dp.add_handler(CommandHandler("collocations", collocations))
    dp.add_handler(CommandHandler("study_plan", study_plan))
    dp.add_handler(CommandHandler("common_mistakes", common_mistakes))
    dp.add_handler(CommandHandler("language_resources", language_resources))
    dp.add_handler(CommandHandler("conversation_starters", conversation_starters))
    dp.add_handler(CommandHandler("grammar_exercises", grammar_exercises))
    dp.add_handler(CommandHandler("cultural_facts", cultural_facts))
    dp.add_handler(CommandHandler("listening_exercises", listening_exercises))
    dp.add_handler(CommandHandler("writing_tips", writing_tips))
    dp.add_handler(CommandHandler("idiomatic_expressions", idiomatic_expressions))
    dp.add_handler(CommandHandler("language_exchange", language_exchange))
    dp.add_handler(CommandHandler("study_groups", study_groups))
    dp.add_handler(CommandHandler("news", news))
    dp.add_handler(CommandHandler("language_jokes", language_jokes))
    dp.add_handler(CommandHandler("progress_check", progress_check))
    dp.add_handler(MessageHandler(Filters.document, handle_document))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
