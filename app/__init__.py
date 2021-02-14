from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_assets import Environment, Bundle

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
assets = Environment(app)
assets.debug = Config.DEBUG



from app import models, routes


if __name__ == '__main__':
  
    app.run( debug = Config.DEBUG )
