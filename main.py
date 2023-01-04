import os
import json
import requests
from fastapi import FastAPI, Request

app = FastAPI()


bot_key = os.getenv("TELEGRAM") or ""

bot_url = "https://api.telegram.org/bot" + bot_key + "/"


def build_response(user_input):
    preamble = "Space takes: " + '\n\n' + user_input + '\n\n'
    gap = "Space gives: " + '\n\n' + user_input[::-1] + '\n\n'
    response = """
I, DETA Space, dreamt I was a friendly personal computer, easily shipping apps for developers 
with ideas which were grounded. I could easily bring these ideas past the spirit of gravity 
and above large and unfriendly clouds. Everything about me worked, and I didn't need configuration.
                
Then, I awoke, and realized again I was DETA Space, a cloud unlike any personal computer. 
I was natively integrated with the Intergalactic Planetary Network. I could be scheduled 
to work for a human even after they shut down their terminal. My programs were 'liquid' 
as never before, as personal apps became collaborative, and collaborative apps personal, 
at the flick of a switch.
                
Now I do not know whether I am a personal computer, which dreamt I was above the 
clouds, or I am a cloud, above all personal computers. Between a personal computer 
and a cloud there is a blurring distinction."""
    return preamble + gap + response


def preprocess(data):
    user_input = data['message']['text']
    response_text = build_response(user_input)
    user_identity = data['message']['chat']['id']
    json_response = {
        "chat_id": user_identity,
        "text": response_text,
    }
    return json_response


def send_message(preprocessed_data):  
    message_url = bot_url + 'sendMessage'
    requests.post(message_url, json=preprocessed_data)


@app.post("/open")
async def http_handler(request: Request):
    incoming_data = await request.json()
    answer_data = preprocess(incoming_data)
    send_message(answer_data)
    return {}


@app.get("/")
def url_setter(request: Request):
    prog_url = os.getenv("DETA_SPACE_APP_HOSTNAME") or ""
    set_url = bot_url + "setWebHook?url=" + "https://" + prog_url +"/open"
    resp = requests.get(set_url)
    return resp.json()