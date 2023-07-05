import os
import glob
import time
import json

import datetime
import vlc




audio_folder_path = os.path.join(os.path.dirname(__file__), '../Audios_for_Recording/')
saves_folder_path = os.path.join(os.path.dirname(__file__), '../Exp_Documents/')

files = list(glob.iglob(audio_folder_path+"**.m4a"))


running_exp = True

experiments = {}
counter = 0

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
    
    experiments[counter] = {}

    file1 = audio_folder_path + experiment['player1_to'] + "_" + experiment['player2_to'] + ".m4a"
    file2 = audio_folder_path + experiment['player1_from'] + "_" + experiment['player2_from'] + ".m4a"
    audio_player1 = vlc.MediaPlayer(file1)
    audio_player2 = vlc.MediaPlayer(file2)

    if file1 not in files or file2 not in files:
        print("We dont have the Audio to do this expermient, they would reach the same object or an object not existing.")
        continue

    start_inp = input("To start press y")

    if start_inp == "y":
        # play file1
        audio_player1.play()
        start_time = time.time()
        experiments[counter]["reach_to"] = {}
        experiments[counter]["reach_to"]["time"] = start_time
        experiments[counter]["reach_to"]["player1"] = player1_to
        experiments[counter]["reach_to"]["player2"] = player2_to
        # audio_player1.stop()
    elif start_inp == "q":
        print("Stopped experiment")
        break
        
    start2_inp = input("To start reach back press y")
    if start2_inp == "y":
        # play file 2
        audio_player2.play()
        start_time = time.time()
        experiments[counter]["reach_back"] = {}
        experiments[counter]["reach_back"]["time"] = start_time
        experiments[counter]["reach_back"]["player1"] = player1_from
        experiments[counter]["reach_back"]["player2"] = player2_from
        # audio_player2.stop()
        # print("Started reach back at: " + str(start_time))
        
    elif start_inp == "q":
        print("Stopped experiment")
        break

    end_input = input("Continue Recording? y/n")

    if end_input == "n":
        #write file
        with open(saves_folder_path + f'{datetime.datetime.now()}.json', 'w', encoding='utf-8') as f:
            json.dump(experiments, f, ensure_ascii=False, indent=4)

        counter = 0
        experiments = {}
        print("Done recording and saved.")


    counter += 1