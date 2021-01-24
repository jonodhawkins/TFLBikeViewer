import sys
sys.path.append('..')
from TFLBikeViewer.CycleDataFile import CycleDataFile
from TFLBikeViewer.CycleData import CycleData

import matplotlib.pyplot as plt
import numpy as np

print("Running python", sys.version)

cData = CycleDataFile('data/195JourneyDataExtract01Jan2020-07Jan2020_Crop.csv')

fig,ax = plt.subplots();
for route in cData.cycleData:
    ax.plot(route.lat, route.lon)
fig.show()
plt.pause(3)
