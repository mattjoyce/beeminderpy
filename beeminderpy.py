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
