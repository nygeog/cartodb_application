from cartodbAWCCensus import cartodbAWCensus

cartoDBusername = 'dms8md23'
cartoDBapikey = 'fc4b0fe709cc086fd177768e648694d6be3170dc'

cartodbAWCensus(    '40.7127','-74.0059','2500','nyct2010',    cartoDBusername, cartoDBapikey)
#def cartodbAWCensus(inLat,   inLng,     bufDist,censusFeature,username,        apikey):