import os
import select
import socket
import sys
import time
from termios import tcflush, TCIFLUSH

import questionBank 
import utilities 

os.system('clear')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((socket.gethostname(),12345))

def buzzer():
    print(f"\nPress buzzer before everyone else within {TIMEOUT} seconds") 
    pressed = ""

    tcflush(sys.stdin, TCIFLUSH) 

    read , _, _ = select.select([sys.stdin, client_socket],[],[], 10) 
    
    if read:
        if read[0] == sys.stdin: 
            pressed = sys.stdin.readline()
        elif read[0] == client_socket: 
            message = receive_msg(client_socket)
            print(message)
            return 
    
    else:
        print("Time's up!! Buzzer cannot be pressed!\n")

    if pressed == "":
        pressed = "false"
    send_msg(pressed, client_socket)

def answer():
    print("\nCongratulations!! You pressed the buzzer first..")
    print(f"You have {TIMEOUT} seconds to answer now\n")
    time.sleep(0.5)
    print("Enter option number")
    answer = ""

    tcflush(sys.stdin, TCIFLUSH) 

    read, _, _ = select.select([sys.stdin],[],[], 10) 
    if read:
        answer = sys.stdin.readline()
    
    else:
        print("Time's up!! You cannot answer now..\n")
    
    if answer == "":
        answer = "false"
    send_msg(answer, client_socket)   

my_username = input("Enter your username: ") 
send_msg(my_username, client_socket)

while True:
    message = receive_msg(client_socket)
    if message is False:
        continue

    if(message == "Buzzer"):
        buzzer()
    elif(message == "Answer"):
        answer()
    elif(message == "GameOver"):
        break
    else:
        print(message)

time.sleep(1)
client_socket.close()
