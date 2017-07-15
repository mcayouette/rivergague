import datetime, dateutil.parser, calendar
import urllib, logging, csv
import tweepy

WATEROFFICE="http://dd.weather.gc.ca/hydrometric/csv/ON/hourly/"
BRITANNIA="ON_02KF005"
cfg = {
"consumer_key"        : "***",
"consumer_secret"     : "***",
"access_token"        : "***",
"access_token_secret" : "***"
}

def getStationCSV(stationName):
    if stationName == BRITANNIA:
        logging.debug("Found Station:" + stationName)
        url = WATEROFFICE + stationName + "_hourly_hydrometric.csv"
    else:
        logging.error("Station NOT Found " + stationName)
        raise Exception("Not Implemented")
    logging.debug("URL for " + stationName + ": " + url)
    return url

# Get the Current Water Level from the Water Office
def getCurrentWaterLevel(stationName):
    url = getStationCSV(stationName)
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
    description = getDescription(float(waterLevel))
    return waterLevel, waterLevelDate, description

# Should I go Paddle?
def getDescription(waterLevel):
    if waterLevel >= 58.4 and waterLevel < 58.5:
        return "Go check out Sewer Wave!"
    elif waterLevel >= 58.5 and waterLevel < 58.7:
        return "Go to Sewer Wave or Champlain with Rope."
    elif waterLevel >= 58.7 and waterLevel > 59:
        return "Go check out Champlain"
    elif waterLevel >= 59.1:
        return "Champlain is HUGE!!"
    else:
        raise(Exception("Nothing to report... exit"))
# Authenticate
def getApi(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    (waterLevel, waterLevelDate, description) = getCurrentWaterLevel(BRITANNIA)
    api = getApi(cfg)
    tweet = description + "\nWater Level at Britannia on " \
            + calendar.day_name[waterLevelDate.weekday()] \
            + " is now at " + str(waterLevel)
    logging.info(tweet)
    status = api.update_status(status=tweet)
    logging.info("Twitter: " + str(status))
