import threading
import time
from copy import copy
from waitress import serve
from flask import *
from message import message
import time
api = Flask(__name__)

messages = []

@api.route("/get_messages", methods="POST")
def get_messages():
    return messages

@api.route("/send_message", methods="POST")
def send_message():
    sender = request.headers.get("sender")
    message = request.headers.get("message")

    if len(message) > 16384:
        message = "Message too long"

    messages.append(message(message, time.time(), sender))

def trim_messages():
    while messages > 127:
        del messages[0]

@api.route('/')
def index():
    return "ROOT"

if __name__ == '__main__':
    serve(api, port=443)
