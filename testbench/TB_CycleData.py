import sys
sys.path.append('..')
from TFLBikeViewer.CycleDataFile import CycleDataFile
from TFLBikeViewer.CycleData import CycleData
from TFLBikeViewer.BikePointLibrary import BikePointLibrary
from TFLBikeViewer.RouteLibrary import RouteLibrary
from datetime import datetime
from datetime import timedelta

import shapefile as shp

import matplotlib.pyplot as plt
import numpy as np

print("Running python", sys.version)

startDate = datetime(2020,1,3,hour=6,minute=30);
endDate = datetime(2020,1,3,hour=6, minute=40);
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

waterway_shp = 'osm/gis_osm_water_a_free_1.shp'
sf = shp.Reader(waterway_shp)
thamesShapes = []
for shape in sf.shapeRecords():
    if shape.record.name == 'River Thames':
        thamesShapes.append(shape)

for k in range(48):
    ax.clear();
    # Draw Thames
    for shape in thamesShapes:
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            x = [i[0] for i in shape.shape.points[i_start:i_end]]
            y = [i[1] for i in shape.shape.points[i_start:i_end]]
            ax.fill(x,y,c='#0097a9', zorder=1)

    # Draw Routes
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
        ax.plot(route.lon, route.lat, linewidth=0.25, zorder=2)
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
