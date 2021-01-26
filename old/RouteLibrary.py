# RouteLibrary.py stores route locations between station IDs
#
# Use pickle to store a dictionary that acts as a lookup

import pickle
import os
import requests
import time
from datetime import datetime

class RouteLibrary:

    APP_KEY = 'b34da350bebd4d90bc105b5d5db94507';

    def __init__(self, fileLocation, overwrite=False):

        self.numRoutes = 0

        # Save file location to object
        self.fileLocation = fileLocation

        if os.path.isfile(fileLocation):
            if not overwrite and input('{} exists.  Do you want to overwrite/add to this library? (Y/N):'.format(fileLocation)).lower() != 'y':
                exit('Unable to open {}.  Quitting.'.format(fileLocation))
            with open(fileLocation, 'rb') as libFile:
                self.data = pickle.load(libFile)
                libFile.close()
                # Iterate through data and count number of points (i.e. number
                # of routes)
                for startIdxList in self.data:
                    for endIdxList in self.data[startIdxList]:
                        self.numRoutes += 1
        else:
            # Create an empty file
            self.data = {}

    def getRoute(self, startIdx, endIdx, bikePointLib):

        # Set empty latitude and longitude lists
        lat = []
        lon = []

        if startIdx == endIdx:
            return lat, lon

        if startIdx in self.data:
            # Check whether end point exists
            startIdxList = self.data[startIdx]
            if endIdx in startIdxList:
                # Load route data
                # print('Using local lookup', startIdx, endIdx)
                lat,lon = self.__getRouteInner(startIdxList, endIdx)
                if len(lat) > 0 and len(lon) > 0:
                    return lat, lon
        # Check if reverse option exists
        elif endIdx in self.data:
            # Check whether start point exists
            endIdxList = self.data[endIdx]
            if startIdx in endIdxList:
                # Load route data
                # print('Using local lookup', startIdx, endIdx)
                lat,lon = self.__getRouteInner(endIdxList, startIdx)
                if len(lat) > 0 and len(lon) > 0:
                    return lat,lon

        # Need to load the route and store
        # Load start and end points
        startPoint = bikePointLib.getBikepointInfoFromId(startIdx);
        endPoint = bikePointLib.getBikepointInfoFromId(endIdx);

        if len(startPoint) == 0:
            print('Error loading startPoint', startIdx)
            return lat,lon
        if len(endPoint) == 0:
            print('Error loading endPoint', endIdx)
            return lat,lon

        # Get direction information
        try:
            reqURL = "https://api.tfl.gov.uk/Journey/JourneyResults/{},{}/to/{},{}?mode=cycle&app_key={}".format(
                startPoint['latitude'], startPoint['longitude'],
                endPoint['latitude'], endPoint['longitude'],
                self.APP_KEY
            )
            journeyReq = requests.get(reqURL).json()
        except KeyError:
            print('KEY ERROR')
            return lat,lon

        print('Using URL lookup', startIdx, endIdx)

        latlon = [];

        # Check whether journeys have been found
        if 'journeys' in journeyReq:
            if len(journeyReq['journeys']) > 0:
                # print('Journeys available frpm', self.startStationName, 'to', self.endStationName)#
                # Check if there are children
                journeys = journeyReq['journeys'][0]
                # Check if there are legs available
                if 'legs' in journeys:
                    # then loop over the legs
                    legs = journeys['legs']
                    for leg in legs:
                        # Add instructions to lat lon record
                        steps = leg['instruction']
                        steps = steps['steps']
                        # Loop over instructions
                        for step in steps:
                            lat.append(step['latitude'])
                            lon.append(step['longitude'])
                            latlon.append((step['latitude'], step['longitude']));
                else:
                    print('No legs available');
            else:
                print('Journeys NOT available frpm', self.startStationName, 'to', self.endStationName)

        # Update lookup table
        if startIdx in self.data:
            innerDict = self.data[startIdx]
        else:
            innerDict = {}

        innerDict[endIdx] = tuple(latlon)
        self.data[startIdx] = innerDict

        return lat,lon

    def __getRouteInner(self, startIdxList, endIdx):
        # Create empty lat and lon arrays
        lat = [];
        lon = [];
        # Loop through and return
        for pair in startIdxList[endIdx]:
            lat.append(pair[0])
            lon.append(pair[1])
        # print(lat, lon)
        return lat, lon

    def save(self):
        with open(self.fileLocation, 'wb') as libFile:
            pickle.dump(self.data, libFile)
            libFile.close()
