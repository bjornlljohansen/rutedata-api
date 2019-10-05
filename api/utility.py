from flask_restplus import Model, fields

Coordinates = Model('Coordinates',{
            'latitude': fields.Float(required=True, description='Latitude'),
            'longitude': fields.Float(required=True, description='Longitude')
            })
