from Crypto.Cipher import ARC4
from Crypto.Hash import SHA
import time
import base64
import requests
from nettime import get_time

class credentials():
    key = ""

def encrypt(data):
    #timestamp acting as a nonce
    if client.globals.timeOverride:
        timestamp = get_time() / 256
        timestamp = round(timestamp)
    timestamp = time.time()/256
    timestamp = round(timestamp)

    key = credentials.key + str(timestamp)
    key = bytes(key, "utf8")

    ###

    key = SHA.new(key).digest()

    arc = ARC4.new(key, drop=3072)
    return arc.encrypt(bytes(data, "utf8"))

def decrypt(data):
    #timestamp acting as a nonce
    if client.globals.timeOverride:
        timestamp = get_time() / 256
        timestamp = round(timestamp)
    timestamp = time.time()/256
    timestamp = round(timestamp)

    key = credentials.key + str(timestamp)
    key = bytes(key, "utf8")

    ###

    key = SHA.new(key).digest()

    arc = ARC4.new(key, drop=3072)
    data = str(arc.decrypt(data))
    data = data [2:]
    data = data [:-1]
    return data

def maketoken(seed=""):
    privatekey = credentials.key + "fklflkdsfjklsjfkdjsfkljdsjflksdjfklsdjfsjfklsj" + str(seed)

    if client.globals.timeOverride:
        timestamp = get_time() / 10
        timestamp = round(timestamp)
    timestamp = time.time()/10
    timestamp = round(timestamp)

    token = privatekey + str(timestamp)

    hashedKey = SHA.new(bytes(token, "utf8")).digest()

    hashedKey = base64.b64encode(hashedKey).decode("utf8")

    return hashedKey

