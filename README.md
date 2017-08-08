The goal of this project is to pull the River Gauge Data from wateroffice.ec.gc.ca and tweet the water level <br>

1) You will need to create a Twitter Account and get Application Tokens<br>
https://apps.twitter.com/app<br>
2) Insert the generated keys in auth.json<br>
3) Modify the stationList to include the River Gauge you are interested in<br>
3) Setup a Cron Scheduling Job on your server<br>
4) Happy Tweeting<br>

Example Command line:<br>
python river.py --StationName=Britannia --debugMode=0<br>
<br>
StationName:<br>
Currently we support any Gov of Canada Water Office.  Simply modify the stationList.json, description.json<br>
<br>
TestMode:<br>
Make sure to set debugMode to 1 otherwise you will be tweeting!<br>
