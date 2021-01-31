from context import tflbikedata
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np

import sys

print("Running python", sys.version)
print(tflbikedata.COPYRIGHT_STATEMENT + "\n")
print(tflbikedata.USER_STATEMENT + "\n")

# Load the BikePointStore
bpStore = tflbikedata.BikePointStore()
bpStore.load()
# Calculate number of unique stations
numStations = bpStore.getHighestId()
# Create popularity matrix
popMatrix = np.zeros((numStations, numStations))
print('Created pop matrix of size',popMatrix.shape)

# Load usage data
with open('data/usage-data-list.csv', 'r') as dataList:

    fig,ax = plt.subplots()

    # Iterate through file
    for filename in dataList:
        # Load JourneyStore
        jStore = tflbikedata.JourneyStore('data/' + filename.rstrip())
        # Show number of loaded journeys
        print('Loaded {} journeys'.format(len(jStore.journeys)))

        # Iterate over the journeys and assign to popularity matrix
        for journey in jStore.journeys:
            popMatrix[journey.startStationId, journey.endStationId] += 1

        ax.imshow(popMatrix)
        fig.savefig('img/usage_analysis_idxid.png', dpi=300)
        # input()
