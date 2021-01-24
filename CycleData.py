import requests

class CycleData:

    def __init__(self, id, duration, bikeId, endDate, endStationId, endStationName, startDate, startStationId, startStationName):
        self.id = id
        self.duration = duration
        self.bikeId = bikeId
        self.endDate = endDate
        self.endStationId = endStationId
        self.endStationName = endStationName
        self.startDate = startDate
        self.startStationId = startStationId
        self.startStationName = startStationName

        # Get start and end station locations
        reqURL = "https://api.tfl.gov.uk/BikePoint/BikePoints_{}".format(self.startStationId);
        ssReq = requests.get(reqURL).json();
        reqURL = "https://api.tfl.gov.uk/BikePoint/BikePoints_{}".format(self.endStationId);
        esReq = requests.get(reqURL).json();

        # Get direction information
        reqURL = "https://api.tfl.gov.uk/Journey/JourneyResults/{},{}/to/{},{}?mode=cycle".format(
            ssReq['lat'], ssReq['lon'], esReq['lat'], esReq['lon']
        )
        journeyReq = requests.get(reqURL).json()

        # Check whether there are journeys available
        self.journeyData = journeyReq;
        self.lat = [];
        self.lon = [];

        # Check whether journeys have been found
        if 'journeys' in journeyReq:
            if len(journeyReq['journeys']) > 0:
                print('Journeys available frpm', self.startStationName, 'to', self.endStationName)#
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

        print('Added', len(self.lat), 'steps')
