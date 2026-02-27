from flask import Flask
import os
from models import db, question

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
database_url = os.environ.get('POSTGRES_URL') or os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///test.db'

db.init_app(app)

with app.app_context():
    db.create_all()

from routes import register_routes
register_routes(app)
