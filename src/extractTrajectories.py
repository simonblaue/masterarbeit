import json
import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import argrelmin

def get_velocity(trj, dt = 1):
    v = np.zeros(np.shape(trj))
    v[:-1,:] = trj[1:,:] - trj[:-1,:]
    return v
    
def calc_center_from_box(corners):
    
    assert len(corners) == 8
        
    minx = min(corners[:,0])
    maxx = max(corners[:,0])
    miny = min(corners[:,1])
    maxy = max(corners[:,1])
    minz = min(corners[:,2])
    maxz = max(corners[:,2])

    # calculate center
    cx = (maxx+minx)/2
    cy = (maxy+miny)/2
    cz = (maxz+minz)/2
        
    return [cx, cy, cz]

def extract_trj(json_file, instanceID = 1):

    with open(json_file) as json_data:
        data = json.load(json_data)

    trj = np.zeros((len(data.keys())-1, 3))
    trj[:] = np.nan

    i = 0
    for key, vals in data.items():
        if key == "NumOfFrames":
            return trj
        bounding_boxes = vals["AABBs"]
        for boxDict in bounding_boxes:
            if boxDict["InstanceID"] == instanceID:
                corners = boxDict["Vertices"]
                center = calc_center_from_box(np.array(corners))
                trj[i,:] = center
        i += 1
    return trj



def get_all_instanceids(json_file):
    
    ids_set = set()
    
    class_instance_dict = {"hand": set(), "block": set(), "other":set()}
    
    with open(json_file) as json_data:
        data = json.load(json_data)
        
    for key, vals in data.items():
        if key == "NumOfFrames":
            return ids_set, class_instance_dict
        bounding_boxes = vals["AABBs"]
        for boxDict in bounding_boxes:
            iid = boxDict["InstanceID"]
            ids_set.add(iid)
            if boxDict["ClassID"] == 1:
                class_instance_dict["hand"].add(iid)
            elif boxDict["ClassID"] == 2:
                class_instance_dict["block"].add(iid)
            else:
                class_instance_dict["other"].add(iid)
            
    return ids_set, class_instance_dict
            
            
            
def find_key(input_dict, value):
    return next((k for k, v in input_dict.items() if value in v), None)            

def save_traj(sourcefilename, trj, iid):
    savename = sourcefilename.replace("recordings", "trajectories").replace("processedAABBs.json", "trj") + "_" + str(iid) + ".csv"
    np.savetxt(savename, trj, delimiter=",", header="x, y, z, vx, vy, vz")
    print(f"Saved to {savename}")
    
    
def ectract_from_jsonfiles(json_files, plot=False):
    
    for jf in json_files:
        if plot: fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))
    
        iids, classNameDict = get_all_instanceids(jf)
        
        for iid in iids:
            
            object = find_key(classNameDict, iid)
            
            if object == "hand":
                trj_full = extract_trj(jf, iid)
                v = get_velocity(trj_full)
                
                v_abs = np.linalg.norm(v, axis=1)
    
                t = np.linspace(0,1, len(v_abs))
    
                signal_lows_at_t = argrelmin(v_abs, order=50)
                
                i = 0
                
                for startidx, endidx in zip(signal_lows_at_t[0][:-1:2], signal_lows_at_t[0][1::2]):
                
                    trj_extracted = trj_full[startidx:endidx, :]
                    
                    if plot : ax.plot(trj_extracted[:,0], trj_extracted[:,1], trj_extracted[:,2], label=i)
                    
                    savedata = np.hstack((trj_full[startidx:endidx, :], v[startidx:endidx, :]))
                
                    save_traj(jf, savedata, i)
                    
                    i+=1
                    
        if plot:          
            plt.legend()        
            plt.show()
    

if __name__ == "__main__":
    
    jf1 = "GrabbingPrimitives/recordings/rec_1/processedAABBs.json"
    jf2 = "GrabbingPrimitives/recordings/rec_2/processedAABBs.json"
    jf3 = "GrabbingPrimitives/recordings/rec_3/processedAABBs.json"
    jf4 = "GrabbingPrimitives/recordings/rec_4/processedAABBs.json"
    
    json_files = [jf1, jf2, jf3, jf4]
    
    ectract_from_jsonfiles(json_files, True)
    
    
    
                
            
    
