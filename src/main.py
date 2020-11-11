from dotenv import load_dotenv
load_dotenv()

from flask import Flask  # noqa: E402
app = Flask(__name__)

from database import init_db  # noqa: E402
db = init_db(app)

from flask_marshmallow import Marshmallow  # noqa: E402
ma = Marshmallow(app)

from controllers import registerable_controllers  # noqa: E402
for controller in registerable_controllers:
    app.register_blueprint(controller)
