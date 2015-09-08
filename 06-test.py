import urllib
import urllib2
import cartodb

username = 'dms8md23'
apikey = 'fc4b0fe709cc086fd177768e648694d6be3170dc'

#Next, lets create an INSERT statement to use

insert = "INSERT INTO testcreate (the_geom) VALUES (ST_Buffer(CDB_LatLng(40.7127, -74.0059),0.11));"

#Create the URL endpoint for our account API

url = "https://%s.cartodb.com/api/v1/sql" % username

#Create an object containing the parameters of our request

params = {
    'api_key' : apikey, # our account apikey, don't share!
    'q'       : insert  # our insert statement above
}

#Send the request using urllib2

req = urllib2.Request(url, urllib.urlencode(params))
response = urllib2.urlopen(req)