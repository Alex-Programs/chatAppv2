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
    
    messageChangeID = '''<head>
    <meta http-equiv='refresh' content='0; URL=https://www.youtube.com/watch?v=oHg5SJYRHA0'>
    </head>'''

    pastAuthentications = []

def encodeAndEncryptMessages(channel):
    resp = []
    for m in globals.messages:
        if m.channel == channel:
            resp.append(message(encrypt(m.text), time.time(), encrypt(m.sender), encrypt(m.channel)))

    resp = jsonpickle.encode(resp)

    return resp

def check_token(token):
    token = decrypt(base64.b64decode(token))

    if credentials.key in token:
        if token not in globals.pastAuthentications:
            return True

        else:
            return False

    else:
        return False

#not actually a connectivity check, but hey, it looks like one
@api.route("/connectivity_check", methods=["GET"])
def connectivity_check():
    return str(globals.messageChangeID) + " CONNECTIVITY OK"

#for when your friend's NTP server is fucked and you can't be arsed to fix it
@api.route("/get_time", methods=["GET"])
def get_time():
    return str(time.time())

@api.route("/get_messages", methods=["GET"])
def get_messages():
    auth = request.headers.get("auth").strip("\n").strip("\t")
    channel = request.headers.get("channel")

    if check_token(auth):
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
    return """<head>
    <meta http-equiv='refresh' content='0; URL=https://www.youtube.com/watch?v=oHg5SJYRHA0'>
    </head>"""

if __name__ == '__main__':
    globals.messages.append(message("Server Startup successful", time.time(), "Server", "main"))
    serve(api, port=443)
