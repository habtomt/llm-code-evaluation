import tkinter as tk
from tkinter import messagebox
import threading
import time

def show_notification (sender ,message ):

    message_snippet =message [:50 ]+"..."if len (message )>50 else message

    tkinter_messagebox =messagebox .showinfo (f"New Message from {sender}",message_snippet )

def request_permission ():

    root =tk .Tk ()
    root .withdraw ()
    tkinter_messagebox =messagebox .showinfo ("Notification Permission","This application needs permission to show notifications.")
    root .destroy ()

    response =tkinter_messagebox
    if response =="OK":
        return True
    else :
        return False

def receive_new_message (sender ,message ):

    permission_granted =request_permission ()
    if permission_granted :

        show_notification (sender ,message )

def simulate_receiving_message ():
    while True :
        sender ="Alice"
        message ="Hello! How are you doing today?"
        receive_new_message (sender ,message )
        time .sleep (5 )

thread =threading .Thread (target =simulate_receiving_message )
thread .daemon =True
thread .start ()

while True :
    pass