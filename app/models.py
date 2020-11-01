from app import db

class Vars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_time_checked_currencies = db.Column(db.DateTime, default=0)

class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    cbr_id = db.Column(db.String(6), unique=True)
    char_code = db.Column(db.String(3), index=True)

class Value(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cbr_id = db.Column(db.String(3), db.ForeignKey('currency.id'))
    timestamp = db.Column(db.String(10), index=True)
    val_rel_to_rub = db.Column(db.Float())