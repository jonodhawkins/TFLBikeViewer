import sys
sys.path.append('..')
from TFLBikeViewer.RouteLibrary import RouteLibrary
from TFLBikeViewer.BikePointLibrary import BikePointLibrary
import csv
import shapefile as shp
import matplotlib.pyplot as plt
import numpy as np

# Test route library location
routeLibLoc = 'tflRouteLib.bak.pkl'

print('Loading RouteLibrary from {}'.format(routeLibLoc))

routeLib = RouteLibrary(routeLibLoc, overwrite=True)
bpl = BikePointLibrary()
bpl.load()

print('Loaded', routeLib.numRoutes, 'routes')

fig,ax=plt.subplots(figsize=(10,6))
lat = []
lon = []
num = []

scatter = []
for startIdx in routeLib.data:
    bpd = bpl.getBikepointInfoFromId(startIdx)
    if len(bpd) == 3:
        lat.append(bpd['latitude'])
        lon.append(bpd['longitude'])
        num.append(len(routeLib.data[startIdx]))
    else:
        print('No data for', startIdx)

# Draw Thames
waterway_shp = 'osm/gis_osm_water_a_free_1.shp'
sf = shp.Reader(waterway_shp)
for shape in sf.shapeRecords():
    if shape.record.name == 'River Thames':
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            x = [i[0] for i in shape.shape.points[i_start:i_end]]
            y = [i[1] for i in shape.shape.points[i_start:i_end]]
            ax.fill(x,y,c='#0097a9', zorder=1)
        fig.show()

# Draw Satter Plot
scatter = ax.scatter(x=lon, y=lat, s=num, c='#f6be00', alpha=0.5, zorder=2)
handles, labels = scatter.legend_elements(prop="sizes",alpha=1)
legend2 = ax.legend(handles, labels, loc="upper left", bbox_to_anchor=(0.9,1), title="Sizes")

ax.set(xlim=(-0.25,0.05), ylim=(51.45,51.55))

with open('routeLibCount.csv','w+') as rlCSV:
    writer = csv.writer(rlCSV, delimiter=',', quotechar='\"')
    writer.writerow(['latitude','longitude','count'])
    for idx in range(len(lat)):
        writer.writerow([lat[idx], lon[idx], num[idx]])

ax.set_title('RouteLibrary Count')
fig.savefig('img/routeLibarary_count.png', dpi=200)
