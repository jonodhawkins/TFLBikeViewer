import requests
import time
from datetime import datetime

class CycleData:

    lastReqTime = -1;

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

        lat, lon = routeLib.getRoute(self.startStationId, self.endStationId, bikePointLib)
        self.lat = lat
        self.lon = lon
        # print('Found lat', len(self.lat), 'lon', len(self.lon))

        # print('Added', len(self.lat), 'steps')
