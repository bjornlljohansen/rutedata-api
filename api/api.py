from flask_restplus import Api

from .stops import api as stops
from .departures import api as departures

api = Api(
    title='Rutedata API',
    version='0.1',
    description='A simple API to get route data for public transport companies using the TravelMagic system',
    contact='apis@bjolab.net'
)

api.add_namespace(stops)
api.add_namespace(departures)
