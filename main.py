import telebot
import time
import threading
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- আপনার সেটিংস ---
API_TOKEN = '8599727244:AAFuffnYlVPaHkbmGmyqBPtZM84OpHG-yL8'
ADMIN_ID = 5716499834 
CHANNEL_ID = -1003878856268  # আপনার স্টোরেজ চ্যানেলের আইডি
MUST_JOIN_CHANNEL = "https://t.me/+LFEmWRfqWmhjMmZl"

bot = telebot.TeleBot(API_TOKEN)

# ফাইল অটো-ডিলিট ফাংশন (১০ মিনিট পর)
def auto_delete(chat_id, message_id):
    time.sleep(600)  # ৬০০ সেকেন্ড = ১০ মিনিট
    try:
        bot.delete_message(chat_id, message_id)
        bot.send_message(chat_id, "⚠️ **নিরাপত্তার কারণে ফাইলটি ১০ মিনিট পর মুছে ফেলা হয়েছে।**")
    except:
        pass

@bot.message_handler(commands=['start'])
def start(message):
    args = message.text.split()
    if len(args) > 1:
        # মেইন বট থেকে আসা ফাইল রিকোয়েস্ট
        file_id = args[1]
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔓 Get File", callback_data=f"get_{file_id}"))
        bot.send_message(message.chat.id, "🚀 **Alpha Drive Storage**\n\nফাইলটি পেতে নিচের বাটনে ক্লিক করুন:", reply_markup=markup)
    else:
        bot.reply_to(message, "👋 হ্যালো! এটি আপনার স্টোরেজ বট। এখানে ফাইল পাঠিয়ে আইডি জেনারেট করুন।")

@bot.callback_query_handler(func=lambda call: call.data.startswith('get_'))
def send_file(call):
    file_msg_id = call.data.split('_')[1]
    try:
        # চ্যানেল থেকে ফাইল কপি করে ইউজারকে পাঠানো
        sent_msg = bot.copy_message(call.message.chat.id, CHANNEL_ID, int(file_msg_id))
        bot.answer_callback_query(call.id, "ফাইলটি পাঠানো হয়েছে!")
        
        # অটো-ডিলিট টাইমার শুরু
        threading.Thread(target=auto_delete, args=(call.message.chat.id, sent_msg.message_id)).start()
    except Exception as e:
        bot.send_message(call.message.chat.id, f"❌ ভুল: {str(e)}")

if __name__ == "__main__":
    print("Storage Bot is running...")
    bot.infinity_polling()
