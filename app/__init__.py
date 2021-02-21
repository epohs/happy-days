from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_assets import Environment

# Initiate our app and load config
# options from our config.py file.
app = Flask(__name__)
app.config.from_object(Config)

# Setup database connection and
# Migrations for changes to the db.
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initiate Flask Login to handle
# authentication and redirects for
# Un logged in users.
login = LoginManager(app)
login.login_view = 'index'

# Flask Assets handles bundling our
# CSS and JavaScript files into a 
# single minified file when we are
# not in development mode.
assets = Environment(app)
assets.debug = Config.DEBUG
assets.cache = not Config.DEBUG
assets.url_expire = Config.DEBUG

# Database Models, and Routes must
# be imported after the app object
# is defined.
from app import models, routes

# Define our bundlels for Flask Assets.
# These will be used by our base.html
# template.
routes.make_asset_bundles()


# Run our Flask app when this file is
# invoked directly. This happens when
# gunicorn first calls our app package.
if __name__ == '__main__':
  
  app.run( debug = Config.DEBUG )
