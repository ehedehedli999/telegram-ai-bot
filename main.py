import telebot
import google.generativeai as genai
import os

# BURAYA DOKUNMA! Bu isimler Hugging Face Settings'teki isimlerle aynı olmalı.
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_KEY')

# Eğer şifreler gelmezse hata mesajı ver
if not TELEGRAM_TOKEN or not GEMINI_KEY:
    print("HATA: Ayarlar (Secrets) kısmında isimler yanlış yazılmış!")
    exit(1)

bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        bot_username = bot.get_me().username
        # Özel mesaj veya grupta etiketlenme durumu
        if message.chat.type == "private" or f"@{bot_username}" in message.text:
            prompt = message.text.replace(f"@{bot_username}", "").strip()
            if prompt:
                response = model.generate_content(prompt)
                bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Hata: {e}")

print("Bot başarıyla başlatıldı!")
bot.polling(non_stop=True)