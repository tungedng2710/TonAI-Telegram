import os
import telebot
import warnings
from configs import BOT_TOKEN, BOT_USERNAME, GREETING, LIMITATION
from utils import complete, gen_image, gen_video

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
    USER_SESSIONS[message.chat.id]["features"] = {
        "/obj_det": {"name": "Object detection", "state": False},
        "/imgen": {"name": "TonAI text to image", "state": False, "prompt": ""},
        "/vidgen": {"name": "TonAI text to video", "state": False, "prompt": ""}
    }
    user_name = message.from_user.first_name
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, f"Hi {user_name} 🤗, {GREETING}")
    else:
        pass

@bot.message_handler(content_types=['sticker', 'audio', 'photo'])
def refuse_reply(message):
    # global USER_SESSIONS
    # user_session = USER_SESSIONS[message.chat.id]
    # if user_session["active"]:
    #     if message.chat.type == 'private':
    #         bot.reply_to(message, "Vui lòng nhập văn bản 🥺")
    #     else:
    #         pass
    pass

# ------------------------------------------------------------------------------------------ #
@bot.message_handler(func=lambda message: USER_SESSIONS[message.chat.id]["active"])
def handle_active_bot(message):
    global USER_SESSIONS
    global DIFFUSION_PIPELINES
    user_session = USER_SESSIONS[message.chat.id]
    # if message.text.lower() in user_session['features'].keys():
    #     user_session['features'][message.text.lower()]['state'] = True
    #     if user_session["features"]["/imgen"]["state"]: # if TonDiffusion is activated
    #         bot.send_message(message.chat.id, "Describe the image you want to generate")
    #     elif user_session["features"]["/vidgen"]["state"]: # if TonDiffusion is activated
    #         bot.send_message(message.chat.id, "Describe the video you want to generate")
    #     elif user_session["features"]["/obj_det"]["state"]:
    #         bot.send_message(message.chat.id, "Gimme an image")
    #     return
    
    if user_session['active']:
        if len(user_session["dialogue"]) > LIMITATION or message.text.lower() == "/reset":
            user_session["dialogue"] = user_session["dialogue"][-LIMITATION:]
        
        if user_session["features"]["/imgen"]["state"]:
            pass
            
        if user_session["features"]["/vidgen"]["state"]:
            pass

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