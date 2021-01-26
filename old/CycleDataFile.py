# CycleData.py defines the CycleData class which loads .csv files representing
# cycle journeys and converts this into an indexed form.
import re
import csv
import numpy as np
from TFLBikeViewer.CycleData import CycleData

class CycleDataFile:

    # Default header values - these are stripped of whitespace and made
    # lowercase to convert to property values for a
    headerValues = {
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
        self.cycleData = [];
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
                            if field in self.headerValues:
                                headerIndex[strippedField.lower()] = headerCount;
                                # print(headerCount, '=>', strippedField.lower())
                                headerCount += 1
                        lineCount += 1
                    else:
                        newCycleData = CycleData(row[headerIndex['rentalid']],
                                                 row[headerIndex['duration']],
                                                 row[headerIndex['bikeid']],
                                                 row[headerIndex['enddate']],
                                                 row[headerIndex['endstationid']],
                                                 row[headerIndex['endstationname']],
                                                 row[headerIndex['startdate']],
                                                 row[headerIndex['startstationid']],
                                                 row[headerIndex['startstationname']]);
                        # Add to list of data
                        self.cycleData.append(newCycleData)
                        # DEBUG
                        # print station ids
                        #print(row[headerIndex['startstationid']], '=>', row[headerIndex['endstationid']])
                        lineCount += 1
                # Sort date and cycle data
                print('Sorting data')
                self.cycleData.sort(key=lambda x:x.startDate)
                print('finished sorting data')

        except IOError:
            print('Unable to load file')

    def filter(self, startDate, endDate):
        return list(filter(lambda cd: cd.startDate >= startDate and cd.startDate <= endDate, self.cycleData));
