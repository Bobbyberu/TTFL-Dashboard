from flask import Flask, abort
from ttfl_dashboard_api.controller import controller
from properties.properties import DbProperty
from peewee import *

db = MySQLDatabase(DbProperty('name'), user=DbProperty('user'),
                   password=DbProperty('pwd'), host=DbProperty('host'), port=DbProperty('port', True))
db.connect()

app = Flask(__name__)
app.register_blueprint(controller)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, threaded=True, debug=True)
