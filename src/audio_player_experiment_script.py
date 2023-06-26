import os
import glob
import time

import datetime
# from mplayer import Player
# player = Player()



audio_folder_path = os.path.join(os.path.dirname(__file__), '../Audios_for_Recording/')

files = list(glob.iglob(audio_folder_path+"**.m4a"))

experiment1 = {
    "player1_from": "A",
    "player1_to": "E",
    "player2_from": "C",
    "player2_to": "A"
    }


# play file 1 

# wait for keyboard input

running_exp = True
while running_exp:

    player1_from = input("Movement player 1 from: ")
    player1_to = input("To: ")

    player2_from = input("Movement player 2 from: ")
    player2_to = input("To: ")
    
    experiment = {
        "player1_from": player1_from,
        "player1_to": player1_to,
        "player2_from": player2_from,
        "player2_to": player2_to
        }

    file1 = audio_folder_path + experiment['player1_to'] + "_" + experiment['player2_to'] + ".m4a"
    file2 = audio_folder_path + experiment['player1_from'] + "_" + experiment['player2_from'] + ".m4a"

    if file1 not in files or file2 not in files:
        print("We dont have the Audio to do this expermient, they would reach the same object or an object not existing.")
        continue

    start_inp = input("To start press y")

    if start_inp == "y":
        # play file1
        # player.loadfile(file1)
        print("Started at: " + str(datetime.datetime.now()))
    elif start_inp == "q":
        print("Stopped experiment")
        break
        
    start2_inp = input("To start reach back press y")
    if start2_inp == "y":
        # play file 2
        # player.loadfile(file2)
        print("Started reach back at: " + str(datetime.datetime.now()))    
    elif start_inp == "q":
        print("Stopped experiment")
        break
