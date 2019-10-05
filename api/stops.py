from flask_restplus import Namespace, Resource, fields
from flask import current_app

from .utility import Coordinates

api = Namespace('stops', description='Operations related to stops/stages')

api.model('Coordinates', Coordinates)

Stop = api.model('Stop',{
        'coordinates': fields.Nested(Coordinates, required=True, description='Coordinates of the stop/stage'),
        'id': fields.String(required=True, description='Stop/stage ID as used by the TravelMagic system'),
        'lines': fields.List(fields.String, required=False, description='List of lines that have arrivals/departures at this stop'),
        'name': fields.String(required=True, description='Name or description of the stop/stage'),
        'place': fields.String(required=False, description='Index of stop/stage within a group of stops at the same place'),
        'stop': fields.String(required=True, description='Stop ID as used by the TravelMagic system')
        }
    )

@api.route('/')
class StopList(Resource):
    @api.doc('List stops')
    @api.marshal_list_with(Stop)
    def get(self):
        '''List all stops'''
        return [stop.__dict__ for stop in current_app.TravelMagic.stops.values()]

@api.route('/<stopid>:<place>')
class StopList(Resource):
    @api.doc('Return Stop')
    @api.marshal_with(Stop)
    def get(self, stopid, place):
        '''Get a specific stop based on it's stop ID and and internal index'''
        stopid=stopid+':'+place
        if stopid in current_app.TravelMagic.stops:
            return current_app.TravelMagic.stops[stopid].__dict__
        api.abort(404)

@api.route('/<int:stopid>')
class StopList(Resource):
    @api.doc('Return Stop')
    @api.marshal_with(Stop)
    def get(self, stopid):
        '''List all stops within a group of stops'''
        return [s.__dict__ for s in current_app.TravelMagic.stops.values() if str(stopid) == s.stop]
        api.abort(404)

@api.route('/<name>')
class StopList(Resource):
    @api.doc('Search for stopid')
    @api.marshal_with(Stop)
    def get(self, name):
        '''List all stopscontaining <name>'''
        return [s.__dict__ for s in current_app.TravelMagic.stops.values() if name in s.name]
        api.abort(404)
