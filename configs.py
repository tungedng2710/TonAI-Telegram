BOT_USERNAME = "tonai_chat_bot"
with open("bot_token.txt") as txtfile:
   BOT_TOKEN = txtfile.read()
   
LIMITATION = 10
GREETING = """
Một số tính năng của TonAI Assistant: 
🌱 /obj_det: Phát hiện vật thể trong ảnh
🌱 /imgen: Sinh ảnh bằng AI
🌱 /vidgen: Sinh video bằng AI
Để tạo ảnh nghệ thuật nâng cao, thử TonAI Creative tại https://c048ee8bef3e06b813.gradio.live/
"""
MAX_DIFFUSION_PIPELINES = 2
DIFFUSION_PIPELINES_GPU = 1
DIFFUSION_PIPELINES_CPU = MAX_DIFFUSION_PIPELINES - DIFFUSION_PIPELINES_GPU
if DIFFUSION_PIPELINES_CPU == 0:
   DIFFUSION_PIPELINES_CPU = 1
INSTRUCTION = {
          "role": "system",
          "content": "Hãy sử dụng tiếng Việt. Đóng vai trợ lý ảo TonAI Assistant của TonAI. Hãy trả lời câu hỏi hoặc làm theo yêu cầu sau"
      }
MODEL_NAMES = ['gpt-3.5-turbo', 'gpt-4']
TEXT2IMG_MODEL_ID = "../checkpoints/realisticVisionV60B1_v51HyperVAE.safetensors"
TEXT2VID_MODEL_ID = "damo-vilab/text-to-video-ms-1.7b"
NEGATIVE_PROMPT = "extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, lowres, text, error, cropped, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions"
