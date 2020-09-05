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

class globals():
    messages = []
    messageChangeID = "kafjl"

def encodeAndEncryptMessages():
    resp = []
    for m in globals.messages:
        resp.append(message(encrypt(m.text), time.time(), encrypt(m.sender)))

    resp = jsonpickle.encode(resp)

    return resp

#not actually a connectivity check, but hey, it looks like one
@api.route("/connectivity_check", methods=["GET"])
def connectivity_check():
    return str(globals.messageChangeID) + " CONNECTIVITY OK"

@api.route("/get_messages", methods=["GET"])
def get_messages():
    auth = request.headers.get("auth").strip("\n").strip("\t")

    if auth == maketoken():
        return encodeAndEncryptMessages()
    else:
        print("UNAUTHORISED CONNECTION")
        return "401 Unauthorized"

@api.route("/send_message", methods=["POST"])
def send_message():
    sender = request.headers.get("sender")
    text = request.headers.get("message")

    sender = decrypt(base64.b64decode(sender))
    text = decrypt(base64.b64decode(text))

    print(str(sender) + " : " + str(text))    

    if len(text) > 16384:
        text = "Message too long"

    globals.messages.append(message(text, time.time(), sender))

    trim_messages()

    if "/wipe" in text:
        globals.messages = []
        globals.messages.append(message("Hello", time.time(), "Server"))

    globals.messageChangeID = choice(range(1,99999))
    return "200 OK"

def trim_messages():
    while len(globals.messages) > 14:
        del globals.messages[0]

@api.route('/')
def index():
    return "ROOT"

if __name__ == '__main__':
    globals.messages.append(message("Server Startup successful", time.time(), "Server"))
    serve(api, port=443, channel_timeout=1024, threads=512)
