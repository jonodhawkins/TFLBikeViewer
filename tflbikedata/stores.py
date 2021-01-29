# Imports
import pickle
import os
import requests
import re
import csv
import numpy as np
import tflbikedata
import json

# RouteStore
class RouteStore:
    """
    A class used to store route information (lat and lon steps from startIdx to
    endIdx).
    ---
    Attributes
    ----------
    APP_KEY : str
        File location of a text file containing the TFL application key. This
        should not be included in any repository.

    numRoutes : int
        Number of routes that have been loaded into the RouteStore file.
        TODO: Make sure that this is dynamically updated

    fileLocation : str
        The location of the file to load the RouteStore from.  If the file does
        not exist, then it will only be created on .save()

    """

    APP_KEY = "APP_KEY.txt";
    APP_KEY_VALUE = None;

    def __init__(self, fileLocation, overwrite):
        """
        Parameters
        ----------
        fileLocation : str
            Location of the RouteStore pickle data
        overwrite : boolean (default = False)
            Whether to present the user with a Y/N command line input
        """

        self.numRoutes = 0
        # Save file location to object
        self.fileLocation = fileLocation

        # Try to load application key
        try:
            with open(self.APP_KEY, 'r') as app_key_file:
                self.APP_KEY_VALUE = app_key_file.readline().strip()
                if len(self.APP_KEY_VALUE) < 1:
                    exit('Unable to load application key from ' + self.APP_KEY)
        except IOError:
            exit('Unable to load application key from ' + self.APP_KEY)

        print('Loaded application key', self.APP_KEY_VALUE)

        # Check whether the file specified exists
        if os.path.isfile(fileLocation):
            if not overwrite and input('{} exists.  Do you want to overwrite/add to this library? (Y/N):'.format(fileLocation)).lower() != 'y':
                # Quit
                exit('Unable to open {}.  Quitting.'.format(fileLocation))
            with open(fileLocation, 'rb') as libFile:
                self.data = pickle.load(libFile)
                libFile.close()
                # Iterate through data and count number of points (i.e. number
                # of routes)
                for startIdxList in self.data:
                    for endIdxList in self.data[startIdxList]:
                        self.numRoutes += 1
        # If the file does not exist, then make an empty list
        else:
            # Create an empty file
            self.data = {}

    def getRoute(self, startIdx, endIdx, bikePointStore):
        """
        Parameters
        ----------
        startIdx : int
            The numerical ID for the bike station at which the journey starts.
        endIdx : int
            The numerical ID for the bike station at which the journey ends.
        bikePointStore : BikePointStore
            Instance of the BikePointStore class which contains the lookup
            table for the location of TFL bike points by numerical ID.
        """

        # Set empty latitude and longitude lists (to be returned at any point
        # throughout execution to avoid returning NoneType)
        lat = []
        lon = []

        # If the journey starts and ends at the same point then we have no
        # information so ignore it.
        if startIdx == endIdx:
            return lat, lon

        # Otherwise check whether the starting point exists
        if startIdx in self.data:
            # If it does then check whether end point exists
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
        startPoint = bikePointStore.getBikepointInfoFromId(startIdx);
        endPoint = bikePointStore.getBikepointInfoFromId(endIdx);

        if len(startPoint) == 0:
            print('Error loading startPoint', startIdx)
            return lat,lon
        if len(endPoint) == 0:
            print('Error loading endPoint', endIdx)
            return lat,lon

        # Get direction information
        try:
            # NOTE: Specifying cyclePreference=cycleHire seems to prevent a
            # 500 return code (NullReferenceException) - weird...
            reqURL = "https://api.tfl.gov.uk/Journey/JourneyResults/{},{}/to/{},{}?mode=cycle&cyclePreference=cycleHire&app_key={}".format(
                startPoint['latitude'], startPoint['longitude'],
                endPoint['latitude'], endPoint['longitude'],
                self.APP_KEY_VALUE
            )
            journeyReqTxt = requests.get(reqURL)
            journeyReq = journeyReqTxt.json()
        except KeyError:
            print('KEY ERROR')
            return lat,lon
        except json.decoder.JSONDecodeError:
            print('JSON ERROR')
            print(journeyReqTxt)
            return lat,lon

        # Check for disambiguation errors
        if 'fromLocationDisambiguation' in journeyReq:
            print('disambiguation error for ', startPointIdx)
            return lat,lon

        if 'toLocationDisambiguation' in journeyReq:
            print('disambiguation error for ', endPointIdx)
            return lat,lon

        print('Using URL lookup', startIdx, endIdx)

        latlon = [];

        # Check whether journeys have been found
        if 'journeys' in journeyReq:
            if len(journeyReq['journeys']) > 0:
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
                print('Journeys NOT available frpm',
                        self.startStationName,
                        'to',
                        self.endStationName
                     )

        # Update lookup table
        if startIdx in self.data:
            innerDict = self.data[startIdx]
        else:
            innerDict = {}

        innerDict[endIdx] = tuple(latlon)
        self.data[startIdx] = innerDict

        return lat,lon

    def save(self):
        """
        Save the RouteStore object to the location specified in
        self.fileLocation
        """
        with open(self.fileLocation, 'wb') as libFile:
            pickle.dump(self.data, libFile)
            libFile.close()

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

