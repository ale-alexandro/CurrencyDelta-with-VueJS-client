from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Init Flask and SQLAlchemy Engine
app = Flask(__name__, static_url_path="")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app,db)

# Init Service Classes
from app.CRB import CRB
crb = CRB()

from app import routes, models
