import message
import requests
import time
from threading import Thread
import tkinter
from tkinter import simpledialog
import jsonpickle
from crypto import *

baseUrl = "http://86.31.173.35:443"

class globals():
    messages = []
    gui = None
    messageChangeID = "fklfklskfjs"
    lastMessageTime = 0
    channel = ""

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


        self.message_list = tkinter.Listbox(self.messages_frame, height=20, width=120, yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.message_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.message_list.pack()
        self.messages_frame.pack()

        self.name_field = tkinter.Entry(self.top, textvariable=self.name, width=120)
        self.name_field.pack()

        self.entry_field = tkinter.Entry(self.top, textvariable=self.message, width=120)
        self.entry_field.bind("<Return>", send)
        self.entry_field.pack()
        self.send_button = tkinter.Button(self.top, text="Send", command=send)
        self.send_button.pack()

        self.top.protocol("WM_DELETE_WINDOW", on_closing)

def send(event=None):
    message = globals.gui.message.get()
    globals.gui.entry_field.delete(0, tkinter.END)

    if parse_commands(message) == False:
        name = globals.gui.name.get()
        print("Sending: " + message + " : " + name)

        #OK, so encrypt() returns bytes, which requests turns to a string. The server doesn't know what to do with bytes-like data
        #with a string type. So first I go plaintext > ciphertextbytes > base64 > base64-string : internet > base64 > ciphertextbytes > plaintext
        message = base64.b64encode(encrypt(message))
        name = base64.b64encode(encrypt(name))
        channel = base64.b64encode(encrypt(globals.channel))

        print(str(message))

        headers = {"message" : message, "sender" : name, "channel" : channel}
        print(globals.channel)
        requests.post(baseUrl + "/send_message", headers=headers)

    get()

def parse_commands(message):
    i = 0
    channel = ""

    if "/ch " in message:
        message = message.strip(" ")
        channel = message[3:]
        channel = channel.strip(" ")

    if channel == "":
        return False

    else:
        globals.channel = channel
        return True

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
    print("Running get()")
    while True:
        headers = {"auth": maketoken(), "channel" : globals.channel}
        r = requests.get(baseUrl + "/get_messages", headers=headers)

        try:
            unpickledmessages = jsonpickle.decode(r.content)
            break
        except:
            print("Retrying")
            time.sleep(0.1)
            pass

    if not globals.messages == unpickledmessages:
        globals.messages = unpickledmessages
        globals.gui.message_list.delete(0, tkinter.END)

        for message in globals.messages:
            toAppend = decrypt(message.sender) + " : " + decrypt(message.text)
            globals.gui.message_list.insert(tkinter.END, toAppend)
        
        globals.gui.message_list.see(tkinter.END)

if __name__ == "__main__":
    globals.channel = "main"
    globals.gui = gui()
    Thread(target=get_loop).start()
    tkinter.mainloop()
