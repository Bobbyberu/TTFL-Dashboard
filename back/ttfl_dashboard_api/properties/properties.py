from configparser import ConfigParser

config = ConfigParser()
config.read('properties/properties.ini')
APISection = 'API'

def APIProperty(field):
    return config[APISection][field]