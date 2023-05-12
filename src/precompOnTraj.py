import numpy as np

import matplotlib.pyplot as plt

from scipy.signal import argrelmin

def get_velocity(trj, dt = 1):
    v = np.zeros(np.shape(trj))
    v[:-1,:] = trj[1:,:] - trj[:-1,:]
    return v



if __name__ == "__main__":
    
    filepath = "GrabbingPrimitives/recordings/rec_1/extracted/trj_1_hand.csv"

    handtrj = np.loadtxt(filepath, delimiter=",")
    v = get_velocity(handtrj)
    v_abs = np.linalg.norm(v, axis=1)
    
    t = np.linspace(0,1, len(v_abs))
    
    signal_lows_at_t = argrelmin(v_abs, order=50)
    # fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))
    
    plt.plot(t, v_abs)
    plt.scatter(t[signal_lows_at_t], v_abs[signal_lows_at_t], color="red")
    
    plt.show()