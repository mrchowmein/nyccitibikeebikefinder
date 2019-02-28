#Jason Chan
#NYC CitiBike E-Bike Finder

import requests
import time
from geopy.distance import geodesic
import datetime
import geocoder


print("\nWelcome to Citi Bike E-Bike Finder\n")

stationJson = requests.get('https://feeds.citibikenyc.com/stations/stations.json').json()
stationStatus = requests.get('https://gbfs.citibikenyc.com/gbfs/es/station_status.json').json()

stationDict = {}

#but bike stations and location into local dict
with open('citiBike.csv', 'w', newline='') as f:
    fieldnames = ['id', 'name', 'lat', 'long']

    for each in stationJson['stationBeanList']:
        stationDict[each['id']] = [each['stationName'], each['latitude'], each['longitude']]



print("Where are you located?")
loc = input("Please enter your address: ")

g = geocoder.arcgis(loc)  #coodinates of your address
print("Your location: ", g.latlng)


while 1:
    coords_1 = g.latlng

    ebikeDict = {}

    sum = 0
    timeNow = datetime.datetime.now()
    print("\nLast checked: {:%m/%d/%Y  %I:%M %p}\n".format(timeNow))

    for each in stationStatus['data']['stations']:
        id = int(each['station_id'])
        ebikeNum = each['num_ebikes_available']

        #save all bike stations with ebikes into ebikeDict
        if ebikeNum > 0:
            key = "{} bike(s) at {}.".format(ebikeNum, stationDict[id][0])
            coords_2 = (stationDict[id][1], stationDict[id][2])
            sum += ebikeNum
            value = geodesic(coords_1, coords_2).miles
            value = str(round(value, 2))
            ebikeDict[key] = value

    #sort ebikeDict
    sorted_d = dict(sorted(ebikeDict.items(), key=lambda x: x[1]))
    for k, v in sorted_d.items():
        print(k, "   Distance from you: ", v, " miles")


    print("Total ebikes available: {}".format(sum))
    print("--------------------------------------------------\n")
    time.sleep(60)  #wait 60 seconds before checking again.