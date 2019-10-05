import requests
import xmltodict

from . import Departure, Stop

class TravelMagic():
    '''Handler class for the TravelMagic API from datagrafikk.no: https://www.datagrafikk.no/?page_id=2052&lang=en'''

    def __init__(self, baseurl):
        baseurl=baseurl.rstrip('/')

        if baseurl[-1*len('TravelMagicWE.dll'):] != 'TravelMagicWE.dll':
            raise ValueError('Base URL should end with the string \'TravelMagicWE.dll\'')

        self.baseurl=baseurl
        self.stops={}

    def getStops(self, viewport):
        if type(viewport) == dict:
            if len(viewport) == 2:
                url = "%s/v1NearestStopsXML?y=%s&x=%s" % (self.baseurl, viewport['lat1'], viewport['lon1'] )
            elif len(viewport) == 4:
                url = "%s/mapxml?y1=%s&x1=%s&y2=%s&x2=%s" % (self.baseurl, viewport['lat1'], viewport['lon1'], viewport['lat2'], viewport['lon2'])
            else:
                raise ValueError("getStops expects a tuple of 2 or 4 coordinates")
        else:
            raise ValueError("getStops expects a tuple of 2 or 4 coordinates")
        r = requests.get(url)

        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise RuntimeError("TravelMagic server responded with: %s" % str(e))
        
        stops=[]

        data = xmltodict.parse(r.content)

        xmlstages = data['stages']
        if not xmlstages:
            return stops

        if len(viewport) == 4:
            if 'i' not in xmlstages:
                return stops
            xmlstages = {'group': [{'i': xmlstages['i']}]}

        if 'group' not in xmlstages:
            return stops

        for group in xmlstages['group']:

            xmlstops = group['i']
            if type(xmlstops) != list:
                '''In the case we only have one stop, xmltodict returns the object directly'''
                xmlstops = [xmlstops]
            for stop in xmlstops:
                stops.append(Stop.fromTravelMagicDict(stop))

        return stops

    def addStops(self, stops):
        count = 0
        for stop in stops:
           if stop.id not in self.stops:
               self.stops[stop.id] = stop
               count += 1
        return count

    def primeStops(self, coordinates, delta=None, stepsize=0.05):
        if type(coordinates) == tuple:
            # We got a proper view
            y1 = coordinates[0]['lat']
            x1 = coordinates[0]['lon']
            y2 = coordinates[1]['lat']
            x2 = coordinates[1]['lon']
        elif type(coordinates) == dict and delta:
            y1 = coordinates['lat']
            x1 = coordinates['lon']
            y2 = coordinates['lat'] + delta['lat']
            x2 = coordinates['lon'] + delta['lon']
        elif type(coordinates) == dict:
            # We only need to get "nearby" stops
            stops = self.getStops({'lat1': coordinates['lat'], 'lon1': coordinates['lon']})
            return self.addStops(stops)

        if y1 > y2:
            y1, y2 = y2, y1
        if x1 > x2:
            x1, x2 = x2, x1

        count = 0
        
        tmp_y1 = y1
        
        while tmp_y1 < y2:
            # looping from south to north
            tmp_y2 = tmp_y1+stepsize if tmp_y1+stepsize < y2 else y2
            tmp_x1=x1
            while tmp_x1 < x2:
                #looping from west to east
                tmp_x2 = tmp_x1+stepsize if tmp_x1+stepsize < x2 else x2
                stops = self.getStops({'lat1': tmp_y1, 'lon1':tmp_x1,'lat2': tmp_y2, 'lon2': tmp_x2})
                count += self.addStops(stops)
                tmp_x1=tmp_x2
            tmp_y1=tmp_y2

        return count


    def getDepartures(self, stop):
        url="%s/v1DepartureSearchXML?hpl=%s&now=1&realtime=1" % (self.baseurl, stop)
        r = requests.get(url)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise RuntimeError("TravelMagic server responded with: %s" % str(e))
        
        departures=[]
        stops={}

        data = xmltodict.parse(r.content)
        xmldepartures = data['result']['departures']
        if xmldepartures:
            xmldepartures = xmldepartures['i']
            for dep in xmldepartures:
                departures.append(Departure.fromTravelMagicDict(dep))


        xmlstops = data['result']['stages']
        if xmlstops:
            xmlstops = xmlstops['i']
            if type(xmlstops) != list:
                '''In the case we only have one stop, xmltodict returns the object directly'''
                xmlstops = [xmlstops]

            for st in xmlstops:
                s = Stop.fromTravelMagicDict(st)
                stops[s.id] = s

        return {'departures': departures, 'stops': stops}
