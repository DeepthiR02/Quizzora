import random
import sys
import questionBank

HEADER_SIZE = 10 
IP = "127.0.0.1"
PORT = 1234
TIMEOUT = 10 

def select_question(asked_que):
    
    index = random.randrange(0, len(questions_list))

    while asked_que[index] == True:
        index = random.randrange(0, len(questions_list))

    asked_que[index] = True
    return index



def display_options(index):

    display_options = random.sample(options_list[index], 4)

    if "None of the above" in display_options: 
        display_options.remove("None of the above")
        display_options.append("None of the above")    

    return display_options


def check_option(current_options, option, index):

    if current_options[option - 1] == options_list[index][0]:
        return True
    else:
        return False


def send_msg(message, socket):
    string = message.encode("utf-8")
    string_header = f"{len(string):>{HEADER_SIZE}}".encode("utf-8")
    socket.send(string_header + string)


def receive_msg(socket):
    try:
        message_header = socket.recv(HEADER_SIZE)
        if not len(message_header):
            return False
        message_len = int(message_header.decode("utf-8").strip())
        return socket.recv(message_len).decode("utf-8")
    except KeyboardInterrupt:
        sys.exit()
    except:
        return False 
