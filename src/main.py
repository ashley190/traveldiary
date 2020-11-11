from dotenv import load_dotenv
load_dotenv()

from flask import Flask
app = Flask(__name__)

from database import init_db
db = init_db(app)

from flask_marshmallow import Marshmallow
ma = Marshmallow(app)

from controllers import registerable_controllers
for controller in registerable_controllers:
    app.register_blueprint(controller)