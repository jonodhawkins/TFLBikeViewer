import shapefile as shp
import matplotlib.pyplot as plt
import numpy as np

waterway_shp = 'osm/gis_osm_water_a_free_1.shp'
sf = shp.Reader(waterway_shp)

fig,ax = plt.subplots()
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
            ax.fill(x,y,c='#0097a9')
        fig.show()

plt.pause(60)
