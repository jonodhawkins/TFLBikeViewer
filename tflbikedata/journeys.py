import requests
import time
import math
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

        self.id = int(id)
        self.duration = int(duration)
        self.bikeId = bikeId
        self.endDate = endDate
        self.endStationId = int(endStationId)
        self.endStationName = endStationName
        self.startDate = startDate
        self.startStationId = int(startStationId)
        self.startStationName = startStationName
        self.lat = []
        self.lon = []
        self.journeyData = []
        self.distance = []
        self.totalDistance = 0

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

        idx = 0
        while idx < len(self.lat):
            if self.lat[idx] < 51.44:
                del self.lat[idx]
                del self.lon[idx]
            idx += 1

        # Iterate over the latitude and longitudinal data and then compute the
        # distance between
        if len(self.distance) == 0:
            idx = 1;
            while idx < len(self.lat):
                # Calculate distance
                self.distance.append(math.sqrt(
                    (self.lat[idx] - self.lat[idx-1])**2
                  + (self.lon[idx] - self.lon[idx-1])**2
                ))
                # Add total distance
                self.totalDistance += self.distance[idx-1]
                idx += 1

    def getPositionAtTime(self, time):

        lat = []
        lon = []

        # Check whether the time is valid
        if time < self.startDate or time > self.endDate:
            return lat, lon

        if not len(self.lat) or not len(self.lon):
            return lat, lon

        # Determine fractional duration
        fractDuration = (time - self.startDate).total_seconds() / self.duration

        # Iterate over individual legs
        idx = 0
        prevDistance = 0
        while idx < len(self.distance):
            # Check whether we are in the current leg
            if self.totalDistance == 0:
                cFractDistance = 0
            else:
                cFractDistance = (prevDistance+self.distance[idx])/self.totalDistance

            if cFractDistance >= fractDuration:
                if self.distance[idx] == 0:
                    subFractDistance = 0;
                else:
                    subFractDistance = (  fractDuration * self.totalDistance
                                    - prevDistance) / (self.distance[idx])
                # Calculate offset
                lat =   self.lat[idx] + (self.lat[idx+1] - self.lat[idx]) \
                                      * subFractDistance
                lon =   self.lon[idx] + (self.lon[idx+1] - self.lon[idx]) \
                                      * subFractDistance
                return lat, lon

            # Add current distance to total
            prevDistance += self.distance[idx]
            # Increment counter
            idx += 1

        return self.lat[-1], self.lon[-1]
