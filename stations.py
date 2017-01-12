import urllib.request
import codecs
import sys
import math

# Find the code of the station closest to the given coordinates
def get_station_code(location_lat, location_lon):
    # Load the station data
    url = "https://www.ncdc.noaa.gov/homr/file/asos-stations.txt"
    try:
        ftpstream = urllib.request.urlopen(url)
    except:
        print("Station codes could not be retrieved")
        sys.exit(1)
    file = codecs.iterdecode(ftpstream, 'utf-8')
    
    # Find character indices for relevant data
    first_line = next(file)
    call_index = first_line.find("CALL")
    lat_index = first_line.find("LAT")
    lon_index = first_line.find("LON")
    
    # Skip line
    next(file)
    
    # Find the smallest distance between provided coordinates and a station
    dist_best = 9999
    for line in file:
        lat = float(line[lat_index:lat_index + 9])
        lon = float(line[lon_index:lon_index + 10])
        dist = math.sqrt((lat - location_lat)**2 + (lon - location_lon)**2)
        if dist < dist_best:
            dist_best = dist
            call_best = "K" + line[call_index:call_index + 3]
        
    return call_best