from flask import send_from_directory, json, request

from app import app, db, crb
from app.models import Currency

from datetime import datetime

@app.route('/index')
@app.route('/')
def index():
    return send_from_directory("static", "index.html")

@app.route('/dist/<path:path>')
def static_dist(path):
    return send_from_directory("static/dist", path)

@app.route('/api/getCurrencyList')
def send_cur_list():
    return crb.getCurrList()

@app.route('/api/getCurrencyDelta')
def send_delta():
    req = request.args
    start = req['start']
    end = req['end']
    
    try:
        dts = datetime.strptime(start, "%d-%m-%Y")
        start = start.replace("/", "-")
    except ValueError:
        return json.dumps({'error': 2, 'date': start})
    
    try:
        dte = datetime.strptime(end, "%d-%m-%Y")
        end = end.replace("/", "-")
    except ValueError:
        return json.dumps({'error': 3, 'date': end})

    if not Currency.query.filter_by(cbr_id=req['cur']).first():
        return json.dumps({'error': 4, 'cbr_cur_id': req['cur']})

    return json.dumps(crb.getDelta(req['cur'], start, end))
