#!/usr/bin/env python
import settings
import beeminderpy
import fitbit_api
import json
import datetime
import time
import sys

"""
   Get a fitbit value for a day, and post it as beeminder datapoint
"""


def main():
  fitbit_api_conn=fitbit_api.oauth_connect( server=settings.FITBIT_BASE_URL,
                       consumer_key      =settings.FITBIT_CONSUMER_KEY,
                       consumer_secret   =settings.FITBIT_CONSUMER_SECRET,
                       access_token_fsp  =settings.FITBIT_ACCESS_TOKEN_FSP,
                       request_token_url =settings.FITBIT_REQUEST_TOKEN_URL,
                       auth_url          =settings.FITBIT_AUTH_URL,
                       access_token_url  =settings.FITBIT_ACCESS_TOKEN_URL,
                       realm             =settings.FITBIT_REALM)

  beeapi=beeminderpy.Beeminder(settings.BEEMINDER_AUTH_TOKEN)

  #deal with the date
  #either privide a specific date 'yyyymmdd' or a delta '-2'
  tdate='-6'
  if len(sys.argv) >1 :
    tdate=sys.argv[1]
  yyyymmdd="2012-11-05"
  try:
    yyyymmdd=datetime.datetime.strptime(tdate, "%Y-%m-%d")
  except ValueError:
    try:
      yyyymmdd=(datetime.date.today()-datetime.timedelta(abs(int(tdate))))
    except:
      print "bad date"
      exit(-1)

  fitbit_api_call = '/1/user/-/activities/steps/date/'+yyyymmdd.strftime("%Y-%m-%d")+'/1d.json'

  data=json.loads(fitbit_api_conn.request(fitbit_api_call))
  print data
  
  value=data['activities-steps'][0]['value']
  print value

  timestamp=int(time.mktime(time.strptime(data['activities-steps'][0]['dateTime'], '%Y-%m-%d')))
  print timestamp

  
  beeapi.create_datapoint(settings.BEEMINDER_USERNAME,'fitbit',timestamp,value,'via API','true')

if __name__ == '__main__':
   main()

