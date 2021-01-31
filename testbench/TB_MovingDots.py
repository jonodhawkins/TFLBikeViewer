from context import tflbikedata
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np

import imageio

print("Running python", sys.version)
print(tflbikedata.COPYRIGHT_STATEMENT + "\n");
print(tflbikedata.USER_STATEMENT + "\n");

print('Loading JourneyStore')
# jStore = tflbikedata.JourneyStore("data/195JourneyDataExtract01Jan2020-07Jan2020.csv")
jStore = tflbikedata.JourneyStore("data/230JourneyDataExtract02Sep2020-08Sep2020.csv")

print('Loading BikePointStore')
bpStore = tflbikedata.BikePointStore();
bpStore.load();

print('Loading RouteStore')
rStore = tflbikedata.RouteStore('tflRouteLib.pkl', overwrite=True)
print('Loaded', rStore.numRoutes,'routes')

print('Loading Background Map')
bmPlotter = tflbikedata.BackgroundMapPlotter('osm/gis_osm_water_a_free_1.shp', ['River Thames'])

# startDate = datetime(2020,1,3,hour=8,minute=30);
# endDate = datetime(2020,1,3,hour=9,minute=30);

startDate = datetime(2020,9,7,hour=13,minute=00);
endDate = datetime(2020,9,7,hour=14,minute=00);

interval = timedelta(minutes=1)
pointTime = startDate

# ongoingJourneys = jStore.filterOngoing(startDate, endDate)

colours = {
    0 : "#003d4c",
    1 : "#0097a9",
    2 : "#5a7075",
    3 : "#002855"
}
numCol = len(colours)

fig,ax = plt.subplots()

images = []

while pointTime <= endDate:

    ax.clear()
    bmPlotter.drawWaterway(ax)

    ongoingJourneys = jStore.filterOngoing(pointTime, pointTime + interval)

    latSum = []
    lonSum = []

    print('Iterating over', len(ongoingJourneys), 'journeys')
    for journey in ongoingJourneys:
        if len(journey.lat) == 0:
            journey.loadSteps(bpStore, rStore)
        lat, lon = journey.getPositionAtTime(pointTime)
        latPrev, lonPrev = journey.getPositionAtTime(pointTime - interval/2)
        if lat:
            latSum.append(lat)
            lonSum.append(lon)
            # print(colours[journey.id % numCol])
            ax.plot(journey.lon, journey.lat, c='#7d8b8f', alpha=0.9, linewidth=0.1)
            ax.scatter(x=lon, y=lat, s=1, c=colours[journey.id % numCol])
            # Add faded dots
            if latPrev:
                ax.plot([lonPrev, lon], [latPrev, lat], linewidth=0.5, alpha=0.9, c=colours[journey.id % numCol])

    rStore.save()

    print('Loaded',len(latSum), 'points')

    ax.set(xlim=(-0.2,0.00 ), ylim=(51.46,51.54))
    ax.text(
        .9,.1, pointTime.strftime('%d/%m/%Y %H:%M:%S'),
        horizontalalignment='right',
        transform=ax.transAxes
    )
    # ax.set_title(pointTime.strftime('%d/%m/%Y %H:%M:%S'))
    ax.set_axis_off()
    ds = pointTime.strftime('%d%m%Y%H%M%S')
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    # Reduce DPI to 150 from 200
    fig.savefig('img/' + ds + '_point.png', dpi=150, facecolor='#f2f2f2')

    images.append(imageio.imread('img/' + ds + '_point.png'))

    pointTime += interval
    rStore.save()

# Save GIF
imageio.mimsave(
    'img/{}_point.gif'.format(startDate.strftime('%d%m%Y%H%M%S')),
    images, duration=0.05
)
