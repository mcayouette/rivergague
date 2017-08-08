import datetime, dateutil.parser, calendar
import urllib, logging, csv
import tweepy
import json

WATEROFFICE = "http://dd.weather.gc.ca/hydrometric/csv/ON/hourly/"

def getStationCSV(stationID):
    logging.debug("Entering getStationCSV stationID: " + stationID)
    if stationID == stationList["Britannia"]:
        logging.debug("Found Station:" + stationID)
        url = WATEROFFICE + stationID + "_hourly_hydrometric.csv"
    else:
        logging.error("Station NOT Found " + stationID)
        raise Exception("Not Implemented")
    logging.debug("URL for " + stationID + ": " + url)
    return url

# Get the Current Water Level from the Water Office
def getCurrWaterLevel(stationID):
    logging.debug("Entering getCurrWaterLevel stationID: " + stationID)
    url = getStationCSV(stationID)
    file = urllib.URLopener()
    file.retrieve(url, str("tmp.csv"))
    reader = csv.reader(open("tmp.csv"))
    # Get the last entry of the CSV to get the latest water level
    for row in reader:
        logging.debug("CSV " + str(row))
        waterLevel = row[2]
        waterLevelDateString = row[1]
    waterLevelDate = dateutil.parser.parse(waterLevelDateString)
    logging.info("Water Level is equal to: " +  waterLevel + " on the " \
                 + str(waterLevelDate.day))
    description = getDescription(stationID, float(waterLevel))
    return waterLevel, waterLevelDate, description

# Should I go Paddle?
def getDescription(stationID, waterLevel):
    logging.debug("Entering getDescription stationID: " + stationID \
                    + " waterlevel: " + str(waterLevel))
    if stationID == stationList["Britannia"]:
        if waterLevel >= 58.4 and waterLevel < 58.5:
            return "Go check out Sewer Wave!\n"
        elif waterLevel >= 58.5 and waterLevel < 58.7:
            return "Go to Sewer Wave or low water Champlain and " \
                    "may require some rope.\n"
        elif waterLevel >= 58.7 and waterLevel > 59:
            return "Go check out Champlain\n"
        elif waterLevel >= 59.1:
            return "Champlain is HUGE!!\n"
    return ""

# Parse JSON Station List
def getJsonStationList():
    logging.debug("Entering getJsonStationList")
    with open('stationList.json') as station_file:
        data = json.load(station_file)
    logging.debug("Station List: " + str(data))
    return data

# Parse Json Authentication File
def getJsonAuth():
    logging.debug("Entering getJsonAuth")
    with open('auth.json') as auth_file:
        data = json.load(auth_file)
    logging.debug("Crendentials: " + str(data))
    return data

# Authenticate
def getApi(cfg):
    logging.debug("Entering getApi with the following auth config: " + str(cfg))
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    debugMode = 1
    stationToQuery = "Britannia"
    stationList = getJsonStationList()
    (waterLevel, waterLevelDate, description) = getCurrWaterLevel(stationList[stationToQuery])
    authData = getJsonAuth()
    api = getApi(authData)
    tweet = description + "Water Level at " + stationToQuery \
            + " on " + calendar.day_name[waterLevelDate.weekday()] \
            + " is now at " + str(waterLevel)
    # Send Out the Tweet!
    if debugMode == 0:
        logging.info("Live mode... post the tweet")
        status = api.update_status(status=tweet)
    else:
        logging.info("Test mode... not posting.")
        status = "Test Mode DID NOT POST"
    logging.info("Tweet: " + tweet)
    logging.info("Twitter Reponse Status: " + str(status))
