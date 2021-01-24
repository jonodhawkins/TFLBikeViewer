import sys
sys.path.append('..')
from TFLBikeViewer.BikePointLibrary import BikePointLibrary

bpl = BikePointLibrary()
print('Is library loaded', bpl.isLoaded())
print('Loading library...')
bpl.load()
print('Is library loaded', bpl.isLoaded())
print(bpl.getBikepointInfoFromId(164))
