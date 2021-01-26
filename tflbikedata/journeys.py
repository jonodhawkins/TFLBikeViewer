import requests
import time
from datetime import datetime

class Journey:
    """
    Encapsulates a journey between two TFL bike points

    Methods
    -------
    loadSteps(parameters)
        Load the route from startStationId to endStationId using the provided
        routeStore and bikePoint objects
    """

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

    def loadSteps(self, bikePointStore, routeStore):
        """
        Get the positional stops along a route in latitude and longitude.

        Parameters
        ----------
        bikePointStore : BikePointStore
            Instance of a BikePointStore object (should be loaded!)
        routeStore : RouteStore
            Instance of a RouteStore object
        """

        if not bikePointStore.isLoaded():
            bikePointStore.load()

        lat, lon = routeStore.getRoute(self.startStationId, self.endStationId, bikePointStore)
        self.lat = lat
        self.lon = lon
