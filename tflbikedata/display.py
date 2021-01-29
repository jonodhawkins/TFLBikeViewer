import shapefile as shp

class BackgroundMapPlotter:
    """
    Plots geographic features to matploblib axes
    """

    def __init__(self, waterwaysFile, waterwaysNames):
        """
        Loads shapefiles and asset names.

        Parameters
        ----------
        waterwaysFile : str
            Location of the shapefile containing waterway data
        waterwaysNames: str
            List of strings for the named shapes to load
        """
        self.waterwayShapes = []
        self.waterwayColour = '#a4dbe8'

        sf = shp.Reader(waterwaysFile)
        for shape in sf.shapeRecords():
            if shape.record.name in waterwaysNames:
                self.waterwayShapes.append(shape)

    def drawWaterway(self, ax):
        """
        Draws waterway filled shapefiles

        Parameters
        ----------
        ax : matploblib axes
            Axes object on which to draw waterway objects
        """
        for shape in self.waterwayShapes:
            for i in range(len(shape.shape.parts)):
                i_start = shape.shape.parts[i]
                if i==len(shape.shape.parts)-1:
                    i_end = len(shape.shape.points)
                else:
                    i_end = shape.shape.parts[i+1]
                x = [i[0] for i in shape.shape.points[i_start:i_end]]
                y = [i[1] for i in shape.shape.points[i_start:i_end]]
                ax.fill(x,y,c=self.waterwayColour, zorder=-1)

################################################################################
