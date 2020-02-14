from datetime import datetime
from marshmallow_sqlalchemy import ModelSchema
from app import db
from app.cars.models import CarData

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    carsdata = db.relationship('CarData', backref='reminder', lazy=True)

    def __repr__(self):
        return f"Reminder('{self.text}')"
"""
class ReminderCarData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_car_data = db.Column(db.Integer, db.ForeignKey('car_data.id'), nullable=False)
    id_reminder = db.Column(db.Integer, db.ForeignKey('reminder.id'), nullable=False)
"""



class ReminderSchema(ModelSchema):
    class Meta:
        model = Reminder
        sqla_session = db.session
"""
class ReminderCarDataSchema(ModelSchema):
    class Meta:
        model = ReminderCarData
        sqla_session = db.session
"""