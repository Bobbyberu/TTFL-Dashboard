from flask import Flask, abort
from ttfl_dashboard_api.controller import controller

app = Flask(__name__)
app.register_blueprint(controller)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, threaded=True, debug=True)
