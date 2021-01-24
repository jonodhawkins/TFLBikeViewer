import requests

class BikePointLibrary:

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
