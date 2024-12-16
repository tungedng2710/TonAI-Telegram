import os
import telebot
import warnings
from configs import *
from utils import complete, encode_image_to_base64, check_ollama_model
warnings.filterwarnings('ignore')

# ------------------------------------------------------------------------------------------ #
bot = telebot.TeleBot(BOT_TOKEN)
USER_SESSIONS = {}
if not check_ollama_model(MODEL_ID):
    print(f"Opp!, you have no Ollama model named {MODEL_ID}! Please pull or create it")
    exit()
else:
    print(f"Bot will run with Ollama model: [{MODEL_ID}]")
    
    
def do_nothing(**kwargs):
    pass
    
# ------------------------------------------------------------------------------------------ #
@bot.message_handler(func=lambda message: message.chat.id not in USER_SESSIONS)
def add_new_user(message):
    global USER_SESSIONS
    USER_SESSIONS[message.chat.id] = {"active": True,
                                      "features": {
                                          "ovd": False,
                                          "gen_image": False
                                          }
                                      }
    USER_SESSIONS[message.chat.id]["dialogue"] = []
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, f"Hi {message.from_user.first_name} 🤗")


@bot.message_handler(commands=['reset'])
def reset(message):
    chat_id = message.chat.id  # Get the chat ID
    if chat_id in USER_SESSIONS:
        USER_SESSIONS.pop(chat_id)  # Remove the chat ID from the dictionary
        bot.reply_to(message, "Your session has been reset.")
    else:
        bot.reply_to(message, "No active session found to reset.")
        
        
@bot.message_handler(commands=['ovd'])
def trigger_ovd(message):
    USER_SESSIONS[message.chat.id]["features"]["ovd"] = True
    

@bot.message_handler(commands=['gen_image'])
def trigger_image_generator(message):
    USER_SESSIONS[message.chat.id]["features"]["gen_image"] = True
    bot.reply_to(message, "Image generator is not available")
    

@bot.message_handler(content_types=['audio'])
def do_nothing():
    pass


@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    global USER_SESSIONS
    user_session = USER_SESSIONS[message.chat.id]
    if user_session['active'] and message.chat.type == 'private':
        sticker = message.sticker
        if sticker.emoji:
            user_session["dialogue"].append({"role": "user", "content": sticker.emoji})
            output = complete(user_session["dialogue"])
            user_session["dialogue"].append({"role": "assistant", "content": output})
            bot.reply_to(message, output)


@bot.message_handler(content_types=['photo'])
def add_image(message):
    global USER_SESSIONS
    user_session = USER_SESSIONS[message.chat.id]
    user_stuffs_path = f"stuffs/user_{message.chat.id}"
    if not os.path.exists(user_stuffs_path):
        os.makedirs(user_stuffs_path)
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = os.path.join(user_stuffs_path, 'temp.jpg')
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    base64_image = encode_image_to_base64(file_path)
    user_session["dialogue"].append({
                    "role": "user",
                    "content": "",
                    "images": [base64_image],
                })
    os.remove(file_path)


@bot.message_handler(func=lambda message: USER_SESSIONS[message.chat.id]["active"])
def handle_active_bot(message):
    global USER_SESSIONS
    user_session = USER_SESSIONS[message.chat.id]
    
    if user_session['active']:
        if len(user_session["dialogue"]) > LIMITATION:
            user_session["dialogue"] = user_session["dialogue"][-LIMITATION:]

        if message.chat.type == 'private':
            chat_id = message.chat.id
            input_text = message.text
            user_session["dialogue"].append({"role": "user", "content": input_text})
            output = complete(user_session["dialogue"])
            user_session["dialogue"].append({"role": "assistant", "content": output})
            bot.send_message(chat_id, output)
        else:
            if f"@{BOT_USERNAME}" in message.text: # Recognize if bot is tagged
                input_text = message.text.replace(f"@{BOT_USERNAME}", "")
                user_session["dialogue"].append({"role": "user", "content": input_text})
                output = complete(user_session["dialogue"])
                user_session["dialogue"].append({"role": "assistant", "content": output})
                bot.reply_to(message, output)
            

# ------------------------------------------------------------------------------------------ #
if __name__ == '__main__':
    print("Bot is running")
    bot.infinity_polling()
# ------------------------------------------------------------------------------------------ #