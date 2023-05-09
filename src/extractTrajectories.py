import json
import numpy as np
import matplotlib.pyplot as plt


    
def calc_center_from_box(corners):
    
    assert len(corners) == 8
    
    print(corners)
    
    minx = min(corners[:,0])
    maxx = max(corners[:,0])
    miny = min(corners[:,1])
    maxy = max(corners[:,1])
    minz = min(corners[:,2])
    maxz = max(corners[:,2])

    # calculate center
    cx = (maxx-minx)/2
    cy = (maxy-miny)/2
    cz = (maxz-minz)/2
        
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
            
            
def save_traj(sourcefilename, trj, iid):
    savename = sourcefilename.replace("processedAABBs.json", "trj") + "_" + str(iid) + ".csv"
    np.savetxt(savename, trj, delimiter=",")
    
    

if __name__ == "__main__":
    json_file = "GrabbingPrimitives/recordings/rec_1/processedAABBs.json"
    iids, _ = get_all_instanceids(json_file)
    
    print(iids)
    
    
    for iid in iids:
    
        trj1 = extract_trj(json_file, iid)
    
        save_traj(json_file, trj1, iid )
    
