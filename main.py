from src import data
from src import plotting
from src import util


import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.signal import find_peaks

def main():
    
    folder_path = "GrabbingPrimitives/recordings/2023-06-01/"

    jf = "processedAABBs.json"

    run1 = folder_path + "2023.6.1-9.32.50/" 
    run2 = folder_path + "2023.6.1-9.33.57/" 
    run3 = folder_path + "2023.6.1-9.35.7/" 
    run4 = folder_path + "2023.6.1-9.36.39/"

    cut1 = run1.replace("recordings","trajectories") + "two_trjs_cut.csv"
    cut2 = run2.replace("recordings","trajectories") + "two_trjs_cut.csv"
    cut3 = run3.replace("recordings","trajectories") + "two_trjs_cut.csv"
    cut4 = run4.replace("recordings","trajectories") + "two_trjs_cut.csv"
   
    # extract_data_and_save(run1, jf, ids=[14,8])
    # extract_data_and_save(run2, jf, ids=[]) # 4, 1
    # extract_data_and_save(run3, jf, ids=[1,2])
    # extract_data_and_save(run4, jf, ids=[1,4])
    
    cut_two_trjs(run1.replace("recordings","trajectories") + "two_trjs_raw.csv", t_idxs=[396, 733])
    # cut_two_trjs(run2.replace("recordings","trajectories") + "two_trjs_raw.csv", t_idxs=[0, 420])
    # cut_two_trjs(run3.replace("recordings","trajectories") + "two_trjs_raw.csv", t_idxs=[57, 460])
    # cut_two_trjs(run4.replace("recordings","trajectories") + "two_trjs_raw.csv", t_idxs=[147, 512])
   
    with open(cut1, "rb") as inp:
        interaction = np.loadtxt(inp, delimiter=",")
        
    t = interaction[:,0]
    trj1 = interaction[:,1:4].copy()
    trj2 = interaction[:,4:7].copy()
    
    plotting.trj_3d([trj1,trj2], labels=["player1", "player2"], legend=True)
    
    
    v1 = util.get_velocity_from_trj(trj1, t)
    v2 = util.get_velocity_from_trj(trj2, t)
    

    plotting.v_profiles([v1,v2], t)
        
    
def extract_data_and_save(folder_path, jf, ids=[]):
    
    
    rec_data1 = data.RecordedData(folder_path+jf)
    
    hand_data = rec_data1.recorded_hands

    plotting.hand_data(hand_data)
    
    if ids == []:
        id1 = int(input("First Id: "))
        id2 = int(input("Second Id: "))
    else:
        id1 = ids[0]
        id2 = ids[1]
    
    ext_data = data.ExtractedInteractionData(hand_data[id1], hand_data[id2])
    
    save_path = folder_path.replace("recordings","trajectories")
    
    if os.path.exists(save_path):
        ext_data.save(save_path+"two_trjs_raw.csv") 
    else:
        os.makedirs(save_path)
        ext_data.save(save_path+"two_trjs_raw.csv") 
    
    print(f"Saved to {save_path}two_trjs_raw.csv")


def cut_two_trjs(file_path, t_idxs):
    
    with open(file_path, "rb") as inp:
        interaction = np.loadtxt(inp, delimiter=",")
    
    t = interaction[:,0]
    trj1 = interaction[:,1:4].copy()
    trj2 = interaction[:,4:7].copy()
    
    plotting.trj_3d([trj1,trj2], labels=["player1", "player2"], legend=True)
    
    
    v1 = util.get_velocity_from_trj(trj1, t)
    v2 = util.get_velocity_from_trj(trj2, t)
    

    plotting.v_profiles([v1,v2], t)
    plt.show()
    
    if t_idxs == []:
        t_start_idx = int(input("At which index to start?"))
        t_end_idx = int(input("At which index to end?"))
    else:
        assert len(t_idxs) == 2
        t_start_idx = t_idxs[0]
        t_end_idx = t_idxs[1]
        
    save_path = json_file_path.replace("raw","cut")
    save_file = np.hstack((t[t_start_idx:t_end_idx, np.newaxis], trj1[t_start_idx:t_end_idx], trj2[t_start_idx:t_end_idx]))
    
    if os.path.exists(save_path.replace("two_trjs_cut.csv", "")):
        with open(save_path, 'wb') as outp:  # Overwrites,  any existing file.
            np.savetxt(X=save_file, fname=outp, delimiter=",", header="time, player1x, player1y, player1z, player2x, player2y, player2z")
    else:
        os.makedirs(save_path.replace("two_trjs_cut.csv", ""))
        with open(save_path, 'wb') as outp:  # Overwrites any existing file.
            np.savetxt(X=save_file, fname=outp, delimiter=",", header="time, player1x, player1y, player1z, player2x, player2y, player2z")
    
    print(f"Saved to {save_path}")

def save_each_interaction(file_path):
    with open(file_path, "rb") as inp:
        interaction = np.loadtxt(inp, delimiter=",")
        
        

if __name__ == "__main__":
    main()
    plt.show()