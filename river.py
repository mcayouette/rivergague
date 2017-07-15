import urllib
import logging
import csv

WATEROFFICE="http://dd.weather.gc.ca/hydrometric/csv/ON/hourly/"
BRITANNIA="ON_02KF005"

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
    reader = csv.reader(open("tmp.csv"))
    # Get the last entry of the CSV to get the latest water level
    waterLevel = ""
    for row in reader:
        logging.debug("CSV " + ''.join(row))
        waterLevel = row[2]
    logging.info("Water Level is equal to: " + waterLevel)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
url = getStationCSV(BRITANNIA)
getCurrentWaterLevel(url)
