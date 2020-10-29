from flask import send_from_directory, json, request

from app import app, crb

@app.route('/index')
@app.route('/')
def index():
    return send_from_directory("static", "index.html")

@app.route('/dist/<path:path>')
def static_dist(path):
    return send_from_directory("static/dist", path)

@app.route('/api/getCurrencyList')
def send_cur_list():
    return json.dumps(crb.getCurrList())

@app.route('/api/getCurrencyDelta')
def send_delta():
    req = request.args
    return json.dumps(crb.getDelta(req['cur'], req['start'], req['end']))