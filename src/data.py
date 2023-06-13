import numpy as np
import matplotlib.pyplot as plt
import pickle

from src import util

class RecordedData():
    def __init__(self, json_file) -> None:
        self.label_dict = util.get_all_instanceids(json_file)
        self.hand_iids = self.label_dict["hand"]
        
        
        self.recorded_hands = {}
        
        for iid in self.hand_iids:
            trj = util.extract_trj(json_file, iid)
            self.recorded_hands[iid] = RecordedInstance(trj, iid)
            
    
    def plot_pos(self):
        pass
    
class RecordedInstance():
    def __init__(self, trj, id) -> None:
        self.trj = trj[:,1:]
        self.id = id

        self.t = trj[:,0]

        
        self.v = np.zeros((len(self.t)-1,3))
        
        self.v[:,0] = (self.trj[1:,0] - self.trj[:-1,0]) * (self.t[1:] - self.t[:-1])
        self.v[:,1] = (self.trj[1:,1] - self.trj[:-1,1]) * (self.t[1:] - self.t[:-1])
        self.v[:,2] = (self.trj[1:,2] - self.trj[:-1,2]) * (self.t[1:] - self.t[:-1])

        self.abs_v = np.linalg.norm(self.v[:,1:], axis = 1)
        
        self.v_std = np.nanstd(self.abs_v)
        
        
    def __str__(self):
        return "This is the recorded instance " + str(self.id)
        
        
class ExtractedInteractionData():
    def __init__(self, player1:RecordedInstance, player2:RecordedInstance) -> None:
        self.player1 = player1
        self.player2 = player2
        
    def plot():
        pass
    
    def save(self, filename):
                
        save_file = np.hstack((self.player1.t[:,np.newaxis], self.player1.trj, self.player2.trj))
        
        with open(filename, 'w') as outp:  # Overwrites any existing file.
           np.savetxt(X=save_file, fname=outp, delimiter=",", header="time, player1x, player1y, player1z, player2x, player2y, player2z")

            
    def __str__(self):
        return f"{str(self.player1)}\n {str(self.player2)}"