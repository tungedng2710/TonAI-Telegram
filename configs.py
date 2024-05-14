BOT_USERNAME = "tonai_chat_bot"
with open("bot_token.txt") as txtfile:
   BOT_TOKEN = txtfile.read()
   
LIMITATION = 20
GREETING = """
Một số tính năng của TonAI Assistant: 
🌱 /obj_det: Phát hiện vật thể trong ảnh
🌱 /imgen: Sinh ảnh với TonDiffusion
🌱 /vidgen: Sinh video với TonDiffusion
"""
MAX_DIFFUSION_PIPELINES = 2
DIFFUSION_PIPELINES_GPU = 1
DIFFUSION_PIPELINES_CPU = MAX_DIFFUSION_PIPELINES - DIFFUSION_PIPELINES_GPU
if DIFFUSION_PIPELINES_CPU == 0:
   DIFFUSION_PIPELINES_CPU = 1
INSTRUCTION = {
          "role": "system",
          "content": "Đóng vai trợ lý ảo TonAI Assistant của TonAI. Hãy trả lời câu hỏi hoặc làm theo yêu cầu sau"
       }
MODEL_NAMES = ['gpt-3.5-turbo', 'gpt-4', 'gemini']
TEXT2IMG_MODEL_ID = "stabilityai/stable-diffusion-2-1"
TEXT2VID_MODEL_ID = "damo-vilab/text-to-video-ms-1.7b"
