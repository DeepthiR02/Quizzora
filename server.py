import os
import select
import socket
import time

os.system("python utilities.py")
os.system("python questionBank.py")

import utilities
import questionBank

os.system('clear')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((socket.gethostname(), 12345))
s.listen(3)

print("Let's begin the game!!!!")

max_players = 3 
max_score = 5 

sockets_list = [s] 
players = {}
scores_list = {}

asked_que = [False]*len(questions_list) 
index = -1 
display_options = [] 
questions = 0 

def accept_connections():
    while len(players) < max_players: 
        conn, addr = s.accept() 
        username = receive_msg(conn) 
        if username is False:
            continue

        sockets_list.append(conn) 
        players[conn] = username 
        scores_list[username] = 0 

        print(f"Accepted new connection {addr}")
        print(f"Player username is {username}")
        send_msg("\nWaiting for other players to connect...\n", conn)


def broadcast(message):
    for connection in sockets_list:
        try:
            send_msg(message, connection)
        except:
            logging.exception('error while sending msg')
            raise

def quiz():
    global index, display_options 
    index = select_question(asked_que) 
    display_options = display_options(index) 
    broadcast(f"\nQ. {questions_list[index]}\n") 
    #time.sleep(0.5)

    option_num = 1
    for option in display_options:
        broadcast(f"{option_num}. {option}")
        option_num += 1

    broadcast("Buzzer") 

def score_table():
    time.sleep(1)
    broadcast("\nYour Scores")
    for player in scores_list:
        broadcast(f"{player} : {scores_list[player]}")

def check_answer(option, buzzer_player):
    global display_options, index
    correct = False 
    time.sleep(0.5)

    if option == "false": 
        send_msg("You get -0.5 score", buzzer_player)
    elif (49 <= ord(option[0]) <= 52): 
        option = int(option)
        correct = check_option(display_options, option, index)
   

    if correct:
        send_msg("\nYou got it right!", buzzer_player)
        send_msg("You get +1 score", buzzer_player)
        scores_list[players[buzzer_player]] += 1
    else:
        send_msg("\nOops! Wrong answer!", buzzer_player)
        send_msg("You get -0.5 score", buzzer_player)
        scores_list[players[buzzer_player]] -= 0.5

    if scores_list[players[buzzer_player]] >= max_score:
        return True
    return False


accept_connections()
time.sleep(0.5)
broadcast("All players have joined the game..")
time.sleep(1)

#Game Rules
broadcast("\nRules of the quiz are simple -") 
broadcast("You have 10 seconds to press buzzer(enter any letter or number on the keyboard).")
broadcast("The first one to press buzzer will be given the opportunity to answer")
broadcast("You have 10 seconds to answer if your answer is correct you get +1 , in all other cases -0.5")
broadcast("First one to reach 5 points will be declared as the winner")
time.sleep(5)
broadcast("\nGame is starting...")
time.sleep(0.5)

while True:

    if questions == len(questions_list):
        break

    time.sleep(2) 
    quiz() 
    questions += 1
    time.sleep(1)

    no_answers = True 
    first_player = True 

    read, _, _ = select.select(sockets_list,[],[], 10) 

    for socket in read:
        message = receiveMsg(socket)
        if first_player and message != "false":  
            buzzer_player = socket 
            first_player = False
            no_answers = False
            break

    if no_answers:
        broadcast("Oh!! Time up!!!\n")
        time.sleep(0.5)
        broadcast("Moving on...")
        continue
    else:
        for socket in sockets_list: 
            if socket != buzzer_player and socket != s:
                send_msg(f"\n{players[buzzer_player]} pressed the buzzer first..", socket)
                send_msg(f"Please wait for {players[buzzer_player]} to answer", socket)

    send_msg("Answer", buzzer_player) 

    option = receive_msg(buzzer_player) 
    if option:
        game_over = check_answer(option, buzzer_player)
    else:
        game_over = check_answer("false", buzzer_player)

    score_table() 

    if game_over:
        break

time.sleep(1)
broadcast("\nGame is over!!")

time.sleep(1)
if questions == len(questions_list):
    broadcast("Question bank is finished..")
else:
    broadcast(f"Winner is {max(scores_list, key = scores_list.get)}!!")

time.sleep(1)
broadcast("Hope you enjoyed!!\n")
broadcast("GameOver") #Indicates the client to close the connection
time.sleep(1)

s.close()
