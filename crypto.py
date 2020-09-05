from Crypto.Cipher import ARC4
from Crypto.Hash import SHA
import time
import base64

def encrypt(data):
    #timestamp acting as a nonce
    timestamp = time.time()/10
    timestamp = round(timestamp)

    key = "Very long and confidential key" + str(timestamp)
    key = bytes(key, "utf8")

    ###

    key = SHA.new(key).digest()

    arc = ARC4.new(key, drop=3072)
    return arc.encrypt(bytes(data, "utf8"))

def decrypt(data):
    #timestamp acting as a nonce
    timestamp = time.time()/10
    timestamp = round(timestamp)

    key = "Very long and confidential key" + str(timestamp)
    key = bytes(key, "utf8")

    ###

    key = SHA.new(key).digest()

    arc = ARC4.new(key, drop=3072)
    data = str(arc.decrypt(data))
    data = data [2:]
    data = data [:-1]
    return data

def maketoken():
    privatekey = "fdsnfoisfsmfesjrf3wmj80wrwmdf8w90skfdsmfw3rjwrj30kr0kwfijesf0wfkpmeshfeisfoskfdksf"
    timestamp = time.time()/1
    timestamp = round(timestamp)

    token = privatekey + str(timestamp)

    hashedKey = SHA.new(bytes(token, "utf8")).digest()

    hashedKey = base64.b64encode(hashedKey).decode("utf8")

    return hashedKey