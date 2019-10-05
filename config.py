import os

''' Example configurations'''

class DevelopmentConfig:
    ENV                 = 'development'
    DEBUG               = True
    SECRET_KEY          = "crashtest"
    TRAVELMAGIC_BASEURL = "http://rp.tromskortet.no/scripts/TravelMagic/TravelMagicWE.dll"
    TRAVELMAGIC_INITVIEWPORT = ({'lat': 69.684943, 'lon':18.989582}, {'lat': 69.696643, 'lon': 19.007582})

class ProductionConfig:
    SECRET_KEY      = os.environ.get('SECRET_KEY')
    TRAVELMAGIC_BASEURL = "http://rp.tromskortet.no/scripts/TravelMagic/TravelMagicWE.dll"
    TRAVELMAGIC_INITVIEWPORT = ({'lat': 69.628081, 'lon': 18.677409}, {'lat': 69.784807, 'lon': 19.430324})

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
