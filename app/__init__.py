from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['DATABASE_URL'] = 'postgres://rmjbezokjkyagx:8c9afbc899de855cb3e60c36f06f5740589bb2ddb4e4f5bbc5b16d4f3815fea5@ec2-54-75-231-215.eu-west-1.compute.amazonaws.com:5432/df34oalf5k8a2j'
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


