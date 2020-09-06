import threading
import time
from copy import copy
from waitress import serve
from flask import *
from message import message
import time
import jsonpickle
from crypto import *
import base64
from random import *

api = Flask(__name__)

credentials.key = input("Key: ")

class globals():
    messages = []
    messageChangeID = "kafjl"

def encodeAndEncryptMessages(channel):
    resp = []
    for m in globals.messages:
        if m.channel == channel:
            resp.append(message(encrypt(m.text), time.time(), encrypt(m.sender), encrypt(m.channel)))

    resp = jsonpickle.encode(resp)

    return resp

#not actually a connectivity check, but hey, it looks like one
@api.route("/connectivity_check", methods=["GET"])
def connectivity_check():
    return str(globals.messageChangeID) + " CONNECTIVITY OK"

@api.route("/get_messages", methods=["GET"])
def get_messages():
    auth = request.headers.get("auth").strip("\n").strip("\t")
    channel = request.headers.get("channel")

    if auth == maketoken():
        return encodeAndEncryptMessages(channel)
    else:
        print("UNAUTHORISED CONNECTION")
        return "401 Unauthorized"

@api.route("/send_message", methods=["POST"])
def send_message():
    sender = request.headers.get("sender")
    text = request.headers.get("message")
    channel = request.headers.get("channel")

    sender = decrypt(base64.b64decode(sender))
    text = decrypt(base64.b64decode(text))
    channel = decrypt(base64.b64decode(channel))

    print(str(sender) + " : " + str(channel) + " : " + str(text))    

    if len(text) > 4096:
        text = "Message too long"

    if "/wipe" in text:
        globals.messages = []
    else:
        globals.messages.append(message(text, time.time(), sender, channel))

    globals.messageChangeID = choice(range(1,99999))
    return "200 OK"

@api.route('/')
def index():
    return "ROOT"

if __name__ == '__main__':
    globals.messages.append(message("Server Startup successful", time.time(), "Server", "main"))
    api.run()
