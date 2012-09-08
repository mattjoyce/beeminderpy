import urllib
import urllib2

class beeminder:
  def __init__(self, auth_token):
    self.AUTH_TOKEN=auth_token
    self.BASE_URL='https://www.beeminder.com/api/v1/'

  def GetUser(self,username):
    url = self.BASE_URL+'users/'+username+'.json'
    values = {'auth_token':self.AUTH_TOKEN}
    data = urllib.urlencode(values) 
    req = urllib2.urlopen(url+'?'+data)
    result = req.read()
    return result

  def GetGoal(self,username,goalname):
    url = self.BASE_URL+'users/'+username+'/goals/'+goalname+'.json'
    values = {'auth_token':self.AUTH_TOKEN}
    data = urllib.urlencode(values)
    req = urllib2.urlopen(url+'?'+data)
    result = req.read()
    return result

  def GetDatapoints(self,username,goalname):
    url = self.BASE_URL+'users/'+username+'/goals/'+goalname+'/datapoints.json'
    values = {'auth_token':self.AUTH_TOKEN}
    data = urllib.urlencode(values)
    req = urllib2.urlopen(url+'?'+data)
    result = req.read()
    return result

  def CreateDatapoint(self,username,goalname,ts,value,comment,sendmail):
    url = self.BASE_URL+'users/'+username+'/goals/'+goalname+'/datapoints.json'
    values = {'auth_token':self.AUTH_TOKEN, 'timestamp':ts, 'value':value, 'comment':comment, 'sendmail':sendmail}
    data = urllib.urlencode(values)
    req = urllib2.Request(url,data)
    response = urllib2.urlopen(req)
    result=response.read()
    return result

