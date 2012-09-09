import urllib
import urllib2
import settings

# based on https://www.beeminder.com/api

class Beeminder:
  def __init__(self, this_auth_token):
    self.auth_token=this_auth_token
    self.base_url='https://www.beeminder.com/api/v1'

  def get_user(self,username):
    url = "%s/users/%s.json" % (self.base_url,username)
    values = {'auth_token':self.auth_token}
    result = self.call_api(url,values,'GET')
    return result

  def get_goal(self,username,goalname):
    url = "%s/users/%s/goals/%s.json" % (self.base_url,username,goalname)
    values = {'auth_token':self.auth_token}
    result = self.call_api(url,values,'GET')
    return result

  def get_datapoints(self,username,goalname):
    url = self.base_url+'users/'+username+'/goals/'+goalname+'/datapoints.json'
    url = "%s/users/%s/goals/%s/datapoints.json" % (self.base_url,username,goalname)
    values = {'auth_token':self.auth_token}
    result = self.call_api(url,values,'GET')
    return result

  def create_datapoint(self,username,goalname,timestamp,value,comment=' ',sendmail='false'):
    url = self.base_url+'users/'+username+'/goals/'+goalname+'/datapoints.json'
    url = "%s/users/%s/goals/%s/datapoints.json" % (self.base_url,username,goalname)
    values = {'auth_token':self.auth_token, 'timestamp':timestamp, 'value':value, 'comment':comment, 'sendmail':sendmail}
    result = self.call_api(url,values,'POST')
    return result

  def call_api(self,url,values,method='GET'):
    result=''
    data = urllib.urlencode(values)
    if method=='POST':
      req = urllib2.Request(url,data)
      response = urllib2.urlopen(req)
    else:
      response = urllib2.urlopen(url+'?'+data)
    result=response.read()
    return result
