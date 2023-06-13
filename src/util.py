import numpy as np
import json

def calc_center_from_box_corners(corners):
    """Calculates the center of a 3d box from its corners

    Args:
        corners (Array): shape(8,3):\n 
       [[x1, y1, z1],\n 
        [x2, y2, z2],\n
          ⋮,   ⋮, ⋮, \n
        [x8, y8, z8]]
        

    Returns:
        List: [centerx, centery, centerz]
    """
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


def get_velocity_from_trj(trj, t):
    v = np.zeros((len(t)-1,3))    
    v[:,0] = (trj[1:,0] - trj[:-1,0]) * (t[1:] - t[:-1])
    v[:,1] = (trj[1:,1] - trj[:-1,1]) * (t[1:] - t[:-1])
    v[:,2] = (trj[1:,2] - trj[:-1,2]) * (t[1:] - t[:-1])
    return v


def get_all_instanceids(json_file):
    
    ids_set = set()
    
    class_instance_dict = {"hand": set(), "block": set(), "other":set()}
    
    with open(json_file) as json_data:
        data = json.load(json_data)
        
    for key, vals in data.items():
        if key == "NumOfFrames":
            return class_instance_dict
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
            
    return class_instance_dict



def find_key(input_dict, value):
    return next((k for k, v in input_dict.items() if value in v), None) 


def extract_trj(json_file, instanceID):

    with open(json_file) as json_data:
        trj_data = json.load(json_data)
    with open(json_file.replace("processedAABBs", "Timestamp")) as json_time_data:
        time_data = json.load(json_time_data)

    trj = np.zeros((trj_data["NumOfFrames"], 4))
    trj[:] = np.nan

    t_offset = time_data["0"]
    
    i = 0
    for key, vals in trj_data.items():
        if key == "NumOfFrames":
            return trj
                
        t = (time_data[key] - t_offset) #* 10 # *10 for seconds
        
        bounding_boxes = vals["AABBs"]
        for boxDict in bounding_boxes:
            if boxDict["InstanceID"] == instanceID:
                corners = boxDict["Vertices"]
                center = calc_center_from_box_corners(np.array(corners))
                trj[i,1:] = center
                trj[i,0] = t
        i += 1
    return trj

def extract_time_spacing(timestampfile):
    with open(timestampfile) as json_data:
        data = json.load(json_data)
        
    num_timesteps = data["NumOfFrames"]
    
    delta_ts = np.zeros(num_timesteps-1)
    
    for i in range(num_timesteps-1):
        
        delta_ts[i] = data[f"{i+1}"] - data[f"{i}"]
    return delta_ts
    