################################################################################

class BikePointStore:
    """
    Stores positional (latitude, longitude) data for TFL bike points, sorted by
    numerical ID.

    Methods
    -------
    isLoaded : boolean
        Returns whether there are bike points available in the BikePointStore
        object

    getBikepointInfoFromId : dict
        Returns a dictionary containing the position and name for a given bike
        point ID.
            'latitude'  : float
            'longitude' : float
            'name'      : str
    """

    def __init__(self):
        self.latitude = {}
        self.longitude = {}
        self.name = {}

    # Check whether the bike arrays have been populated
    def isLoaded(self):
        if len(self.latitude) and len(self.longitude) and len(self.name):
            return True
        else:
            return False

    def getBikepointInfoFromId(self, id):
        # Check whether bike point exists
        if id in self.latitude and id in self.longitude and id in self.name:
            return {
                'latitude'  : self.latitude[id],
                'longitude' : self.longitude[id],
                'name'      : self.name[id]
            }
        else:
            return {}

    def load(self):
        # Make request
        bikePoints = requests.get('https://api.tfl.gov.uk/BikePoint/').json();
        # Iterate over response
        for bp in bikePoints:
            # Split name into numeric id
            idText = bp['id'].split('_')
            id = int(idText[1]);
            # Assign parameters
            self.name[id] = bp['commonName'];
            self.latitude[id] = bp['lat']
            self.longitude[id] = bp['lon']

################################################################################
class JourneyStore:
    """
    Loads Journey information from a CSV file and stores as a list of Journey
    objects.

    Methods are exposed to enable filtering and selection of Journeys by the
    date at which they occured

    Parameters
    ----------
    HEADER_VALUES : dict
        Contains a list of accepted header value parameters from the CSV input
        file.
    """

    # Default header values - these are stripped of whitespace and made
    # lowercase to convert to property values for a
    HEADER_VALUES = {
        'Rental Id',
        'Duration',
        'Bike Id',
        'End Date',
        'EndStation Id',
        'EndStation Name',
        'Start Date',
        'StartStation Id',
        'StartStation Name'
    }

    # Constructor
    def __init__(self, fileLocation):
        # Create empty cycle data list
        self.journeys = [];
        try:
            # Open file
            print('Loading... ', fileLocation)
            with open(fileLocation) as csvfile:
                cycleReader = csv.reader(csvfile, delimiter=',', quotechar='\"')
                header = cycleReader
                # Prepare whitespace stripping regular expression
                whitespacePattern = re.compile(r'\s+')
                # Header indicies
                headerIndex = {}
                # Line count
                lineCount = 0;
                for row in cycleReader:
                    # Get header
                    if lineCount == 0:
                        print('Reading header with', len(row), 'fields')
                        # Identify key fields
                        headerCount = 0
                        for field in row:
                            # Remove whitespace from field name
                            strippedField = re.sub(whitespacePattern, '', field)
                            if field in self.HEADER_VALUES:
                                headerIndex[strippedField.lower()] = headerCount;
                                # print(headerCount, '=>', strippedField.lower())
                                headerCount += 1
                        lineCount += 1
                    else:
                        newCycleData = tflbikedata.Journey(row[headerIndex['rentalid']],
                                                 row[headerIndex['duration']],
                                                 row[headerIndex['bikeid']],
                                                 row[headerIndex['enddate']],
                                                 row[headerIndex['endstationid']],
                                                 row[headerIndex['endstationname']],
                                                 row[headerIndex['startdate']],
                                                 row[headerIndex['startstationid']],
                                                 row[headerIndex['startstationname']]);
                        # Add to list of data
                        self.journeys.append(newCycleData)
                        # DEBUG
                        # print station ids
                        #print(row[headerIndex['startstationid']], '=>', row[headerIndex['endstationid']])
                        lineCount += 1
                # Sort date and cycle data
                print('Sorting data')
                self.journeys.sort(key=lambda x:x.startDate)
                print('finished sorting data')

        except IOError:
            print('Unable to load file')

    def filterStarted(self, startDate, endDate):
        """
        Returns a list of journeys that have started between the provided
        startDate and endDate objects (inclusive).

        Parameters
        ----------
        startDate : datetime
            Start date for filter condition
        endDate : datetime
            End date for filter condition
        """
        return list(filter(
                lambda cd: cd.startDate >= startDate and cd.startDate <= endDate,
                self.journeys
               ))

    def filterOngoing(self, startDate, endDate):
        """
        Returns a list of journeys that are ongoing between the provided
        startDate and endDate objects (inclusive).

        Parameters
        ----------
        startDate : datetime
            Start date for filter condition
        endDate : datetime
            End date for filter condition
        """
        return list(filter(
                lambda cd: (cd.startDate <= startDate and cd.endDate >= endDate),
                self.journeys
               ))
