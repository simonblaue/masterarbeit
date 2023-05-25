import numpy as np
import matplotlib.pyplot as plt

from src import util

class RecordedData():
    def __init__(self, json_file, ) -> None:
        self.label_dict = util.get_all_instanceids(json_file)
        self.hand_iids = self.label_dict["hand"]
        
        self.recorded_hands = []
        
        for iid in self.hand_iids:
            trj = util.extract_trj(json_file, iid)
            self.recorded_hands.append(RecordedInstance(trj, iid))
            
    
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
    def __init__(self, trj1, trj2, v1, v2) -> None:
        self.trj1 = trj1
        self.trj2 = trj2
        self.v1 = v1
        self.v2 = v2
        
    def plot():
        pass