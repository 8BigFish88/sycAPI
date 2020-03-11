from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['PER_PAGE'] = 6
db = SQLAlchemy(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://mhtsdvfq:yOhNRqRkv7XmSoYEMY4pgvM3AmrpTC-0@kandula.db.elephantsql.com:5432/mhtsdvfq'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://pwckokmklmmjwv:a088dbd74aff681a40df0b6fef9367a70d91cd8e590198aec6648b821a83f7aa@ec2-54-75-246-118.eu-west-1.compute.amazonaws.com:5432/d6ubnsb7h4c8p'
migrate = Migrate(app, db)
api = Api(app, version='1.0', title='SYC API')

from app.users.controllers import users
from app.cars.controllers import cars
from app.reminders.controllers import reminders
api.add_namespace(users)
api.add_namespace(cars)
api.add_namespace(reminders)

db.create_all()


