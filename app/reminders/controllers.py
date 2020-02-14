from flask import jsonify, request
from flask_restplus import Resource, reqparse, fields
from app.reminders.models import Reminder, ReminderSchema
from app.cars.models import Car, CarSchema, CarData, CarDataSchema
from app import api
from app import db
from app import app

resp = {200: 'Success', 400: 'reminder already in db', 406: 'Content not allowed', \
    413: 'Payload too large', 500: 'Server Error', 404: 'reminder Not Found' }

reminders = api.namespace('api/v1.0/reminders',description='CRUD operation for syc reminders')

car_schema = CarSchema()
reminder_schema = ReminderSchema()
car_data_schema = CarDataSchema()
reminders_schema = ReminderSchema(many=True)
#reminder_car_data_schema = ReminderCarDataSchema()

reminderModel = reminders.model('reminderModel', {
    'text' : fields.String(required=True, validate=True)
})

parserId = reqparse.RequestParser()
parserId.add_argument('reminder_id',type=int)

parserIdCarData = reqparse.RequestParser()
parserIdCarData.add_argument('id_CarData',type=int)

parserPage = reqparse.RequestParser()
parserPage.add_argument('page',type=int, default=1)

@reminders.route('/<int:reminder_id>')
class GET_reminderById(Resource):
    def get(self,reminder_id):
        reminder = Reminder.query.get(reminder_id)
        if not reminder:
            return 'reminder Not Found', 404
        return jsonify(reminder_schema.dump(reminder))

    @reminders.expect(reminderModel, validate=True)
    def put(self,reminder_id):
        reminder = Reminder.query.get(reminder_id)
        if not reminder:
           return 'reminder Not Found', 404
        print(request.get_json())
        reminder.text = request.get_json()['text'] if request.get_json()['text'] else reminder.text
        db.session.commit()
        return jsonify(reminder_schema.dump(reminder))

    def delete(self,reminder_id):
        try:
            reminder = Reminder.query.get(reminder_id)
            if not reminder:
             return 'reminder Not Found', 404
            db.session.delete(reminder)
            db.session.commit()
            return jsonify({'result': True})
        except:
            return 'Error Server Side', 500

    @reminders.expect(parserIdCarData, validate=True)
    def post(self,reminder_id):
        id_CarData = int(request.args.get('id_CarData'))
        car_data = CarData.query.get(id_CarData)
        if not car_data:
             return 'cardata Not Found', 404
        car_data.id_reminder = reminder_id
        db.session.commit()
        response = {}
        response['car_data'] = car_data_schema.dump(car_data)
        response['reminder'] = reminder_schema.dump(car_data.reminder)
        return jsonify(response)


@reminders.route('')
class POST_reminder(Resource):
    @reminders.expect(reminderModel, validate=True)
    @reminders.doc(responses=resp)
    def post(self):
            text = request.get_json()['text'] 
            new_reminder = Reminder(
            text=text)
            db.session.add(new_reminder)
            db.session.commit()
            return jsonify(reminder_schema.dump(new_reminder))

    @reminders.expect(parserId, parserPage)
    def get(self):
        if request.args.get('reminder_id'):
            reminder_id=request.args.get('reminder_id')
            reminder = Reminder.query.get(reminder_id)
            if not reminder:
                return 'reminder Not Found', 404
            return jsonify(reminder_schema.dump(reminder))
        else:
            page = request.args.get('page', 1 , type=int)
            reminders_count = Reminder.query.count()
            pages= reminders_count // app.config['PER_PAGE'] + (reminders_count % app.config['PER_PAGE'] > 0)
            reminders = Reminder.query.paginate(page, app.config['PER_PAGE'], False).items
            response =   { "page": page, "per_page": app.config['PER_PAGE'],
                    "total": reminders_count, "total_pages": pages, "data": []}
            response["data"]=reminders_schema.dump(reminders)
            return jsonify(response)

@reminders.route('/car/<int:car_id>')
class Get_car_reminders(Resource):
    def get(self,car_id):
        car = Car.query.get(car_id)
        if not car:
                return 'Car Not Found', 404
        response = {}
        response['car'] = car_schema.dump(car)
        response['car_data'] = []
        for carData in car.carData:
            response['car_data'].append(reminder_schema.dump(carData.reminder)) 
            response['car_data'].append(car_data_schema.dump(carData))
        return jsonify(response)

@reminders.route('/car/<int:car_id>/<int:car_data_id>')
class Delete_car_reminder(Resource):
    def delete(self,car_id, car_data_id):
        car = Car.query.get(car_id)
        if not car:
                return 'Car Not Found', 404
        for car_data in car.carData:
            if car_data_id == car_data.id:
                car_data =  CarData.query.get(car_data_id)
                car_data.id_reminder = None
                db.session.commit()
                return jsonify({'result': True})
        else:
            return 'CarData Not Found', 404





        

