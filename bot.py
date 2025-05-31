# english_learning_bot.py

import sqlite3
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# إعدادات المشرف والتوكن
ADMIN_ID = 5048497546
BOT_TOKEN = "7717188841:AAFwAGIfcsgcem0fx678cSUK6faKmNUuVWM"

# إنشاء مجلدات للملفات حسب المستوى
LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]
TYPES = ["pdf", "audio", "rules", "stories", "idioms", "podcasts"]

for level in LEVELS:
    for t in TYPES:
        os.makedirs(f"content/{level}/{t}", exist_ok=True)

# قاعدة البيانات

def setup_db():
    conn = sqlite3.connect("bot.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT
        )
    """)
    conn.commit()
    conn.close()

# إضافة نصيحة جديدة

def add_tip(text):
    conn = sqlite3.connect("bot.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO tips (text) VALUES (?)", (text,))
    conn.commit()
    conn.close()

# عرض نصائح

def show_tips(update: Update, context: CallbackContext):
    conn = sqlite3.connect("bot.db")
    cur = conn.cursor()
    cur.execute("SELECT text FROM tips")
    rows = cur.fetchall()
    if rows:
        tips = "\n\n".join([r[0] for r in rows])
        update.message.reply_text(f"\U0001F4D6 نصائح لتعلم الإنجليزية:\n{tips}")
    else:
        update.message.reply_text("لا توجد نصائح حالياً.")
    conn.close()

# أمر إضافة نصيحة (مشرف فقط)

def add_tip_cmd(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        return update.message.reply_text("هذا الأمر للمشرف فقط.")
    text = " ".join(context.args)
    if not text:
        return update.message.reply_text("يرجى كتابة النصيحة بعد الأمر.")
    add_tip(text)
    update.message.reply_text("تمت إضافة النصيحة بنجاح.")

# رفع ملفات تعليمية (PDF أو صوتيات وغيرها)

def upload_file(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        return update.message.reply_text("هذا الأمر للمشرف فقط.")
    try:
        level = context.args[0].upper()
        ftype = context.args[1].lower()
        if level not in LEVELS or ftype not in TYPES:
            raise ValueError
        context.user_data['upload_level'] = level
        context.user_data['upload_type'] = ftype
        update.message.reply_text("الرجاء إرسال الملف الآن.")
    except:
        update.message.reply_text("يرجى كتابة الأمر بالشكل: /upload A1 pdf")

# استقبال الملف من المشرف

def handle_file(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        return
    level = context.user_data.get("upload_level")
    ftype = context.user_data.get("upload_type")
    if not level or not ftype:
        return update.message.reply_text("يرجى استخدام الأمر /upload أولاً.")
    file = update.message.document or update.message.audio
    if not file:
        return update.message.reply_text("لم يتم اكتشاف ملف صالح.")
    file_path = f"content/{level}/{ftype}/{file.file_name}"
    file.get_file().download(file_path)
    update.message.reply_text("تم حفظ الملف بنجاح.")
    context.user_data.clear()

# عرض محتوى معين من المستوى

def show_content(update: Update, context: CallbackContext):
    try:
        level = context.args[0].upper()
        ftype = context.args[1].lower()
        path = f"content/{level}/{ftype}"
        if not os.path.exists(path):
            raise ValueError
        files = os.listdir(path)
        if not files:
            return update.message.reply_text("لا يوجد محتوى بعد.")
        for fname in files:
            with open(os.path.join(path, fname), "rb") as f:
                update.message.reply_document(f)
    except:
        update.message.reply_text("يرجى استخدام الأمر بالشكل: /get A1 pdf")

# أوامر عامة

def start(update: Update, context: CallbackContext):
    update.message.reply_text("""
\U0001F44B مرحباً بك في بوت تعليم الإنجليزية!
اختر أمراً:
/start - هذه الرسالة
/tips - عرض نصائح
/add_tip [النصيحة] - إضافة نصيحة (للمشرف)
/upload [المستوى] [نوع] - رفع ملف (للمشرف)
/get [المستوى] [نوع] - عرض محتوى
/info - نبذة عن المعهد وصانع البوت
    """)

def info(update: Update, context: CallbackContext):
    update.message.reply_text("""
\U0001F393 معهد لوس أنجلوس لتعلم اللغة الإنجليزية
نوفر محتوى تعليمي تفاعلي شامل من المستوى A1 إلى C2.

صانع البوت: أ. أحمد - متخصص في تصميم أنظمة تعليمية رقمية.
    """)

# إعداد الكود الأساسي

def main():
    setup_db()
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("tips", show_tips))
    dp.add_handler(CommandHandler("add_tip", add_tip_cmd))
    dp.add_handler(CommandHandler("upload", upload_file))
    dp.add_handler(CommandHandler("get", show_content))
    dp.add_handler(MessageHandler(Filters.document | Filters.audio, handle_file))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
