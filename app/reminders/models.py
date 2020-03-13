from datetime import datetime
from marshmallow_sqlalchemy import ModelSchema
from app import db
from app.cars.models import Car, CarData


class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    carsdata = db.relationship('CarData', backref='reminder', lazy=True)

    def __repr__(self):
        return f"Reminder('{self.text}')"

    @staticmethod
    def update_reminders(car):
        response = {}
        for carData in car.carData:
            if (carData.carDataCode == 2) and (CarData.revisione(car, carData.dataDate)):
                carData.id_reminder = 7
                response['review_date'] = carData.reminder.text
            elif (carData.carDataCode == 2) and not (CarData.revisione(car, carData.dataDate)):
                carData.id_reminder == None
            if (carData.carDataCode == 3) and (CarData.tagliando(car, carData.dataInt, CarData.GetKm(car, car.carData), CarData.GetDateDetection(car, car.carData))):
                carData.id_reminder = 6
                response['check_km'] = carData.reminder.text
            elif (carData.carDataCode == 3) and not (CarData.tagliando(car, carData.dataInt, CarData.GetKm(car, car.carData), CarData.GetDateDetection(car, car.carData))):
                carData.id_reminder = None
            if (carData.carDataCode == 4) and (CarData.assicurazione(car, carData.dataDate)):
                carData.id_reminder = 8
                response['assurance_date'] = carData.reminder.text
            elif (carData.carDataCode == 4) and not (CarData.assicurazione(car, carData.dataDate)):
                carData.id_reminder = None
            if (carData.carDataCode == 5) and (CarData.bollo(car, carData.dataDate)):
                carData.id_reminder = 9
                response['tax_date'] = carData.reminder.text
            elif (carData.carDataCode == 5) and not (CarData.bollo(car, carData.dataDate)):
                carData.id_reminder = None
            db.session.commit()
        return response


class ReminderSchema(ModelSchema):
    class Meta:
        model = Reminder
        sqla_session = db.session
