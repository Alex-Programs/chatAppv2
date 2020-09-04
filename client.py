import message
import requests
import time
from threading import Thread
import tkinter
import jsonpickle

from Crypto.Cipher import AES

baseUrl = "http://127.0.0.1:443"

class globals():
    messages = []

class gui():
    def __init__(self):
        self.top = tkinter.Tk()
        self.top.title("Encrypted Messenger")

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

        self.name_field = tkinter.Entry(self.top, textvariable=self.name)
        self.name_field.pack()

        self.entry_field = tkinter.Entry(self.top, textvariable=self.message)
        self.entry_field.bind("<Return>", send)
        self.entry_field.pack()
        self.send_button = tkinter.Button(self.top, text="Send", command=send)
        self.send_button.pack()

        self.top.protocol("WM_DELETE_WINDOW", on_closing)

def send(event=None):
    message = gui.message.get()
    name = gui.name.get()
    print("Sending: " + message + " : " + name)

    headers = {"message" : message, "sender" : name}
    requests.post(baseUrl + "/send_message", headers=headers)

def on_closing():
    exit()

def get_loop():
    #Yes, I know web sockets are a thing, but I'm not reading another medium article about a fast, scalabe library for them. This does the job

    while True:
        time.sleep(0.25)
        r = requests.get(baseUrl + "/get_messages").content

        print(str(r))
        unpickledmessages = jsonpickle.decode(r)

        if not unpickledmessages == globals.messages:
            globals.messages = unpickledmessages

            gui.message_list.delete(0, tkinter.END)
            for message in globals.messages:
                toAppend = message.sender + " : " + message.text
                gui.message_list.insert(tkinter.END, toAppend)

Thread(target=get_loop).start()

gui = gui()
tkinter.mainloop()