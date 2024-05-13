BOT_USERNAME = "tonai_chat_bot"
BOT_TOKEN = "6260442274:AAEQaoCxHTHwhS56TBIeyyu3B8D9mKNOx_w"
LIMITATION = 20
GREETING = """
Một số tính năng của TonAI Assistant: 
   /obj_det: Phát hiện vật thể trong ảnh
   /imgen: Sinh ảnh với TonDiffusion
   /vidgen: Sinh video với TonDiffusion
"""
MAX_DIFFUSION_PIPELINES = 3
DIFFUSION_PIPELINES_GPU = 2
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


# ------------------------------------------------------------------------------------------------ #
# BOT_USERNAME = "dmom_demo_bot"
# BOT_TOKEN = "6941617248:AAHxaQqKEbgiFXs3R0n36E8psP1jB3D2hbI"
# instruction = "Bạn là bác sĩ, hãy trả lời ngắn gọn từ 2 đến 3 câu cho câu hỏi sau của bệnh nhân: "
