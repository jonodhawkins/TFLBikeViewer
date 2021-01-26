from context import tflbikedata
import sys
from datetime import datetime

print("Running python", sys.version)
print(tflbikedata.COPYRIGHT_STATEMENT + "\n");
print(tflbikedata.USER_STATEMENT + "\n");

print('Loading JourneyStore')
jStore = tflbikedata.JourneyStore("data/195JourneyDataExtract01Jan2020-07Jan2020.csv")

print('Loading BikePointStore')
bpStore = tflbikedata.BikePointStore();
bpStore.load();

print('Loading RouteStore')
rStore = tflbikedata.RouteStore('tflRouteLib.pkl', overwrite=True)
print('Loaded', rStore.numRoutes,'routes')

startDate = datetime(2020,1,3,hour=7,minute=30);
endDate = datetime(2020,1,3,hour=7, minute=40);

ongoingJourneys = jStore.filterOngoing(startDate, endDate)
startJourneys = jStore.filterStarted(startDate, endDate)

print('There are', len(ongoingJourneys),'ongoing journeys vs.', len(startJourneys),'started journeys between',startDate,'and',endDate)

print('Iterating over journeys...')
for journey in startJourneys:
    journey.loadSteps(bpStore, rStore)

rStore.save()
