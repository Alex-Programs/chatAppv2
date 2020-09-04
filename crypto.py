from Crypto.Cipher import ARC4
from Crypto.Hash import SHA
import time
import base64

def encrypt(data):
    key = b'Very long and confidential key'
    key = SHA.new(key).digest()

    arc = ARC4.new(key)
    return arc.encrypt(bytes(data, "utf8"))

def decrypt(data):
    key = b'Very long and confidential key'
    key = SHA.new(key).digest()

    arc = ARC4.new(key)
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