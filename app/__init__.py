from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['PER_PAGE'] = 6
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app, version='1.0', title='SYC API')

from app.users.controllers import users
from app.cars.controllers import cars
from app.reminders.controllers import reminders
api.add_namespace(users)
api.add_namespace(cars)
api.add_namespace(reminders)

db.create_all()


