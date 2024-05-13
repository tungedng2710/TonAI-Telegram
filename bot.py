import os
import re
import torch
import telebot
import warnings
import asyncio
from io import BytesIO
from threading import Thread
from g4f.client import Client
from diffusers.utils import export_to_video
from configs import BOT_TOKEN, BOT_USERNAME, MODEL_NAMES, INSTRUCTION, GREETING, LIMITATION
from utils import complete, gen_image, gen_video, DIFFUSION_PIPELINES, VIDGEN_DIFFUSION_PIPELINES

from features.object_detection.yolov8 import detect_objects
warnings.filterwarnings('ignore')

bot = telebot.TeleBot(BOT_TOKEN)
bot_active = True
USER_SESSIONS = {}


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
    USER_SESSIONS[message.chat.id]["dialogue"] = [INSTRUCTION]
    user_name = message.from_user.first_name
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, f"Chào {user_name}, tôi có thể giúp gì cho bạn? \n{GREETING}")
    else:
        pass

@bot.message_handler(content_types=['sticker', 'audio'])
def refuse_reply(message):
    global USER_SESSIONS
    user_session = USER_SESSIONS[message.chat.id]
    if user_session["active"]:
        if message.chat.type == 'private':
            bot.reply_to(message, "Vui lòng nhập văn bản")
        else:
            pass

@bot.message_handler(content_types=['photo'])
def process_photo(message):
    global USER_SESSIONS
    user_session = USER_SESSIONS[message.chat.id]
    if not os.path.exists("photos"):
        os.makedirs("photos")
    if not os.path.exists("object_detection_results"):
        os.makedirs("object_detection_results")
    if user_session["active"]:
        if message.chat.type == 'private':
            fileID = message.photo[-1].file_id
            file_info = bot.get_file(fileID)
            local_image_path = file_info.file_path
            image_name = os.path.basename(local_image_path)
            with open(local_image_path, 'wb') as new_file:
                new_file.write(bot.download_file(file_info.file_path))
            if user_session["features"]["/obj_det"]["state"]:
                bot.send_message(message.chat.id, "I'm trying to find something in your image, be patient...")
                detect_objects(local_image_path, os.path.join("object_detection_results", image_name))
                photo = open(os.path.join("object_detection_results", image_name), "rb")
                bot.send_photo(message.chat.id, photo)
                bot.send_message(message.chat.id, "Object detector is deactivated. Type /obj_det to reactivate it")
                user_session["features"]["/obj_det"]["state"] = False
            else:
                bot.reply_to(message, GREETING)
        else:
            bot.reply_to(message, "Vui lòng nhập văn bản")

# ------------------------------------------------------------------------------------------ #
@bot.message_handler(func=lambda message: USER_SESSIONS[message.chat.id]["active"])
def handle_active_bot(message):
    global USER_SESSIONS
    global DIFFUSION_PIPELINES
    client = Client()
    user_session = USER_SESSIONS[message.chat.id]
    if message.text.lower() in user_session['features'].keys():
        user_session['features'][message.text.lower()]['state'] = True
        if user_session["features"]["/imgen"]["state"]: # if TonDiffusion is activated
            bot.send_message(message.chat.id, "Describe the image you want to generate!")
        elif user_session["features"]["/vidgen"]["state"]: # if TonDiffusion is activated
            bot.send_message(message.chat.id, "Describe the video you want to generate!")
        elif user_session["features"]["/obj_det"]["state"]:
            bot.send_message(message.chat.id, "Gimme an image")
        return
    
    if user_session['active']:
        if len(user_session["dialogue"]) > LIMITATION:
            user_session["dialogue"] = [INSTRUCTION]
        
        if user_session["features"]["/imgen"]["state"]:
            chat_id = message.chat.id
            user_session["features"]["/imgen"]["prompt"] = message.text
            input_text = user_session["features"]["/imgen"]["prompt"]
            bot.send_message(message.chat.id, "I'm drawing a picture, be patient...")
            for pipeline in DIFFUSION_PIPELINES:
                image = None
                if pipeline["is_available"]:
                    pipeline["is_available"] = False
                    try:
                        image = gen_image(input_text, pipeline["generator"])
                        pipeline["is_available"] = True
                        break
                    except:
                        pass
                pipeline["is_available"] = True
            user_session["features"]["/imgen"]["state"] = False
            if image is not None:
                image_path = f"photos/{chat_id}_{input_text}.png"
                bio = BytesIO()
                bio.name = image_path
                image.save(bio, 'PNG')
                bio.seek(0)
                bot.send_photo(message.chat.id, photo=bio)
                bot.send_message(message.chat.id, "I've done. Type /imgen to generate more images")
                return
            else:
                bot.send_message(message.chat.id, "I get overloaded. Try it later")
                return
            
        if user_session["features"]["/vidgen"]["state"]:
            chat_id = message.chat.id
            user_session["features"]["/vidgen"]["prompt"] = message.text
            input_text = user_session["features"]["/vidgen"]["prompt"]
            bot.send_message(message.chat.id, "I'm making a video, be patient...")
            try:
                video_frames = gen_video(input_text)
            except Exception as e:
                print(e)
                pass
            user_session["features"]["/vidgen"]["state"] = False
            if video_frames is not None:
                video_path = f"videos/{chat_id}_{input_text}.mp4"
                export_to_video(video_frames, video_path)
                bot.send_video(chat_id=chat_id, video=open(video_path, 'rb'), supports_streaming=True)
                bot.send_message(message.chat.id, "I've done. Type /vidgen to generate more videos")
                return
            else:
                bot.send_message(message.chat.id, "I get overloaded. Try it later")
                return

        if message.chat.type == 'private':
            chat_id = message.chat.id
            input_text = message.text
            user_session["dialogue"].append({"role": "user", "content": input_text})
            output = complete(user_session["dialogue"], MODEL_NAMES, client)
            user_session["dialogue"].append({"role": "assistant", "content": output})
            bot.send_message(chat_id, output)
        else:
            if f"@{BOT_USERNAME}" in message.text:
                input_text = message.text.replace(f"@{BOT_USERNAME}", "")
                user_session["dialogue"].append({"role": "user", "content": input_text})
                output = complete(user_session["dialogue"], MODEL_NAMES, client)
                user_session["dialogue"].append({"role": "assistant", "content": output})
                bot.reply_to(message, output)
            else:
                pass
            
# ------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------ #
if __name__ == '__main__':
    print("Bot is running")
    bot.infinity_polling()
# ------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------ #