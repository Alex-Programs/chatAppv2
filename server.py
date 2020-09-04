import threading
import time
from copy import copy
from waitress import serve
from flask import *
from message import message
import time
import jsonpickle
from crypto import *

api = Flask(__name__)

class globals():
    messages = []
    key = "hello world"

globals.messages.append(message("Hello", time.time(), "Server"))

def encodeAndEncryptMessages():
    resp = []
    for m in globals.messages:
        resp.append(message(encrypt(m.text), time.time(), encrypt(m.sender)))

    resp = jsonpickle.encode(resp)

    return resp

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

    if len(text) > 16384:
        text = "Message too long"

    globals.messages.append(message(text, time.time(), sender))

    trim_messages()

    return "200 OK"

def trim_messages():
    while len(globals.messages) > 14:
        del globals.messages[0]

@api.route('/')
def index():
    return "ROOT"

if __name__ == '__main__':
    serve(api, port=443)
