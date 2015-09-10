import urllib
import urllib2
import cartodb
import datetime
from datetime import datetime
import time
import pandas as pd

def cartodbAWCensus(inLat,inLng,bufDist,censusFeature,username,apikey):
    fileDate = datetime.now().strftime('%Y%m%d_%H%M%S')
    fd = fileDate

    print 'Datetime:'
    print fd
    url = "https://%s.cartodb.com/api/v1/sql" % username
    
    i = '1' #in this, basically create a new var that is the count of number of unique lat,lng's, in this case just this one, make this a loop at some point.
    
    insertList = ["CREATE TABLE latlngtable_"+fd+" (cdbawcensusuid int);",
                  "SELECT cdb_cartodbfytable('latlngtable_"+fd+"');",
                  "INSERT INTO latlngtable_"+fd+" (the_geom, cdbawcensusuid) VALUES (CDB_LatLng("+inLat+", "+inLng+"), "+i+")",
                  "CREATE TABLE latlngtablebuffer_"+fd+" AS SELECT ST_Buffer(the_geom_webmercator, "+bufDist+") AS the_geom_webmercator, cartodb_id, cdbawcensusuid FROM latlngtable_"+fd+"",
                  "SELECT cdb_cartodbfytable('latlngtablebuffer_"+fd+"');",
                  "CREATE TABLE latlngtablebufferintersect_"+fd+" AS (SELECT  ST_Intersection(a.the_geom, b.the_geom), a.geoid, a.sq_km, b.cdbawcensusuid FROM "+censusFeature+" as a, latlngtablebuffer_"+fd+" as b WHERE ST_Intersects(a.the_geom, b.the_geom))",
                  "SELECT cdb_cartodbfytable('latlngtablebufferintersect_"+fd+"');",
                  "CREATE TABLE latlngtablebufferintersectcalc_"+fd+" AS SELECT ST_Area(the_geom::geography) area_sqmeters, (ST_Area(the_geom::geography)/(sq_km*1000000)) pctorigarea, geoid, the_geom, cdbawcensusuid, sq_km FROM latlngtablebufferintersect_"+fd+"",
                  "SELECT cdb_cartodbfytable('latlngtablebufferintersectcalc_"+fd+"');",
                  "DROP TABLE latlngtable_"+fd+", latlngtablebuffer_"+fd+", latlngtablebufferintersect_"+fd+""
                 ]
    print '------------'
    print 'Running SQL commands to PostGIS/CartoDB...'
    for insert in insertList:   
        params = {
            'api_key' : apikey, # our account apikey, don't share!
            'q'       : insert  # our insert statement above
        }  
        #print insert
        req = urllib2.Request(url, urllib.urlencode(params))
        response = urllib2.urlopen(req)
    time.sleep(60)
    url = "http://%scartodb.com/api/v2/sql?q=SELECT%20*%20FROM%20latlngtablebufferintersectcalc_"+fd+"&format=csv&api_key="+apikey % username
    df = pd.read_csv(url)
    df = df.drop(['the_geom','the_geom_webmercator'], axis=1)
    df.to_csv("latlngtablebufferintersectcalc_"+fd+".csv", index=False)
    print 'Table Output - saved table as .csv to folder where this script has run from'
    print '------------'
    print df.head(10)

