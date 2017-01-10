import logging
import datetime
import urllib.request
import codecs
import sys
import csv

snow = False
rain = False
frost_scores = []
frost_sum = 0
date_time_UTC_last = None

# Check for and get station code from argument
if len(sys.argv) is 2:
    airport_code = sys.argv[1]
    if not airport_code.isalnum():
        print("Invalid station code\nNote: Most airports have weather " +
              "station codes starting with a 'K' followed by the three-" +
              "digit airport code.")
        sys.exit(1)
else:
    print("Invalid format; proper format is 'python windshield.py " + 
          "[Station Code]'\nNote: Most airports have weather station codes " +
          "starting with a 'K' followed by the three-digit airport code.")
    sys.exit(1)

# Get current time
now = datetime.datetime.now()

# Load the weather data
url = ("http://api.wunderground.com/history/airport/" + airport_code + "/" + 
       str(now.year) + "/" + str(now.month) + "/" + str(now.day) + 
       "/DailyHistory.html?format=1")
try:
    ftpstream = urllib.request.urlopen(url)
except:
    print("Data could not be retrieved")
    sys.exit(1)
file = codecs.iterdecode(ftpstream, 'utf-8')

next(file) # Skip first line which is blank
next(file) # Skip second line which is headers
# For each line in file, extract data and adjust variables
for line in file:
    if "No daily or hourly history data available" in line:
        print("No data found for that station code today")
        sys.exit(1)
    data = line.strip().split(',')
    events = data[10]
    if "Snow" in events:
        snow = True
        rain = False
    if "Rain" in events:
        rain = True
        snow = False
    temp = float(data[1])
    dewpoint = float(data[2])
    if "Calm" in data[7]:
        wind_speed = 0
    else:
        wind_speed = float(data[7])
    date_time_UTC = datetime.datetime.strptime(data[13][0:19], 
                    "%Y-%m-%d %H:%M:%S")
    if date_time_UTC_last is not None:
        difference = date_time_UTC - date_time_UTC_last
        time_multiplier = difference.total_seconds() / 3600
        if "Rain" not in events and \
           "Snow" not in events and \
           dewpoint <= 32 and \
           temp - dewpoint < 4:
            frost_score = (4 - (temp - dewpoint)) * time_multiplier
            if wind_speed <= 5:
                frost_scores.append(frost_score)
            elif wind_speed > 5 and wind_speed < 15:
                wind_adjustment = - 0.1 * wind_speed + 1.5
                frost_scores.append(wind_adjustment * frost_score)
        else:
            frost_score = 0
        logging.debug("Time: " + str(date_time_UTC) + "\tPeriod: " + 
              str(time_multiplier) + "\tTemperature: " + str(temp) + 
              "\tDewpoint: " + str(dewpoint) + "\tWind : " + str(wind_speed)
              + "\tFrost Score: " + str(frost_score))
    date_time_UTC_last = date_time_UTC

# Sum the frost scores
for score in frost_scores:
    frost_sum += score
logging.debug("Frost Sum: " + str(frost_sum))

# Print the result
print(now.strftime("%A, %B %d") + ": ", end="")
if snow:
    print("There may be snow on the windshield")
elif rain:
    print("There may be rain on the windshield")
elif frost_sum > 12:
    print("There may be frost on the windshield")
else:
    print("There may be nothing on the windshield")
