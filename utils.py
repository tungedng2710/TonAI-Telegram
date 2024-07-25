import requests
import torch

from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler, DiffusionPipeline
from bs4 import BeautifulSoup
from newspaper import Article
from configs import TEXT2IMG_MODEL_ID, TEXT2VID_MODEL_ID, DIFFUSION_PIPELINES_GPU, DIFFUSION_PIPELINES_CPU, NEGATIVE_PROMPT

DEVICE = "cuda:0"
VIDGEN_DIFFUSION_PIPELINES = []
DIFFUSION_PIPELINES = []
if DIFFUSION_PIPELINES_GPU > 0:
    for i in range(DIFFUSION_PIPELINES_GPU):
        pipe = StableDiffusionPipeline.from_single_file(TEXT2IMG_MODEL_ID)
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        try:
            pipe = pipe.to(DEVICE)
            pipeline_dict = {"generator": pipe, "is_available": True, "gpu": True}
        except Exception as e:
            pipeline_dict = {"generator": pipe, "is_available": True, "gpu": False}
        DIFFUSION_PIPELINES.append(pipeline_dict)
if DIFFUSION_PIPELINES_CPU > 0:
    for i in range(DIFFUSION_PIPELINES_CPU):
        pipe = StableDiffusionPipeline.from_single_file(TEXT2IMG_MODEL_ID, torch_dtype=torch.float16)
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        pipeline_dict = {"generator": pipe, "is_available": True, "gpu": False}
        DIFFUSION_PIPELINES.append(pipeline_dict)

# for i in range(2):
#     vidgen_pipe = DiffusionPipeline.from_pretrained("damo-vilab/text-to-video-ms-1.7b", 
#                                                     torch_dtype=torch.float16, variant="fp16")
#     vidgen_pipe.scheduler = DPMSolverMultistepScheduler.from_config(vidgen_pipe.scheduler.config)
#     vidgen_pipe.enable_model_cpu_offload(gpu_id = 0)
#     vidgen_pipe.enable_vae_slicing()
#     pipeline_dict = {"generator": vidgen_pipe, "is_available": True, "gpu": True}
#     VIDGEN_DIFFUSION_PIPELINES.append(pipeline_dict)

print(f"Num imgen pipelines: {len(DIFFUSION_PIPELINES)}")

def complete(messages, model_names, client):
    for model_name in model_names:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=messages
            )
            output = response.choices[0].message.content
            break
        except Exception as e:
            print(e)
            output = "TonAI is temporarily down 🥺"
            continue
    return output

def gen_image(prompt, pipe):
    image = pipe(prompt=prompt, 
                 width=768, 
                 height=768, 
                 num_inference_steps=20,
                 negative_prompt=NEGATIVE_PROMPT,
                 guidance_scale=2).images[0]
    return image

def gen_video(prompt, num_frames=50, device_id=0):
    vidgen_pipe = DiffusionPipeline.from_pretrained(TEXT2VID_MODEL_ID,
                                                    torch_dtype=torch.float16, 
                                                    variant="fp16")
    vidgen_pipe.scheduler = DPMSolverMultistepScheduler.from_config(vidgen_pipe.scheduler.config)
    vidgen_pipe.enable_model_cpu_offload(gpu_id = device_id)
    vidgen_pipe.enable_vae_slicing()
    video_frames = vidgen_pipe(prompt, num_inference_steps=25, num_frames=num_frames).frames
    return video_frames

def extract_article_text(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:   
            # Extract main text using newspaper3k
            article = Article(url)
            article.download(input_html=response.text)
            article.parse()
            return article.text
        else:
            print(f"Failed to retrieve content. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# @bot.message_handler(func=lambda message: '/qna' in message.text.lower())
# def extract_qna(message):
#     global user_sessions
#     client = Client()
#     # url_to_read = re.search("(?P<url>https?://[^\s]+)", message.text).group("url")
#     if user_sessions[message.chat.id]["active"]:
#         url_to_read = message.text.replace('/extract_qna ', '')
#         try:
#             article_text = extract_article_text(url_to_read)
#             input_text = f"""
#                 Hãy đọc đoạn văn sau và tạo một bộ Q&A gồm 10 cặp câu hỏi và câu trả lời: Hãy đọc tài liệu này và tạo một 
#                 bộ Q&A bao gồm 10 câu hỏi và câu trả lời. Độ dài mỗi câu trả lời từ 2 đến 4 câu. Để làm cho câu hỏi sinh động hơn, 
#                 hãy đóng vai bệnh nhân hỏi bác sĩ và giả định ra tình huống thực tế gặp phải: \n
#                 {article_text}
#                 """
#             messages = [{"role": "user", "content": input_text}]
#             response = client.chat.completions.create(model=model_names[0],messages=messages)
#             output = response.choices[0].message.content
#             bot.send_message(message.chat.id, output)
#         except:
#             pass

# @bot.message_handler(func=lambda message: message.text.lower() == '/end')
# def say_bye(message):
#     global user_sessions
#     bot.reply_to(message, "Bye! Tôi sẽ trở lại khi bạn gõ '/resume'")
#     user_sessions[message.chat.id] = {"active": False}

# @bot.message_handler(func=lambda message: message.text.lower() == '/resume')
# def comeback(message):
#     global user_sessions
#     user_sessions[message.chat.id] = {"active": True}
#     bot.reply_to(message, "Xin chào, tôi có thể giúp gì cho bạn?")

# @bot.message_handler(func=lambda message: '/summarize' in message.text.lower())
# def summarize_article(message):
#     global USER_SESSIONS
#     client = Client()
#     if USER_SESSIONS[message.chat.id]["active"]:
#         url_to_read = re.search("(?P<url>https?://[^\s]+)", message.text).group("url")
#         try:
#             article_text = extract_article_text(url_to_read)
#             input_text = f"Tóm tắt bài báo sau: {article_text}"
#             messages = [{"role": "user", "content": input_text}]
#             response = client.chat.completions.create(model=MODEL_NAMES[0],messages=messages)
#             output = response.choices[0].message.content
#             bot.send_message(message.chat.id, output)
#         except:
#             pass