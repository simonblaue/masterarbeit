import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import random

import numpy as np

def randomcolor():
    return "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])


def hand_data(data, savename=None):
    
    num_instances = len(data)
    
    colors = [ randomcolor() for _ in range(num_instances)]
    
    fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))
    
    for instance, color in zip(data, colors):
    
        trj = instance.trj
        ax.plot(trj[:,0],trj[:,1],trj[:,2], label=str(instance), color=color)
    
    plt.legend()
        
    if savename:
        plt.savefig("plots/" + savename + ".pdf")
        
    plt.show()
    
    return colors

def instance_trj_3d(trjs, iids, label_dict, savename=None):
    
    colors = [ randomcolor() for _ in range(len(iids))]
    
    fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))
    
    for trj, iid, color in zip(trjs,iids, colors):
    
        label = next((k for k, v in label_dict.items() if iid in v), None)
        
        ax.plot(trj[:,0],trj[:,1],trj[:,2], label=label+str(iid), color=color)
    
    plt.legend()
        
    if savename:
        plt.savefig("plots/" + savename + ".pdf")
        
    plt.show()
    
    return colors
    
    
def animate_trjs_3d(trjs, iids, label_dict, savename=None):
    fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))
    
    num_of_lines = len(trjs)
    
    
    
    colors = [randomcolor() for _ in range(num_of_lines)]
    
    num_of_frames = len(trjs[0])
    
    lines = [[] for _ in range(num_of_lines)]
    
    
    def animate(i):
            for j in range(num_of_lines):
                
                line = lines[j]
                trj = trjs[j]
                
                line.append(trj[i])
    
            for line,color in zip(lines,colors):
                xs = np.array(line)[:,0]
                ys = np.array(line)[:,1]
                zs = np.array(line)[:,2]
                
                ax.plot(xs,ys,zs, color=color)
    
    
    anim = FuncAnimation(fig, animate, interval=30)
    
    return anim

def trj_3d(trjs, labels, legend=False, savename=None):

    fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))
    
    for trj, label in zip(trjs,labels):
    
        ax.plot(trj[:,0],trj[:,1],trj[:,2], label=label)
    
    
    if legend:
        plt.legend()
        
    if savename:
        plt.savefig("plots/" + savename + ".pdf")
        
    plt.show()