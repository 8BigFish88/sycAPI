from datetime import datetime
from app import db
from marshmallow_sqlalchemy import ModelSchema

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    fuel = db.Column(db.String(100), nullable=False)
    matriculation = db.Column(db.DateTime, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    carData = db.relationship('CarData', backref='car_author', lazy=True)

    def __repr__(self):
        return f"Car('{self.name}', '{self.matriculation}', '{self.fuel}','{self.image_file}', {self.carData}')"

class CarData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dataInt = db.Column(db.Integer, nullable=True, default=0)
    dataDate = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    carDataCode = db.Column(db.Integer, nullable=False)
    id_car = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    id_reminder = db.Column(db.Integer, db.ForeignKey('reminder.id'), nullable=True)
    
    def __repr__(self):
        return f"CarData('{self.valueInt}', '{self.valueDate}')"

    def add_dataInt(car,carDataCode,value):
        carValue = CarData(dataInt = value, carDataCode = carDataCode, car_author = car )
        db.session.add(carValue)

    def add_dataDate(car,carDataCode,value):
        carValue = CarData(dataDate = datetime.strptime(value, '%m/%d/%Y'), carDataCode = carDataCode, car_author = car )
        db.session.add(carValue)
	    



class CarSchema(ModelSchema):
    class Meta:
        model = Car
        sqla_session = db.session

class CarDataSchema(ModelSchema):
    class Meta:
        model = CarData
        sqla_session = db.session
