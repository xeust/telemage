import os
import json
import requests
import base64
from deta import Deta
from fastapi import FastAPI, Request 
from fastapi.responses import HTMLResponse
from jinja2 import Template

app = FastAPI()

deta = Deta()

photos = deta.Drive("generations")

bot_key = os.getenv("TELEGRAM")

open_ai_key = os.getenv("OPEN_AI")

bot_url = "https://api.telegram.org/bot" + bot_key + "/"

open_ai_url = "https://api.openai.com/v1/images/generations"

def get_image_from_prompt(prompt):
    open_ai_data = {
        "prompt": prompt,
        "n": 1,
        "size": "512x512",
        "response_format": "b64_json"
    }
    auth_header = "Bearer " + open_ai_key
    headers = {"Content-Type": "application/json", "Authorization": auth_header}
    response = requests.post(open_ai_url, json=open_ai_data, headers=headers).json()
    if not "error" in response:
        return {"b64img": response["data"][0]["b64_json"], "created": response["created"]}
    return {"error": response["error"]["message"]}

def save_and_send_img(b64img, chat_id, prompt, timestamp):
    image_data = base64.b64decode(b64img)
    filename = f"{timestamp} - {prompt}.png"
    photos.put(filename, image_data)
    photo_payload = {"photo": image_data}
    message_url = bot_url + f"sendPhoto?chat_id={chat_id}&caption={prompt}"
    response = requests.post(message_url, files=photo_payload).json()
    return {"chat_id": chat_id, "caption": prompt}

def send_error(chat_id, error_message):
    message_url = bot_url + f"sendMessage"
    payload = {"text": error_message, "chat_id": chat_id}
    response = requests.post(message_url, json=payload).json()
    return response

def get_webhook_info():
    message_url = bot_url + "getWebhookInfo"
    response = requests.get(message_url).json()
    return response

@app.post("/open")
async def http_handler(request: Request):
    incoming_data = await request.json()
    if "message" not in incoming_data:
        print(incoming_data)
        return send_error(user_identity, "Unknown error, lol, handling coming soon")
    prompt = incoming_data['message']['text']
    user_identity = incoming_data['message']['chat']['id']
    open_ai_resp = get_image_from_prompt(prompt)
    if "b64img" in open_ai_resp:
        return save_and_send_img(open_ai_resp["b64img"], user_identity, prompt, open_ai_resp["created"])
    if "error" in open_ai_resp:
        return send_error(user_identity, open_ai_resp["error"])
    return send_error(user_identity, "Unknown error, lol, handling coming soon")

@app.get("/set_webhook")
def url_setter(request: Request):
    prog_url = os.getenv("DETA_SPACE_APP_HOSTNAME")
    set_url = bot_url + "setWebHook?url=" + "https://" + prog_url +"/open"
    resp = requests.get(set_url)
    return resp.json()

@app.get("/")
def home(request: Request):
    home_template = Template((open("index.html").read()))
    home_css = open("style.css").read()
    if not (bot_key or open_ai_key):
        return HTMLResponse(home_template.render(css=home_css, status="SETUP_ENVS"))
    response = get_webhook_info()
    if response and "result" in response and not response["result"]["url"]:
        return HTMLResponse(home_template.render(css=home_css, status="SETUP_WEBHOOK"))
    elif response and "result" in response and "url" in response["result"]:
        return HTMLResponse(home_template.render(css=home_css, status="READY"))
    else:
        return HTMLResponse(home_template.render(css=home_css, status="ERROR"))