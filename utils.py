import base64
import ollama
import subprocess
from configs import MODEL_ID


def ensure_latest_tag(model_name: str) -> str:
    """
    Ensure the given model name has a tag; if not, append ':latest'.

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
    

def check_ollama_model(model_id: str) -> bool:
    """
    Check if the specified model ID exists in the list of available Ollama models.

    Args:
        model_id (str): The ID of the model to check.

    Returns:
        bool: True if the model exists, False otherwise.
    """
    model_id = ensure_latest_tag(model_id)
    models_list = ollama.list()
    for model in models_list["models"]:
        if model_id == model["name"]:
            return True
    return False


def encode_image_to_base64(image_path: str) -> str:
    """
    Convert an image file to a base64 encoded string.

    Args:
        image_path (str): The file path of the image to encode.

    Returns:
        str: The base64 encoded string representation of the image.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def complete(messages: list) -> str:
    """
    Send a list of messages to the Ollama API and get the model's response.

    Args:
        messages (list): A list of messages for the chat model.

    Returns:
        str: The response message from the model, or an error message if the request fails.
    """
    try:
        response = ollama.chat(model=MODEL_ID, messages=messages)
        output = response['message']['content']
    except Exception as e:
        print(e)
        output = "TonAI is temporarily down 🥺"
    return output


def gen_image(prompt: str, chat_id: str) -> None:
    """
    Generate an image based on a given prompt and save it to a specific location.

    Args:
        prompt (str): The textual description used to generate the image.
        chat_id (str): The chat ID used to determine the output file's saved path.

    Returns:
        None
    """
    command = [
        "python",           # Python interpreter
        "features/query_comfyui.py",         # The script to execute
        "--prompt", f"'{prompt}'",          # The prompt argument
        "--saved_path", f"stuffs/{chat_id}_temp.jpg"    # The saved path argument
    ]
    try:
        subprocess.run(command, capture_output=True, text=True)
    except Exception as e:
        print(f"Error generating image: {e}")