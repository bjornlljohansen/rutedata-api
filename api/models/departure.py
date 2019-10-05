from collections import OrderedDict

from datetime import datetime

class Departure:

    @classmethod
    def fromTravelMagicDict(cls, odict):
        ''' Example dict:
            OrderedDict([
                ('@tt', '2'),
                ('@tp', 'Buss.png'),
                ('@tn', 'Buss'),
                ('@d', '27.09.2019 22:21:00'),
                ('@a', '27.09.2019 22:21:00'),
                ('@v', '19021343:1'),
                ('@hplnr', '19021343'),
                ('@stopnr', '1'),
                ('@l', '20'),
                ('@nd', 'Kroken via sentrum'),
                ('@c', 'Troms fylkestrafikk'),
                ('@dir', 'Tur'),
                ('@ns', ''),
                ('@fnt', ''),
                ('@tid', '43735.19:9:20:1131.0'),
                ('@d2', '27.09.2019 22:21:05'),
                ('@a2', '27.09.2019 22:20:49'),
                ('@monitored', 'true'),
                ('@updateid', '2,19021343:1,,20,1,2,19021355,19021747,43735.1335,43735.1384,43735.1341,43735.1341,19:9:20:1131,2019-09-27'),
                ('@lineref', '20'),
                ('@vehiclejourneyref', '19:9:20:1131')
            ])
            OrderedDict([
                ('@tt', '2'),
                ('@tp', 'Buss.png'),
                ('@tn', 'Buss'),
                ('@d', '28.09.2019 02:26:00'),
                ('@a', '28.09.2019 02:26:00'),
                ('@v', '19021091:1'),
                ('@hplnr', '19021091'),
                ('@stopnr', '1'),
                ('@l', '42'),
                ('@nd', 'Stakkevollan via sentrum'),
                ('@c', 'Troms fylkestrafikk'),
                ('@dir', 'Retur'),
                ('@ns', ''),
                ('@fnt', ''),
                ('@tid', '43736.19:9:42:1150.0'),
                ('@d2', '28.09.2019 02:26:00'),
                ('@a2', '28.09.2019 02:26:00'),
                ('@cancellation', 'true'),
                ('@fromcancellation', 'true'),
                ('@monitored', 'true'),
                ('@updateid', '2,19021091:1,,42,2,2,19023061,19021355,43736.118,43736.168,43736.146,43736.146,19:9:42:1150,2019-09-28'),
                ('@lineref', '42'),
                ('@vehiclejourneyref', '19:9:42:1150'),
                ('fromnotes',
                    OrderedDict([
                        ('i', OrderedDict([
                            ('@d', 'Holdeplass Nerstranda stengt inntil videre. Benytt midlertidig holdeplass i Storgata.'),
                            ('@st', 'situation'),
                            ('@sv', 'normal')
                            ])
                        )
                    ])
                )
            ])
        '''
        if type(odict) != OrderedDict:
            raise ValueError("Departure.fromTravelMagicDict takes exacly one OrderedDict")

        d = {}
        try:
            d['name']=odict['@nd']
            d['line']=odict['@l']
            d['stop']=odict['@hplnr']
            d['stopid']=odict['@v']
            d['place']=odict['@stopnr']
            d['realtime']="@monitored" in odict and odict['@monitored'] == 'true'
            d['time']= odict['@d2'] if d['realtime'] else odict['@d']
            d['time'] = int(datetime.strptime(d['time'], '%d.%m.%Y %H:%M:%S').timestamp())
            d['cancelled']="@cancellation" in odict and odict['@cancellation'] == 'true'
            d['stopcancelled']="@fromcancellation" in odict and odict['@fromcancellation'] == 'true'
            if "fromnotes" in odict:
                notes = [{'description': odict["fromnotes"]['i']['@d'], 'type': odict["fromnotes"]['i']['@st'], 'version': odict["fromnotes"]['i']['@sv']}]

        except KeyError as e:
            raise ValueError("Missing members of OrderedDict: %s" % e)

        return Departure(**d)

    def __init__(self, name, line, time, stop, stopid, place, realtime, cancelled=False, stopcancelled=False, notes=[]):
        self.name=name
        self.line=line
        self.time=time
        self.stop=stop
        self.stopid=stopid
        self.place=place
        self.realtime=realtime
        self.cancelled=cancelled
        self.stopcancelled=stopcancelled
        self.notes=notes


