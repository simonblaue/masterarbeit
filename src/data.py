import numpy as np
import matplotlib.pyplot as plt
import pickle

from src import util

class RecordedData():
    def __init__(self, json_file, ) -> None:
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
        self.trj = trj
        self.id = id
        self.t = range(len(self.trj))
        self.v = np.zeros(np.shape(trj))
        self.v[:-1,:] = trj[1:,:] - trj[:-1,:]

        self.abs_v = np.linalg.norm(self.v, axis = 1)
        
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
        
        trj_array = np.hstack((self.player1.trj, self.player2.trj))
        
        with open(filename, 'wb') as outp:  # Overwrites any existing file.
           np.savetxt(filename + ".csv", trj_array, delimiter=",")

            
    def __str__(self):
        return f"{str(self.player1)}\n {str(self.player2)}"