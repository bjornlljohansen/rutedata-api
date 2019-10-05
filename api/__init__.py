from flask import Flask
from config import config

from .api import api
from .models import TravelMagic



def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    with app.app_context():
        app.TravelMagic = TravelMagic(app.config['TRAVELMAGIC_BASEURL'])
        if 'TRAVELMAGIC_INITVIEWPORT' in app.config.keys():
            print("Initializing stop database of TravelMagic with %s" % str(app.config['TRAVELMAGIC_INITVIEWPORT']))
            ret = app.TravelMagic.primeStops(app.config['TRAVELMAGIC_INITVIEWPORT'])
            print("Initiated TravelMagic with %d stops" % ret)

    api.init_app(app)

    return app
