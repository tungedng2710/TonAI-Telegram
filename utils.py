import base64
import ollama
import subprocess
from configs import MODEL_ID


def ensure_latest_tag(model_name: str) -> str:
    """
    Ensures the model_name has a tag; if not, appends ':latest'.

    Args:
        model_name (str): The name of the model, potentially without a tag.

    Returns:
        str: The model name with a tag (e.g., ':latest' if missing).
    """
    # Check if ':' exists and the tag is non-empty after ':'
    if ':' in model_name and model_name.split(':')[-1]:
        return model_name  # Model already has a tag
    else:
        return f"{model_name}:latest"
    
    
def check_ollama_model(model_id):
    model_id = ensure_latest_tag(model_id)
    models_list = ollama.list()
    for model in models_list["models"]:
        if model_id == model["name"]:
            return True
    return False


def encode_image_to_base64(image_path):
    """Convert an image file to a base64 encoded string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def complete(messages):
    try:
        response = ollama.chat(model=MODEL_ID, messages=messages)
        output = response['message']['content']
    except Exception as e:
        print(e)
        output = "TonAI is temporarily down 🥺"
    return output

def gen_image(prompt, chat_id):
    command = [
        "python",           # Python interpreter
        "features/query_comfyui.py",         # The script you want to run
        "--prompt", f"'{prompt}'",          # The prompt argument
        "--saved_path", f"stuffs/{chat_id}_temp.jpg"    # The saved path argument
    ]
    try:
        subprocess.run(command, capture_output=True, text=True)
    except Exception as e:
        print(f"An error occurred: {e}")

def gen_video(prompt, num_frames=50, device_id=0):
    pass