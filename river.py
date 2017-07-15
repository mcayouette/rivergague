import requests, urllib
import logging
import csv

WATEROFFICE="http://dd.weather.gc.ca/hydrometric/csv/ON/hourly/"
BRITANNIA="ON_02KF005"

# https://wateroffice.ec.gc.ca/report/real_time_e.html?stn=02KF005&mode=Table
# http://dd.weather.gc.ca/hydrometric/csv/ON/hourly/ON_02KF005_hourly_hydrometric.csv
def getStationCSV(stationName):
    if stationName == BRITANNIA:
        logger.debug("Found Station:" + stationName)
        url = WATEROFFICE + stationName + "_hourly_hydrometric.csv"
    else:
        logger.error("Station NOT Found " + stationName)
        raise Exception("Not Implemented")
    logger.debug("URL for " + stationName + ": " + url)
    return url

def getCurrentWaterLevel(stationName):
    # Download the CSV
    file = urllib.URLopener()
    file.retrieve(url, ''.join("tmp.csv"))
    download = requests.get(url)
    reader = csv.reader(open("tmp.csv"))
    waterLevel = ""
    for row in reader:
        logging.debug("CSV " + ''.join(row))
        waterLevel = row[2]
    logging.info("Water Level is equal to: " + waterLevel)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
url = getStationCSV(BRITANNIA)
getCurrentWaterLevel(url)
