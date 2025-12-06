from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
import os
"https://www.vnam.edu.vn/Categories.aspx?lang=&CatID=12&SubID=47"
"https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html"
"code to active: . ./venv_name/bin/activate"

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'example.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids a warning
db = SQLAlchemy(app)

class STUDENT(db.Model):
    ID = db.Column(db.String(255), primary_key=True, nullable=False)
    NAME = db.Column(db.String(25), nullable=False )
    CLASS = db.Column(db.String(25))
    Score = db.Column(db.Integer)

class Thesis(db.Model):
    ID = db.Column(db.String(25), primary_key = True, nullable=False)
    Author = db.Column(db.String(25),nullable = False)
    Category = db.Column(db.String(25), nullable = False)
    Supervisor = db.Column(db.String(25), nullable = False)
    Name = db.Column(db.String(255),nullable = False)
    File_name = db.Column(db.String(25), nullable = False)

@app.route('/')
def main_home():
    return render_template('home.html')

@app.route('/learning')
def to_learning():
    return render_template('learning.html')

@app.route('/thesis')
def to_thesis():
    return render_template('thesis.html')

@app.route('/vnmap')
def to_vnmap():
    return render_template('vnmap.html')

@app.route('/gallery/')
def to_gallery():
    return render_template('gallery.html')

@app.route('/gallery/infographic')
def to_infographic():
    return render_template('infographic.html')

@app.route('/library/')
def to_library():
    return render_template('library.html')

@app.route('/gallery/development')
def to_development():
    return render_template('development.html')

@app.route('/music_world/')
def to_musicworld():
    return render_template('musicworld.html')

@app.route('/music_world/3dpreview/')
def to_3dpreview():
    return render_template('3dpreview.html')

@app.route('/music_world/3dpreview/<string:inname>')
def render_3d(inname):
    filename= inname+ ".glb"
    return render_template('3d_view.html',modelname=filename)

@app.route('/testdb')
def test_db():
    profiles = db.session.query(STUDENT).all()
    return render_template('testdb.html',profiles=profiles)

@app.route('/library/search', methods=["POST"])
def search_thesis():
    name = request.form.get("Search")
    return result(name)

@app.route('/library/result')
def result(name):
    result = db.session.execute(db.select(Thesis).where((Thesis.Name+Thesis.ID+Thesis.Author+Thesis.Supervisor+Thesis.Category).like(f'%{name}%'))).scalars()
    return render_template('thesis_search_result.html',result = result)




if __name__ == '__main__':
    with app.app_context():  # Needed for DB operations outside a request
        db.create_all()      # Creates the database and tables
        db.Model.metadata.reflect(db.engine)
        print("Reflected tables:", db.Model.metadata.tables.keys())
        print("Database file URI:", app.config['SQLALCHEMY_DATABASE_URI'])
    app.run(host='0.0.0.0', port=3000, debug=True)
