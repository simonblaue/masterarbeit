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


def get_velocity_from_trj(trj, dt = 1):
    v = np.zeros(np.shape(trj))
    v[:-1,:] = trj[1:,:] - trj[:-1,:]
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
                center = calc_center_from_box_corners(np.array(corners))
                trj[i,:] = center
        i += 1
    return trj