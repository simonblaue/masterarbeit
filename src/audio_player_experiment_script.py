import os
import glob
import time
import json

import datetime
import vlc


audio_folder_path = os.path.join(os.path.dirname(__file__), '../Audios_for_Recording/')
saves_folder_path = os.path.join(os.path.dirname(__file__), '../Exp_Documents/')
files = list(glob.iglob(audio_folder_path+"**.m4a"))

with open(os.path.join(os.path.dirname(__file__), 'exps.json')) as f:

    exp_list = json.load(f)


def manual_run():
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


def auto_run():
    
    start = input("Start y/n?")
    experiments = {}

    if start == "y":

        for exps in exp_list.keys():
            experiments[exps] = {}
            print(f"Startet exp {exps}")
            for run in exp_list[exps]:
                experiments[exps][run] = {}
                file1 = audio_folder_path + exp_list[exps][run]['player1_to'] + "_" + exp_list[exps][run]['player2_to'] + ".m4a"
                file2 = audio_folder_path + exp_list[exps][run]['player1_from'] + "_" + exp_list[exps][run]['player2_from'] + ".m4a"
                audio_player1 = vlc.MediaPlayer(file1)
                audio_player2 = vlc.MediaPlayer(file2)

                go_on = input("Continue? y/n")
                if go_on=="y":
                    # reach to
                    audio_player1.play()
                    start_time = time.time()
                    experiments[exps][run]["reach_to"] = {}
                    experiments[exps][run]["reach_to"]["time"] = start_time
                    experiments[exps][run]["reach_to"]["player1"] = exp_list[exps][run]['player1_to']
                    experiments[exps][run]["reach_to"]["player2"] = exp_list[exps][run]['player2_to']
                else:
                    with open(saves_folder_path + f'{datetime.datetime.now()}.json', 'w', encoding='utf-8') as f:
                        json.dump(experiments, f, ensure_ascii=False, indent=4)
                    print("Done recording and saved.")
                    return
                
                go_on = input("Continue? y/n")
                if go_on=="y":
                    # reach back
                    audio_player2.play()
                    start_time = time.time()
                    experiments[exps][run]["reach_back"] = {}
                    experiments[exps][run]["reach_back"]["time"] = start_time
                    experiments[exps][run]["reach_back"]["player1"] = exp_list[exps][run]['player1_from']
                    experiments[exps][run]["reach_back"]["player2"] = exp_list[exps][run]['player2_from']

                else:
                    with open(saves_folder_path + f'{datetime.datetime.now()}.json', 'w', encoding='utf-8') as f:
                        json.dump(experiments, f, ensure_ascii=False, indent=4)
                    print("Done recording and saved.")
                    return

        with open(saves_folder_path + f'{datetime.datetime.now()}.json', 'w', encoding='utf-8') as f:
            json.dump(experiments, f, ensure_ascii=False, indent=4)
            print("Done recording and saved.")


if __name__ == "__main__":
    mode = input("Which mode? auto / manual ?")

    if mode == "auto":
        auto_run()

    if mode == "manual":
        manual_run()
