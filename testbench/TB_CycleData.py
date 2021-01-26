import sys
sys.path.append('..')
from TFLBikeViewer.CycleDataFile import CycleDataFile
from TFLBikeViewer.CycleData import CycleData
from TFLBikeViewer.BikePointLibrary import BikePointLibrary
from TFLBikeViewer.RouteLibrary import RouteLibrary
from datetime import datetime
from datetime import timedelta

import matplotlib.pyplot as plt
import numpy as np

print("Running python", sys.version)

startDate = datetime(2020,1,2,hour=17,minute=40);
endDate = datetime(2020,1,2,hour=17, minute=50);
cData = CycleDataFile('data/195JourneyDataExtract01Jan2020-07Jan2020.csv')
bpl = BikePointLibrary()
bpl.load()
rl = RouteLibrary('tflRouteLib.pkl', overwrite=True)
print('Pre-loaded', rl.numRoutes, 'routes')

print('Testing bikepoint load')
print(len(bpl.latitude))
idxmax = max(bpl.latitude.keys())

count = np.zeros([idxmax, idxmax], dtype=np.int16)

fig,ax = plt.subplots()
for k in range(48):
    ax.clear();
    ax.set(xlim=(-0.25,0.05), ylim=(51.45,51.55))
    ax.set_title(startDate.strftime('%d/%m/%Y %H:%M:%S'))
    cDataFilt = cData.filter(startDate, endDate);
    print('Loading', len(cDataFilt), 'tracks for', startDate)
    for route in cDataFilt:
        route.loadSteps(bpl, rl)
        # instead of loading steps, lets add them to a matrix and count the number
        # of journeys
        # if route.startStationId <= route.endStationId:
        #     count[route.startStationId, route.endStationId] += 1
        # else:
        #     count[route.endStationId, route.startStationId] += 1
        # print('Route len',len(route.lat), len(route.lon))
        # print(route.lat)
        # print(route.lon)
        ax.plot(route.lon, route.lat, linewidth=0.25)
        # input()
    rl.save()

    ds = startDate.strftime('%d%m%Y%H%M%S')
    fig.savefig('img/' + ds + '_timelapse.png', dpi=200)
    startDate += timedelta(minutes=10);
    endDate += timedelta(minutes=10);


print(np.sum(np.sum(count)))

# ax.imshow(np.log10(count+1), interpolation='none');

now = datetime.now()
ds = now.strftime('%d%m%Y%H%M%S')
fig.savefig('img/' + ds + '_test.png', dpi=400)
