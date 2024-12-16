#This is an example that uses the websockets api and the SaveImageWebsocket node to get images directly without
#them being saved to disk

import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import random
import json
import urllib.request
import urllib.parse
import json
import argparse


server_address = "0.0.0.0:7865"
# server_address = "116.103.227.252:7865"
client_id = str(uuid.uuid4())

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req =  urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()

def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())

def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break #Execution is done
        else:
            # If you want to be able to decode the binary stream for latent previews, here is how you can do it:
            # bytesIO = BytesIO(out[8:])
            # preview_image = Image.open(bytesIO) # This is your preview in PIL image format, store it in a global
            continue #previews are binary data

    history = get_history(prompt_id)[prompt_id]
    for node_id in history['outputs']:
        node_output = history['outputs'][node_id]
        images_output = []
        if 'images' in node_output:
            for image in node_output['images']:
                image_data = get_image(image['filename'], image['subfolder'], image['type'])
                images_output.append(image_data)
        output_images[node_id] = images_output

    return output_images

def query_sd35(ckpt_name: str = "sd3.5_medium_incl_clips_t5xxlfp8scaled.safetensors",
               prompt: str = "a capybara",
               negative_prompt: str = "ugly, disfigured, deformed",
               width: int = 768,
               height: int = 768,
               batch_size: int = 1,
               seed: int = random.randint(0, 999999999999999),
               cfg: float = 3.0,
               step: int = 20,
               saved_path: str = "./temp.jpg"):
    
    with open('stuffs/sd3_5_workflow_api.json') as f:
        prompt_config = json.load(f)

    prompt_config["3"]["inputs"]["seed"] = seed
    prompt_config["3"]["inputs"]["cfg"] = cfg
    prompt_config["3"]["inputs"]["step"] = step
    prompt_config["4"]["inputs"]["ckpt_name"] = ckpt_name
    prompt_config["6"]["inputs"]["text"] = prompt
    prompt_config["7"]["inputs"]["text"] = negative_prompt
    prompt_config["5"]["inputs"]["width"] = width
    prompt_config["5"]["inputs"]["height"] = height
    prompt_config["5"]["inputs"]["batch_size"] = batch_size

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    images = get_images(ws, prompt_config)
    ws.close() # for in case this example is used in an environment where it will be repeatedly called, like in a Gradio app. otherwise, you'll randomly receive connection timeouts
    #Commented out code to display the output images:

    output_images = []
    for node_id in images:
        for image_data in images[node_id]:
            from PIL import Image
            import io
            output_images.append(Image.open(io.BytesIO(image_data)))
    output_images[0].save(saved_path)
    return output_images


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SD3.5 API query and save output image.")
    parser.add_argument("--saved_path", type=str, default="./temp.jpg", 
                        help="Path to save the generated image. Default is './temp.jpg'.")
    parser.add_argument("--prompt", type=str, default="a cat", 
                        help="Prompt for image generation")

    args = parser.parse_args()

    # Call the query function with the user-defined saved_path
    query_sd35(prompt=args.prompt,
               saved_path=args.saved_path)