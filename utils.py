import ollama

from configs import MODEL_ID


def complete(messages):
    try:
        response = ollama.chat(model=MODEL_ID, messages=messages)
        output = response['message']['content']
    except Exception as e:
        print(e)
        output = "TonAI is temporarily down 🥺"
    return output

def gen_image(prompt, pipe):
    pass

def gen_video(prompt, num_frames=50, device_id=0):
    pass

def extract_article_text(url):
    pass