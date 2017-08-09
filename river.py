import datetime, dateutil.parser, calendar
import urllib, logging, csv
import tweepy
import ujson
import argparse

WATEROFFICE = "http://dd.weather.gc.ca/hydrometric/csv/ON/hourly/"

def getStationCSV(stationName, stationID):
    logging.debug("Entering getStationCSV stationName: {} stationID: {}" \
                    .format(stationName, stationID))
    if stationID == stationList[stationName]:
        logging.debug("Found Station: {}".format(stationID))
        url = "{}{}_hourly_hydrometric.csv".format(WATEROFFICE, stationID)
    else:
        logging.error("Station NOT Found {}".format(stationID))
        raise Exception("Not Implemented")
    logging.debug("URL for {}: {}".format(stationID, url))
    return url

# Get the Current Water Level from the Water Office
def getCurrWaterLevel(stationName, stationID):
    logging.debug("Entering getCurrWaterLevel stationName: {} stationID: {}"\
                    .format(stationName, stationID))
    url = getStationCSV(stationName, stationID)
    file = urllib.URLopener()
    file.retrieve(url, str("tmp.csv"))
    reader = csv.reader(open("tmp.csv"))
    # Get the last entry of the CSV to get the latest water level
    for row in reader:
        logging.debug("CSV {}".format(row))
        waterLevel = row[2]
        waterLevelDateString = row[1]
    waterLevelDate = dateutil.parser.parse(waterLevelDateString)
    logging.info("Water Level is equal to: {} on the {}" \
                    .format(waterLevel, waterLevelDate.day))
    description = getDescription(stationID, float(waterLevel))
    return waterLevel, waterLevelDate, description

# Should I go Paddle?
def getDescription(stationID, waterLevel):
    logging.debug("Entering getDescription stationID: {} waterlevel: {}" \
                    .format(stationID, waterLevel))
    # Parse Water Level JSON Data
    with open('description.json') as description_file:
        data = ujson.load(description_file)
    # Iterate through the different water level conditions
    try:
        for entry in data[stationToQuery]:
            logging.debug("Check Water Level Condition: {} low: {} high: {}" \
                            " description {}".format(stationToQuery, entry['low'], \
                            entry['high'], entry['description']))
            if waterLevel >= entry['low'] and waterLevel < entry['high']:
                logging.debug("Water Level Condition FOUND")
                return entry['description']
        logging.debug("Water Level Condition NOT FOUND return empty description")
    except KeyError:
        logging.error("KeyError while parsing the Description JSON File.")
        pass
    return ""

# Parse JSON Station List
def getJsonStationList():
    logging.debug("Entering getJsonStationList")
    with open('stationList.json') as station_file:
        data = ujson.load(station_file)
    logging.debug("Station List: {}".format(data))
    return data

# Parse Json Authentication File
def getJsonAuth():
    logging.debug("Entering getJsonAuth")
    with open('auth.json') as auth_file:
        data = ujson.load(auth_file)
    logging.debug("Crendentials: {}".format(data))
    return data

# Authenticate
def getApi(cfg):
    logging.debug("Entering getApi with the following auth config: " \
                    "{}".format(cfg))
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--StationName', help='River Station Name')
    parser.add_argument('--debugMode', help='Debug Mode 0 (off) or 1 (on)')
    args = parser.parse_args()
    if args.StationName is None:
        raise Exception("Argument Station Name is missing.")
    else:
        stationToQuery = args.StationName
    if args.debugMode is None or args.debugMode == 0:
        debugMode = 0
        logging.basicConfig(level=logging.INFO)
    else:
        debugMode = args.debugMode
        logging.basicConfig(level=logging.DEBUG)

    stationList = getJsonStationList()
    stationID = stationList[stationToQuery]
    (waterLevel, waterLevelDate, description) = getCurrWaterLevel(stationToQuery, stationID)
    authData = getJsonAuth()
    api = getApi(authData)
    todayDate = calendar.day_name[waterLevelDate.weekday()]
    tweet = description + "Water Level at {} on {} is now at {}" \
            .format(stationToQuery, todayDate, waterLevel)
    # Send Out the Tweet!
    if debugMode == 0:
        logging.info("Live mode... post the tweet")
        status = api.update_status(status=tweet)
    else:
        logging.info("Test mode... not posting.")
        status = "Test Mode DID NOT POST"
    logging.info("Tweet: {}".format(tweet))
    logging.info("Twitter Reponse Status: {}".format(status))
