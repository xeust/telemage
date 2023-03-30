import base64
import os

import openai
import requests
from deta import Base, Drive
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Template
from pydantic import BaseModel


class New_ID(BaseModel):
    new_id: int


app = FastAPI()
app.mount("/public", StaticFiles(directory="public"), name="public")

PHOTOS = Drive("generations")
CONFIG = Base("config")

BOT_KEY = os.getenv("TELEGRAM")
OPEN_AI_KEY = os.getenv("OPEN_AI")
BOT_URL = f"https://api.telegram.org/bot{BOT_KEY}"
OPEN_AI_URL = "https://api.openai.com/v1/images/generations"

env_error = (
        not BOT_KEY
        or BOT_KEY == "enter your key"
        or not OPEN_AI_KEY
        or OPEN_AI_KEY == "enter your key"
)

openai.api_key = OPEN_AI_KEY


def get_image_from_prompt(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512",
        response_format="b64_json",
    )

    if "error" not in response:
        return {
            "b64img": response["data"][0]["b64_json"],  # type: ignore
            "created": response["created"],  # type: ignore
        }

    return {"error": response["error"]["message"]}  # type: ignore


def save_and_send_img(b64img, chat_id, prompt, timestamp):
    image_data = base64.b64decode(b64img)
    filename = f"{timestamp} - {prompt}.png"
    PHOTOS.put(filename, image_data)
    photo_payload = {"photo": image_data}
    message_url = f"{BOT_URL}/sendPhoto?chat_id={chat_id}&caption={prompt}"
    requests.post(message_url, files=photo_payload).json()
    return {"chat_id": chat_id, "caption": prompt}


def send_error(chat_id, error_message):
    message_url = f"{BOT_URL}/sendMessage"
    payload = {"text": error_message, "chat_id": chat_id}
    return requests.post(message_url, json=payload).json()


def get_webhook_info():
    message_url = f"{BOT_URL}/getWebhookInfo"
    return requests.get(message_url).json()


@app.get("/")
def home():
    home_template = Template((open("index.html").read()))

    response = get_webhook_info()

    if (env_error):
        return RedirectResponse("/setup")

    if response and "result" in response and not response["result"]["url"]:
        return RedirectResponse("/setup")

    if response and "result" in response and "url" in response["result"]:
        return HTMLResponse(home_template.render(status="READY"))

    return HTMLResponse(home_template.render(status="ERROR"))

@app.get("/setup")
def setup():
    home_template = Template((open("index.html").read()))
    if (env_error):
        return HTMLResponse(home_template.render(status="SETUP_ENVS"))
    return HTMLResponse(home_template.render(status="SETUP_WEBHOOK"))

@app.get("/authorize")
def auth():
    authorized_chat_ids = CONFIG.get("chat_ids")
    home_template = Template((open("index.html").read()))

    if authorized_chat_ids is None:
        return HTMLResponse(home_template.render(status="AUTH", chat_ids=None))

    return HTMLResponse(
        home_template.render(status="AUTH", chat_ids=authorized_chat_ids.get("value"))  # type: ignore
    )


@app.post("/authorize")
def add_auth(item: New_ID):
    if CONFIG.get("chat_ids") is None:
        CONFIG.put(data=[item.new_id], key="chat_ids")
        return

    CONFIG.update(updates={"value": CONFIG.util.append(item.new_id)}, key="chat_ids")
    return


@app.post("/open")
async def http_handler(request: Request):
    incoming_data = await request.json()

    if "message" not in incoming_data:
        print(incoming_data)
        return send_error(None, "Unknown error, lol, handling coming soon")

    prompt = incoming_data["message"]["text"]
    chat_id = incoming_data["message"]["chat"]["id"]
    authorized_chat_ids = CONFIG.get("chat_ids")

    if prompt in ["/chat-id", "/chatid"]:
        payload = {
            "text": f"```{chat_id}```",
            "chat_id": chat_id,
            "parse_mode": "MarkdownV2",
        }
        message_url = f"{BOT_URL}/sendMessage"
        requests.post(message_url, json=payload).json()
        return

    if prompt in ["/start", "/help"]:
        response_text = (
            "welcome to telemage. to generate an image with ai,"
            " send me a prompt or phrase and i'll do some magic."
        )
        payload = {"text": response_text, "chat_id": chat_id}
        message_url = f"{BOT_URL}/sendMessage"
        requests.post(message_url, json=payload).json()
        return

    if authorized_chat_ids is None or chat_id not in authorized_chat_ids.get("value"):  # type: ignore
        payload = {"text": "you're not authorized. contact this bot's admin to authorize.", "chat_id": chat_id}
        message_url = f"{BOT_URL}/sendMessage"
        requests.post(message_url, json=payload).json()
        return

    open_ai_resp = get_image_from_prompt(prompt)
    if "b64img" in open_ai_resp:
        return save_and_send_img(
            open_ai_resp["b64img"], chat_id, prompt, open_ai_resp["created"]
        )

    if "error" in open_ai_resp:
        return send_error(chat_id, open_ai_resp["error"])

    return send_error(chat_id, "Unknown error, lol, handling coming soon")


@app.get("/set_webhook")
def url_setter():
    PROG_URL = os.getenv("DETA_SPACE_APP_HOSTNAME")
    set_url = f"{BOT_URL}/setWebHook?url=https://{PROG_URL}/open"
    resp = requests.get(set_url)
    return resp.json()
