import threading
import time
from copy import copy
from waitress import serve
from flask import *
from message import message
import time
import jsonpickle

api = Flask(__name__)

class globals():
    messages = []
globals.messages.append(message("Hello", time.time(), "Server"))

@api.route("/get_messages", methods=["GET"])
def get_messages():
    return jsonpickle.encode(globals.messages)

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
