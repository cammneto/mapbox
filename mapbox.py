import requests
import sys
import numpy as np
import os

def readFile(readMEfile):
    readme = open(readMEfile, "r")
    return readme

def cityName(readmeFile): #Extracts the city name from terrain.party README file
    f=readFile(readmeFile)
    for line in f:
        if 'terrain.party/api' in line:
            name=line.split('=')[1]
            name=name.split('&')[0]
            print('City Name ---> '+name)
    return name

def coordinates(readmeFile): #Extracts and rearrange terrain.party README file coordinates for use in overpass api link
    f=readFile(readmeFile)
    for line in f:
        if 'terrain.party/api' in line:
            coordinates=line.split('box=')[1]
            coordinates=np.around([float(coordinates.split(',')[2]),float(coordinates.split(',')[3]),float(coordinates.split(',')[0]),float(coordinates.split(',')[1])],4)
            coordinates=str(coordinates[0])+','+str(coordinates[1])+','+str(coordinates[2])+','+str(coordinates[3])
            print('  overpass coordinates ---> '+coordinates+'\n')
    return coordinates

def download(readmeFile):
    url='http://overpass-api.de/api/map?bbox='+coordinates(readmeFile)
    print('Downloading .osm file from:')
    print('  '+url+'\n')
    r = requests.get(url)
    cityname=cityName(readmeFile)
    print('File saved at: ' + os.getcwd())
    with open(cityname+'.osm', 'wb') as osmFile:
        osmFile.write(r.content)
        ### Retrieve HTTP meta-data
        print(r.status_code)
        print(r.headers['content-type'])
        print(r.encoding)

download(sys.argv[1])
