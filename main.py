import telebot
import google.generativeai as genai
import os

TELEGRAM_TOKEN = os.environ.get('8333602244:AAHU0BsG3pyyQ-RFt8FVFK-ih8IPCuCzvHw')
GEMINI_KEY = os.environ.get('AIzaSyBB1H7YC2D6bC7oNImuGuMq7elV5w49wp4')

bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        bot_username = bot.get_me().username
        if message.chat.type == "private" or f"@{bot_username}" in message.text:
            prompt = message.text.replace(f"@{bot_username}", "").strip()
            if prompt:
                response = model.generate_content(prompt)
                bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Hata: {e}")

print("Bot çalışıyor...")
bot.polling(non_stop=True)
