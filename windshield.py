import datetime
import urllib.request
import codecs
import csv

snow = False
rain = False

airport_code = input("Station Code: ")

now = datetime.datetime.now()

url = ("http://api.wunderground.com/history/airport/" + airport_code + "/" + 
str(now.year) + "/" + str(now.month) + "/" + str(now.day) + 
"/DailyHistory.html?format=1")
ftpstream = urllib.request.urlopen(url)
file = codecs.iterdecode(ftpstream, 'utf-8')
next(file)
for line in file:
    events = line.strip().split(',')[10]
    if "Snow" in events:
        snow = True
    elif "Rain" in events:
        rain = True

if snow:
    print("It snowed")
if rain:
    print("It rained")