#!/usr/bin/env python

'''

This was taken from https://groups.google.com/forum/?fromgroups=#!topic/fitbit-api/CkXQ6-0-vMs

Description:
   Using the FitBit API get: http://api.fitbit.com/1/user/-/activities/date/2011-04-17.xml

   Displays:
    <?xml version="1.0" encoding="UTF-8"?><result><summary><activeScore>44</activeScore><caloriesOut>1894</caloriesOut><distances><activityDistance><activity>total</activity><distance>0.11</distance></activityDistance><activityDistance><activity>tracker</activity><distance>0.11</distance></activityDistance><activityDistance><activity>loggedActivities</activity><distance>0</distance></activityDistance><activityDistance><activity>veryActive</activity><distance>0</distance></activityDistance><activityDistance><activity>moderatelyActive</activity><distance>0.03</distance></activityDistance><activityDistance><activity>lightlyActive</activity><distance>0.08</distance></activityDistance><activityDistance><activity>sedentaryActive</activity><distance>0</distance></activityDistance></distances><fairlyActiveMinutes>7</fairlyActiveMinutes><lightlyActiveMinutes>20</lightlyActiveMinutes><sedentaryMinutes>1413</sedentaryMinutes><steps>260</steps><veryActiveMinutes>0</veryActiveMinutes></summary></result>

Reference:
   http://wiki.fitbit.com/display/API/Fitbit+API
   http://wiki.fitbit.com/display/API/API-Get-Activities
   http://wiki.fitbit.com/display/API/OAuth-Authentication-API#OAuth-Authentication-API-TheOAuthFlow
   http://oauth.net/core/1.0a/

Notes: 
   FitBit API rejects oauth.OAuthSignatureMethod_HMAC_SHA1()
   generated signatures so use oauth.OAuthSignatureMethod_PLAINTEXT()
   instead.
'''

import os, httplib, json, urllib, sys

# Install oauth for python. On Ubuntu run: sudo apt-get install python-oauth
from oauth import oauth
DEBUG = True

class oauth_connect:
    def __init__(self, server, consumer_key, consumer_secret, access_token_fsp, request_token_url, auth_url, access_token_url, realm):
        self.connection = httplib.HTTPSConnection(server)
        self.consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
        self.signature_method = oauth.OAuthSignatureMethod_PLAINTEXT()
        self.access_token_fsp = access_token_fsp
        self.request_token_url = request_token_url
        self.auth_url = auth_url
        self.access_token_url = access_token_url
        self.realm = realm
        self.access_token = self.get_access_token()

    def fetch_response(oauth_request, debug=DEBUG):
        url= oauth_request.to_url()
        self.connection.request(oauth_request.http_method,url)
        response = self.connection.getresponse()
        s=response.read()
        if debug:
            print 'requested URL: %s' % url
            print 'server response: %s' % s
        return s

    def request(self,api_call):
        print '* Access a protected resource ...'
        print api_call
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, token=self.access_token, http_url=api_call)
        oauth_request.sign_request(self.signature_method, self.consumer, self.access_token)
        headers = oauth_request.to_header(self.realm)
        self.connection.request('GET', api_call, headers=headers)
        resp = self.connection.getresponse()
        return resp.read()

    def get_access_token(self):
        # if we don't have a cached access-token stored in a file, then get one
        if not os.path.exists(self.access_token_fsp):
            print '* Obtain a request token ...'
            oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, http_url=self.request_token_url)
            if DEBUG:
                self.connection.set_debuglevel(10)
            oauth_request.sign_request(self.signature_method, self.consumer, None)
            resp=fetch_response(oauth_request, self.connection)
            auth_token=oauth.OAuthToken.from_string(resp)
            print 'Auth key: %s' % str(auth_token.key)
            print 'Auth secret: %s' % str(auth_token.secret)
            print '-'*75,'\n\n'

            # authorize the request token
            print '* Authorize the request token ...'
            auth_url="%s?oauth_token=%s" % (self.auth_url, auth_token.key)
            print 'Authorization URL:\n%s' % auth_url
            oauth_verifier = raw_input( 'Please go to the above URL and authorize the app -- Type in the Verification code from the website, when done: ')
            print '* Obtain an access token ...'
            # note that the token we're passing to the new 
            # OAuthRequest is our current request token
            oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, token=auth_token, http_url=self.access_token_utl, parameters={'oauth_verifier': oauth_verifier})
            oauth_request.sign_request(self.signature_method, self.consumer, auth_token)

            # now the token we get back is an access token
            # parse the response into an OAuthToken object
            access_token=oauth.OAuthToken.from_string( fetch_response(oauth_request,self.connection))
            print 'Access key: %s' % str(access_token.key)
            print 'Access secret: %s' % str(access_token.secret)
            print '-'*75,'\n\n'

            # write the access token to file; next time we just read it from file
            if DEBUG:
                print 'Writing file', self.access_token_fsp
            fobj = open(access_token_fsp, 'w')
            access_token_string = access_token.to_string()
            fobj.write(access_token_string)
            fobj.close()
        else:
            if DEBUG:
                print 'Reading file', self.access_token_fsp
            fobj = open(self.access_token_fsp)
            access_token_string = fobj.read()
            fobj.close()
        return oauth.OAuthToken.from_string(access_token_string)


def main():
   SERVER='api.fitbit.com'
   myoauth=oauth_connect( server            =SERVER,
                          consumer_key      ='', 
                          consumer_secret   ='',
                          access_token_fsp  ='access_token.string',
                          request_token_url ='https://%s/oauth/request_token' % SERVER,
                          auth_url          ='https://%s/oauth/access_token' % SERVER, 
                          access_token_url  ='https://%s/oauth/authorize' % SERVER,
                          realm             =SERVER)

   if len(sys.argv)>1:
      apiCall = '/1/user/-/activities/steps/date/'+sys.argv[1]+'.json'
   else:
      apiCall = '/1/user/-/activities/steps/date/today/1d.json'
   #apiCall = '/1/user/-/devices.xml'
   #apiCall='/1/user/-/profile.xml'
   #apiCall='/1/user/-/activities/recent.xml'

   # For other FitBit API calls:
   #  http://wiki.fitbit.com/display/API/Resource-Access-API
   #  http://wiki.fitbit.com/display/API/API-Get-Activities

   # access protected resource
   data=json.loads(myoauth.request(apiCall))
   print data

if __name__ == '__main__':
   main()
