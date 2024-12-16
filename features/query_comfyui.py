#This is an example that uses the websockets api and the SaveImageWebsocket node to get images directly without
#them being saved to disk

import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse
import json

server_address = "0.0.0.0:7866"
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

def query_sd35(ckpt_name: str = "sd3.5_medium.safetensors",
               prompt: str = "a capybara",
               negative_prompt: str = "ugly, disfigured, deformed",
               width: int = 1024,
               height: int = 1024,
               batch_size: int = 1,
               seed: int = 77498386,
               cfg: float = 3.0,
               step: int = 20):
    
    with open('stuffs/comfyui_workflow_api/sd3_5_workflow_api.json') as f:
        prompt_config = json.load(f)

    prompt_config["3"]["inputs"]["seed"] = seed
    prompt_config["3"]["inputs"]["cfg"] = cfg
    prompt_config["3"]["inputs"]["step"] = step
    prompt_config["4"]["inputs"]["ckpt_name"] = ckpt_name
    prompt_config["16"]["inputs"]["text"] = prompt
    prompt_config["40"]["inputs"]["text"] = negative_prompt
    prompt_config["53"]["inputs"]["width"] = width
    prompt_config["53"]["inputs"]["height"] = height
    prompt_config["53"]["inputs"]["batch_size"] = batch_size

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
    return output_images


# query_sd35(prompt="a cat")