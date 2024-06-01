from models.messaging import Messaging
import os

# TEMP: just a test
channel = "1089098339540291627"

def display_new():
    os.system('clear')

    messages = Messaging.get_messages(channel)
    for message in messages:
        print(f'{message.get("author").get("username")}: {message.get("content")}')

    print('\n> ', end='')

Messaging.subscribe_channel(channel, display_new)   
display_new()

while True:
    message = input()
    Messaging.send_message(channel, message)