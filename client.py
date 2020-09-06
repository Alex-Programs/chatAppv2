import message
import requests
import time
from threading import Thread
import tkinter
from tkinter import simpledialog
import jsonpickle
from crypto import *

baseUrl = "http://192.168.0.51:443"

class globals():
    messages = []
    gui = None
    messageChangeID = "fklfklskfjs"
    lastMessageTime = 0

class gui():
    def __init__(self):
        self.top = tkinter.Tk()
        self.top.title("Encrypted Messenger")

        self.top.withdraw()
        credentials.key = simpledialog.askstring(title="Credentials Required", prompt="Please enter encryption keys: ")
        self.top.deiconify()

        self.messages_frame = tkinter.Frame(self.top)
        self.message = tkinter.StringVar() 
        self.message.set("")
        self.name = tkinter.StringVar()
        self.name.set("")
        self.scrollbar = tkinter.Scrollbar(self.messages_frame)


        self.message_list = tkinter.Listbox(self.messages_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.message_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.message_list.pack()
        self.messages_frame.pack()

        self.name_field = tkinter.Entry(self.top, textvariable=self.name, width=50)
        self.name_field.pack()

        self.entry_field = tkinter.Entry(self.top, textvariable=self.message, width=50)
        self.entry_field.bind("<Return>", send)
        self.entry_field.pack()
        self.send_button = tkinter.Button(self.top, text="Send", command=send)
        self.send_button.pack()

        self.top.protocol("WM_DELETE_WINDOW", on_closing)

def send(event=None):
    message = globals.gui.message.get()
    name = globals.gui.name.get()
    print("Sending: " + message + " : " + name)

    #OK, so encrypt() returns bytes, which requests turns to a string. The server doesn't know what to do with bytes-like data
    #with a string type. So first I go plaintext > ciphertextbytes > base64 > base64-string : internet > base64 > ciphertextbytes > plaintext
    message = base64.b64encode(encrypt(message))
    name = base64.b64encode(encrypt(name))

    print(str(message))

    headers = {"message" : message, "sender" : name}
    requests.post(baseUrl + "/send_message", headers=headers)

def on_closing():
    globals.gui.top.destroy()
    raise SystemExit

def get_loop():
    time.sleep(1)
    get()
    globals.lastMessageTime = time.time()
    while True:
        t = time.time() - globals.lastMessageTime
        toWait = 0.1 + (t/30)
        if toWait > 1.5:
            toWait = 1.5
        time.sleep(toWait)
        r = requests.get(baseUrl + "/connectivity_check").content
        if not r == globals.messageChangeID:
            print("Getting")
            get()
            globals.messageChangeID = r
            globals.lastMessageTime = time.time()

def get():
    headers = {"auth": maketoken()}

    r = requests.get(baseUrl + "/get_messages", headers=headers)

    while r.content == "401 Unauthorized":
        print("Retrying due to unauthorised")
        headers = {"auth": maketoken()}
        time.sleep(0.1)
        r = requests.get(baseUrl + "/get_messages", headers=headers)

    try:
        unpickledmessages = jsonpickle.decode(r.content)
        globals.messages = unpickledmessages
    except:
        pass

    globals.gui.message_list.delete(0, tkinter.END)
    for message in globals.messages:
        toAppend = decrypt(message.sender) + " : " + decrypt(message.text)
        globals.gui.message_list.insert(tkinter.END, toAppend)

globals.gui = gui()
Thread(target=get_loop).start()
tkinter.mainloop()
