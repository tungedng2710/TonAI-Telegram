# TonAI Telegram Bot

**Telegram bot with Ollama and ComfyUI**

<p align="center">
   <img src="./stuffs/ollama_logo.jpg" height="100" />
   <img src="./stuffs/telegram_logo.jpg" height="100" />
   <img src="./stuffs/comfy_logo.jpg" height="100" />
</p>

## Setup
Clone this repository and move to it
```
git clone https://github.com/tungedng2710/TonAI-Telegram.git
cd TonAI-Telegram
```
Install requirements
```
pip install -r requirements.txt
```
Install [Ollama](https://ollama.com/) backend

If you are using Linux, run the command
```
curl -fsSL https://ollama.com/install.sh | sh
```
After installing Ollama, start the Ollama service
```
ollama serve
```
Ollama will run on default port `11434`. If you want more advanced configs, please checkout the [Official Ollama website](https://ollama.com/)

Create a ```configs.py``` file, then write the configs file like the example below
```
MODEL_ID = 'llama3.2-vision'
BOT_USERNAME = "tonai_chat_bot"
with open("bot_token.txt") as txtfile:
   BOT_TOKEN = txtfile.read()
   
LIMITATION = 20
GREETING = """
I'm TonAI Chatbot
"""
```
You have to pull Ollama model (or create it before). For example, from terminal, run this command below to pull Llama 3.2 11B Vision from Ollama. If you want your bot can handle photos sent by users, you need to find multi-modal models.
```
ollama run llama3.2-vision
```

**NOTE:** You must also have the ```bot_token.txt``` file, which contains your Telegram bot token. I cannot upload the `BOT_TOKEN`, so you have to replace the `BOT_TOKEN` infomation in this code with your own Telegram bot token. If you don't know how to create a Telegram bot, visit this [Tutorial website](https://core.telegram.org/bots/tutorial).
## Run
Just run the Python code
```
python run main.py
```
