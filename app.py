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

from routes import register_routes
register_routes(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.Model.metadata.reflect(db.engine)
        print("Reflected tables:", db.Model.metadata.tables.keys())
        print("Database file URI:", app.config['SQLALCHEMY_DATABASE_URI'])
    app.run(host='0.0.0.0', port=3000, debug=True)