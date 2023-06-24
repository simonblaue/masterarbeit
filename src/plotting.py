import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import random
import numpy as np
import json

def randomcolor():
    return "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])


def hand_data(data, savename=None):
    
    num_instances = len(data)
    
    colors = [ randomcolor() for _ in range(num_instances)]
    
    fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))
    
    for instance, color in zip(data.values(), colors):
        
        trj = instance.trj
        ax.plot(trj[:,0],trj[:,1],trj[:,2], label=instance.id, color=color)
    
    plt.legend()
        
    if savename:
        plt.savefig("plots/" + savename + ".pdf")
        
    
    
    fig = plt.figure()
    for instance, color in zip(data.values(), colors):
        plt.plot(instance.t[:-1] , instance.abs_v, label=instance.id, color=color)
    
    plt.legend()
    
    
    plt.show(block=False)
    plt.pause(0.001)
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
        
    plt.show(block=False)
    plt.pause(0.001)
    
    return colors
    
    
def animate_trjs_3d(trjs, savename=None, show=False, delta_t=30):
    fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))
    
    num_of_lines = len(trjs)
    
    
    
    colors = [randomcolor() for _ in range(num_of_lines)]
    
    num_of_frames = len(trjs[0])
    print(num_of_frames)
    
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
    
    
    anim = FuncAnimation(fig, animate, interval=delta_t, frames=num_of_frames)
    
    if show:
        plt.show()
    
    return anim

def trj_3d(trjs, labels, legend=False, savename=None):

    fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))
    
    for trj, label in zip(trjs,labels):
    
        ax.plot(trj[:,0],trj[:,1],trj[:,2], label=label)
        ax.scatter(trj[0,0], trj[0,1], trj[0,2], marker='o', color="black", label="Start")
        ax.scatter(trj[-1,0], trj[-1,1], trj[-1,2], marker='x', color='red', label="End")
    
    
    if legend:
        plt.legend()
        
    if savename:
        plt.savefig("plots/" + savename + ".pdf")
        
    plt.show(block=False)
    plt.pause(0.001)
    
    
def v_profiles(vs, t):
    
    fig, ax = plt.subplots(layout='constrained')
    ax2 = ax.twiny()
    ax.set_xlabel('Time [seconds]')
    ax.set_ylabel('Abs. Velocity [m/s]')
    
    for v in vs:
        v_abs = np.linalg.norm(v, axis=1)
        ax.plot(t[:-1], v_abs)
        ax2.plot(range(len(t)-1), v_abs)
    

    ax2.set_xlabel('Time [steps]')
    # ax2.cla()
    


    plt.show(block=False)
    plt.pause(0.001)
    
def one_interaction(json_file, id, save=False):
    
    with open(json_file, 'r') as f:
        interactions = json.load(f)
    
    interaction = interactions[str(id)]
    
    trj1 = np.array(interaction["trj1"])
    trj2 = np.array(interaction["trj2"])
    #t = np.array(interaction["t"])
    
    _, ax = plt.subplots(subplot_kw=dict(projection="3d"))
    
    ax.plot(trj1[:,0], trj1[:,1], trj1[:,2], label="Player 1")
    ax.plot(trj2[:,0], trj2[:,1], trj2[:,2], label="Player 2")
    
    
    ax.scatter(trj1[0,0], trj1[0,1], trj1[0,2], marker='o', color="black", label="Start")
    ax.scatter(trj1[-1,0], trj1[-1,1], trj1[-1,2], marker='x', color='red', label="End")
    
    ax.scatter(trj2[0,0], trj2[0,1], trj2[0,2], marker='o', color="black")
    ax.scatter(trj2[-1,0], trj2[-1,1], trj2[-1,2], marker='x', color='red')
    
    # ax.legend([line1, line2, start1, end1], ["Player 1", "Player 2", "Start", "End"])

    ax.legend()    
    plt.show(block=False)
    plt.pause(0.001)
    