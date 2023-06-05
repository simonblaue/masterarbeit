from src import data
from src import plotting


import numpy as np

main_path = "GrabbingPrimitives/recordings/2023-06-01/"

jf = "processedAABBs.json"

jf1 = main_path + "2023.6.1-9.32.50/" + jf
jf2 = main_path + "2023.6.1-9.33.57/" + jf
jf3 = main_path + "2023.6.1-9.35.7/" + jf
jf4 = main_path + "2023.6.1-9.36.39/" + jf


def main():
    rec_data1 = data.RecordedData(jf2)
    
    hand_data = rec_data1.recorded_hands


    plotting.hand_data(hand_data)
    
    id1 = 1
    id2 = 4
    
    ext_data = data.ExtractedInteractionData(hand_data[id1], hand_data[id2])
    
    ext_data.save(main_path.replace("recordings","trajectories") + "run2")
   
    with open(main_path.replace("recordings","trajectories") + "run2.csv" , "rb") as inp:
        interaction = np.loadtxt(inp, delimiter=",")
    
    trj1 = interaction[:,0:3].copy()
    trj2 = interaction[:,3:6].copy()
    
    
    plotting.trj_3d([trj1,trj2], labels=["player1", "player2"], legend=True)

    


























if __name__ == "__main__":
    main()