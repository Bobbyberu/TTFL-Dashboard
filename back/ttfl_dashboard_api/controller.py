from ttfl_dashboard_api import app

@app.route('/')
def hello():
    return 'hello'