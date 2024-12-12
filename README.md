# TonAI Telegram Bot

TonAI Chatbot as a Telegram bot

## Setup
### For chatbot only
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
After install Ollama, start the Ollama service
```
ollama serve
```
Ollama will run on default port `11434`. If you want more advanced configs, please checkout the [Official Ollama website](https://ollama.com/)

### For image generation
Coming soon

## Run
**NOTE:** I cannot upload the `BOT_TOKEN`, so you have to replace the `BOT_TOKEN` infomation in this code with your own Telegram bot token. If you don't know how to create a Telegram bot, visit this [Tutorial website](https://core.telegram.org/bots/tutorial)

Just run the Python code
```
python run bot.py
```