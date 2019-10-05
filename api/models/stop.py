from collections import OrderedDict

class Stop:

    @classmethod
    def fromTravelMagicDict(cls, odict):
        '''
            OrderedDict([
                ('@v', '19021091:1'),
                ('@hplnr', '19021091'),
                ('@stopnr', '1'),
                ('@n', 'Nerstranda (Tromsø)'),
                ('@t', '0'),
                ('@d', '0'),
                ('@m', '1'),
                ('@x', '18,954256'),
                ('@y', '69,647085'),
                ('@tn', 'Buss'),
                ('@st', 'Buss.png'),
                ('@l', '34,42,70,71,72,73'),
                ('@lineref', '34,42,70,71,72,73'),
                ('zones', OrderedDict([
                    ('zone', [OrderedDict([
                            ('@v', '19100'),
                            ('@n', 'Tromsø')
                        ]),
                        OrderedDict([
                            ('@v', '19100'),
                            ('@n', 'Tromsø')
                            ]),
                        OrderedDict([
                            ('@v', '19100'),
                            ('@n', 'Tromsø')
                        ]),
                        OrderedDict([
                            ('@v', '19100'),
                            ('@n', 'Tromsø')
                        ]),
                        OrderedDict([
                            ('@v', '19100'),
                            ('@n', 'Tromsø')
                        ])
                        ])
                    ])
                )
            ])
            OrderedDict([
                ('@v', '19021343:3'),
                ('@hplnr', '19021343'),
                ('@stopnr', '3'),
                ('@n', 'Utsikten (Tromsø)'),
                ('@t', '0'),
                ('@d', '0'),
                ('@m', '1'),
                ('@x', '19,002269'),
                ('@y', '69,692722'),
                ('@tn', 'Buss'),
                ('@st', 'Buss.png'),
                ('@l', '20,X32,42'),
                ('@lineref', '20,32,42'),
                ('zones', OrderedDict([
                    ('zone', [OrderedDict([
                            ('@v', '19100'),
                            ('@n', 'Tromsø')
                        ]),
                        OrderedDict([
                            ('@v', '19100'),
                            ('@n', 'Tromsø')
                        ]),
                        OrderedDict([
                            ('@v', '19100'),
                            ('@n', 'Tromsø')
                        ]),
                        OrderedDict([
                            ('@v', '19100'),
                            ('@n', 'Tromsø')
                        ]),
                        OrderedDict([
                            ('@v', '19100'),
                            ('@n', 'Tromsø')
                        ])
                        ])
                    ])
                )
            ])
        '''
        if type(odict) != OrderedDict:
            raise ValueError("Stop.fromTravelMagicDict takes exacly one OrderedDict, got %s : %s" % (type(odict), str(odict)))

        d = {}
        try:
            d['name']=odict['@n']
            d['id']=odict['@v']
            d['stop']=odict['@hplnr']
            d['place']=odict['@stopnr'] if '@stopnr' in odict else 0
            d['coordinates'] = {'latitude': float(odict['@y'].replace(',','.')), 'longitude': float(odict['@x'].replace(',','.'))}
            d['lines'] = odict['@l'].split(',') if '@l' in odict else []

        except KeyError as e:
            raise ValueError("Missing members of OrderedDict: %s" % e)

        return Stop(**d)

    def __init__(self, name, id, stop, place, coordinates, lines):
        self.name=name
        self.id=id
        self.stop=stop
        self.place=place
        self.coordinates=coordinates
        self.lines=lines


