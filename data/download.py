import urllib.request
import urllib.parse

with open('usage-data-list.csv', 'r') as listFile:

    for line in listFile:

        url = "http://cycling.data.tfl.gov.uk/usage-stats/{}".format(urllib.parse.quote(line[:-1]))

        print('Downloading {} ...'.format(url))

        urllib.request.urlretrieve(url, line[:-1])

        print('Done')
