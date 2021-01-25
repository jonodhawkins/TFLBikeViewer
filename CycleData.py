import requests
import time
from datetime import datetime

class CycleData:

    lastReqTime = -1;
    APP_KEY = 'b34da350bebd4d90bc105b5d5db94507';

    def __init__(self, id, duration, bikeId, endDate, endStationId, endStationName, startDate, startStationId, startStationName):
        self.id = id
        self.duration = duration
        self.bikeId = bikeId
        self.endDate = endDate
        self.endStationId = int(endStationId)
        self.endStationName = endStationName
        self.startDate = startDate
        self.startStationId = int(startStationId)
        self.startStationName = startStationName
        self.lat = [];
        self.lon = [];
        self.journeyData = [];

        # Convert endDate and startDate to datetime objects
        self.startDate = datetime.strptime(self.startDate, '%d/%m/%Y %H:%M')
        self.endDate = datetime.strptime(self.endDate, '%d/%m/%Y %H:%M')

    def loadSteps(self, bikePointLib, routeLib):

        if not bikePointLib.isLoaded():
            bikePointLib.load()

        # Load start and end points
        startPoint = bikePointLib.getBikepointInfoFromId(self.startStationId);
        endPoint = bikePointLib.getBikepointInfoFromId(self.endStationId);

        if len(startPoint) == 0:
            print('Error loading startPoint', self.startStationId)
            return
        if len(endPoint) == 0:
            print('Error loading endPoint', self.endStationId)
            return

        # print('Loading', self.startStationId, 'to', self.endStationId)

        # self.lat.append(startPoint['latitude'])
        # self.lat.append(endPoint['latitude'])
        # self.lon.append(startPoint['longitude'])
        # self.lon.append(endPoint['longitude'])

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
            return

        # Check whether there are journeys available
        self.journeyData = journeyReq;

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
                            self.lat.append(step['latitude'])
                            self.lon.append(step['longitude'])
                else:
                    print('No legs available');
            else:
                print('Journeys NOT available frpm', self.startStationName, 'to', self.endStationName)#

        # print('Added', len(self.lat), 'steps')
