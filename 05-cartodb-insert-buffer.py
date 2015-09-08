import urllib
import urllib2
import cartodb

username = 'dms8md23'
apikey = 'fc4b0fe709cc086fd177768e648694d6be3170dc'

#Next, lets create an INSERT statement to use

#insert = "INSERT INTO testCREATE AS SELECT ST_Buffer(the_geom,500) AS the_geom FROM testtable1"
#insert = "INSERT INTO testCREATE SELECT ST_Buffer(the_geom_webmercator,2500) AS the_geom_webmercator, cartodb_id FROM test_table1"
#Create the URL endpoint for our account API
insert = "INSERT INTO testCREATE (the_geom_webmercator, cartodb_id) VALUES ((SELECT ST_Buffer(the_geom_webmercator,2500) AS the_geom_webmercator FROM test_table1), SELECT cartodb_id FROM test_table1)"


#THIS WORKS IN THE CARTODB QUERY EDITOR
#SELECT ST_Buffer(the_geom_webmercator,500) AS the_geom_webmercator, cartodb_id FROM test_table1

url = "https://%s.cartodb.com/api/v1/sql" % username

#Create an object containing the parameters of our request

params = {
    'api_key' : apikey, # our account apikey, don't share!
    'q'       : insert  # our insert statement above
}

#Send the request using urllib2

req = urllib2.Request(url, urllib.urlencode(params))
response = urllib2.urlopen(req)