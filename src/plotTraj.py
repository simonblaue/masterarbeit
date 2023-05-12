import matplotlib.pyplot as plt
import numpy as np
from extractTrajectories import *
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D


mpl.rcParams['legend.fontsize'] = 10

json_file = "GrabbingPrimitives/recordings/rec_1/processedAABBs.json"

iids, class_instances = get_all_instanceids(json_file)

fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))

for iid in iids:

    objectname = find_key(class_instances, iid)
    file = json_file.replace("processedAABBs.json", "extracted/trj") + "_" + str(iid)+ "_" + str(objectname) + ".csv"
    
    trj1 = np.loadtxt(file, delimiter=",")

    xs = trj1[:,0]
    ys = trj1[:,1]
    zs = trj1[:,2]
        

    for lab,ids in class_instances.items():
        if iid in ids:
            plot_label = lab
    
    if plot_label == "hand":
        ax.plot(xs,ys,zs, label=plot_label)
    else:
        ax.plot(xs,ys,zs)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.legend(loc="center right")
plt.savefig("plots/forhenrik.pdf")
plt.show()
