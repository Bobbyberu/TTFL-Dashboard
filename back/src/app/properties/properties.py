from configparser import ConfigParser

config = ConfigParser()
config.read('app/properties/properties.ini')
APISection = 'API'
DbSection = 'Database'


def APIProperty(field):
    return config[APISection][field]


def DbProperty(field, isInt=False):
    if isInt:
        return int(config[DbSection][field])
    else:
        return config[DbSection][field]
