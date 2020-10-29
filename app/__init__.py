from flask import Flask

from app.CRB import CRB

app = Flask(__name__, static_url_path="")
crb = CRB()

from app import routes
