import os
import telebot
import warnings
from configs import BOT_TOKEN, BOT_USERNAME, GREETING, LIMITATION
from utils import complete
warnings.filterwarnings('ignore')

bot = telebot.TeleBot(BOT_TOKEN)
bot_active = True
USER_SESSIONS = {}
if not os.path.exists("photos"):
    os.makedirs("photos")
if not os.path.exists("videos"):
    os.makedirs("videos")

# ------------------------------------------------------------------------------------------ #
@bot.message_handler(func=lambda message: message.chat.id not in USER_SESSIONS)
def add_new_user(message):
    global USER_SESSIONS
    USER_SESSIONS[message.chat.id] = {"active": True}  # Initialize user session
    USER_SESSIONS[message.chat.id]["dialogue"] = []
    user_name = message.from_user.first_name
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, f"Hi {user_name} 🤗, {GREETING}")
    else:
        pass

@bot.message_handler(content_types=['sticker', 'audio', 'photo'])
def refuse_reply(message):
    pass

# ------------------------------------------------------------------------------------------ #
@bot.message_handler(func=lambda message: USER_SESSIONS[message.chat.id]["active"])
def handle_active_bot(message):
    global USER_SESSIONS
    global DIFFUSION_PIPELINES
    user_session = USER_SESSIONS[message.chat.id]
    
    if user_session['active']:
        if len(user_session["dialogue"]) > LIMITATION or message.text.lower() == "/reset":
            user_session["dialogue"] = user_session["dialogue"][-LIMITATION:]

        if message.chat.type == 'private':
            chat_id = message.chat.id
            input_text = message.text
            user_session["dialogue"].append({"role": "user", "content": input_text})
            output = complete(user_session["dialogue"])
            user_session["dialogue"].append({"role": "assistant", "content": output})
            bot.send_message(chat_id, output)
        else:
            if f"@{BOT_USERNAME}" in message.text:
                input_text = message.text.replace(f"@{BOT_USERNAME}", "")
                user_session["dialogue"].append({"role": "user", "content": input_text})
                output = complete(user_session["dialogue"])
                user_session["dialogue"].append({"role": "assistant", "content": output})
                bot.reply_to(message, output)
            else:
                pass
            

# ------------------------------------------------------------------------------------------ #
if __name__ == '__main__':
    print("Bot is running")
    bot.infinity_polling()
# ------------------------------------------------------------------------------------------ #