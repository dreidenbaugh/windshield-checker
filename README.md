# Windshield Checker
This Python command-line program scrapes weather data from the 
Internet to roughly predict whether an exposed windshield would be 
covered with frost, rain, or snow.

## Usage
Using geographic coordinates, run on the command line as follows:
```
$ python windshield.py [Latitude] [Longitude]
```

To use a weather station code, run on the command line as follows:
```
$ python windshield.py [Station Code]
```

Note that most airports have weather station codes starting with a 'K' 
followed by the three-digit airport code (e.g., "KBOI").

## Predictions
The program uses Weather Underground archive data to check reported 
weather conditions so far on the current day for the specified 
station. If rain or snow events have been reported, the program 
assumes that whichever occurred most recently may be on the 
windshield. Otherwise, the program predicts whether frost is on the 
windshield by calculating a score that increases with each weather 
observation at which the dew point and air temperature were near and 
the wind speed was low. The predictions are very approximate as many 
unpredictable factors can affect the formation of frost on a 
windshield and whether precipitation accumulates and remains on a 
windshield.