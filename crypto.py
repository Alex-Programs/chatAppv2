from Crypto.Cipher import ARC4
from Crypto.Hash import SHA
import time
import base64
import requests
import nettime
from random import *

class credentials():
    key = ""

def encrypt(data):
    timestamp = time.time()/256
    timestamp = round(timestamp)

    key = credentials.key
    key = bytes(key, "utf8")

    ###

    key = SHA.new(key).digest()

    arc = ARC4.new(key, drop=3072)
    return arc.encrypt(bytes(data, "utf8"))

def decrypt(data):
    key = credentials.key
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

    rand = ""

    for i in range(1, 64):
        rand = rand + str(choice(range(0, 9)))

    token = privatekey + rand

    token = encrypt(token)

    token = base64.b64encode(token)

    return token

