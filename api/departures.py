from flask_restplus import Namespace, Resource, fields
from flask import current_app

from .utility import Coordinates

api = Namespace('departures', description='Operations related to departures')

from .stops import Stop

Note = api.model('Note',{
            'description': fields.String(required=True, description='Text data of the note'),
            'type': fields.String(required=True, description='Note type'),
            'version': fields.String(required=True, description='Note version')
            })

Departure = api.model('Departure',{
        'name': fields.String(required=True, description='Line/Departure name'),
        'line': fields.String(required=True, description='Line or route the departure is a part of'),
        'realtime': fields.Boolean(required=True, description='Indicated if the time attribute is realtime prediction, or regular route departure time'),
        'time': fields.Integer(required=True, description='Departure time'),
        'stop': fields.String(required=True, description='Stop the departure departs from'),
        'place': fields.String(required=True, description='Place number the departure departs from'),
        'stopid': fields.String(required=True, description='Stop ID the departure departs from'),
        'cancelled': fields.Boolean(required=True, description='Indicated if the route has been cancelled'),
        'stopcancelled': fields.Boolean(required=True, description='Indicated if this specific stop of the route has been cancelled'),
        'notes': fields.List(fields.Nested(Note),required=False, description='Notes pertaining to this departure')
        }
    )

DeparturesStopsDict = api.model("DeparturesStopsDict", {
        'departures': fields.List(fields.Nested(Departure), required=True, description="List of departures"),
        'stops': fields.List(fields.Nested(Stop), required=True, description="List of stops")
        }
    )

@api.route('/<int:stopid>')
@api.route('/<stopid>:<place>')
class StopDepartureList(Resource):
    @api.doc('Return Departures for a given stop/stage')
    @api.marshal_with(DeparturesStopsDict)
    def get(self, stopid, place=None):
        '''Get departures from a specific stop or group of stops'''
        if place:
            stopid=stopid+':'+place
        if stopid in current_app.TravelMagic.stops:
            ret = current_app.TravelMagic.getDepartures(stopid)
        else:
            ret =  current_app.TravelMagic.getDepartures(stopid)
            departures, stops = ret['departures'], ret['stops']
            if not stops:
                api.abort(404)
            current_app.TravelMagic.addStops(stops.values())

        return {'departures': departures, 'stops': [stop for stop in stops.values()] }

@api.route('/<name>')
class StopsDepartureList(Resource):
    @api.doc('Return departures from stops matching <name>')
    @api.marshal_with(DeparturesStopsDict)
    def get(self, name):
        '''List all departures from stops containing <name>'''
        stops = {s.id: s for s in current_app.TravelMagic.stops.values() if name in s.name}
        if not stops:
            api.abort(404)
        departures = []
        for stop in stops.values():
            departures.extend(current_app.TravelMagic.getDepartures(stop.id)['departures'])
        departures = sorted(departures, key=lambda k: k.time)

        return {'departures': departures, 'stops': [stop for stop in stops.values()] }
