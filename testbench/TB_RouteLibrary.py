import sys
sys.path.append('..')
from TFLBikeViewer.RouteLibrary import RouteLibrary

# Test route library location
routeLibLoc = 'tflRouteLib.pkl'

print('Loading RouteLibrary from {}'.format(routeLibLoc))

routeLib = RouteLibrary(routeLibLoc)
