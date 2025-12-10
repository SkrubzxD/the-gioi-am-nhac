from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask import jsonify
import random
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

class question(db.Model):
    ID = db.Column(db.String(255) , primary_key = True , nullable = False)
    QName = db.Column(db.String(255), nullable = False)
    CorrectA = db.Column(db.String(25), nullable = False)
    DecoyB = db.Column(db.String(25), nullable = False)
    DecoyC = db.Column(db.String(25), nullable = False)
    DecoyD = db.Column(db.String(25), nullable = False)

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
    result = db.session.execute(db.select(Thesis).where((Thesis.Name+Thesis.ID+Thesis.Author+Thesis.Supervisor+Thesis.Category).like(f'%{name}%'))).scalars()
    return render_template('thesis_search_result.html',result = result)
    
@app.route('/quiz/')
def to_quiz():
    return render_template('quiz.html')

@app.route('/quiz/question')
def to_quest():
    data = []
    quest = db.session.execute(
        db.select(question).order_by(func.random()).limit(3)
    ).scalars().all()
    data = []
    for row in quest:
        # DEBUG: Print each row to see what it looks like
        print(f"Processing row: {row.ID}") 
        choice_pool = []
        choice_pool.append(row.CorrectA)
        choice_pool.append(row.DecoyB)
        choice_pool.append(row.DecoyC)
        choice_pool.append(row.DecoyD)
        random.shuffle(choice_pool)
        # 2. Convert each object to a dictionary manually
        row_as_dict = {
            'ID': row.ID,
            'QName': row.QName,
            'ChoiceA': choice_pool[0],
            'ChoiceB': choice_pool[1],
            'ChoiceC': choice_pool[2],
            'ChoiceD': choice_pool[3]
        }
        data.append(row_as_dict)
    
    # 3. Jsonify the list of dictionaries
    return render_template('question.html',questions=data)
@app.route("/submit-quiz", methods=["POST"])
def submit_quiz():
    score = 0
    total_questions = 0
    results_summary = []

    # request.form is a dictionary of { "name_attribute": "value_selected" }
    # In your case: { "QuestionID": "User's Choice String" }
    
    for q_id, user_answer in request.form.items():
        # Safety Check: In case you have other inputs like CSRF tokens or submit buttons,
        # ensure q_id is actually a number before querying the DB.
        

        # 1. Fetch the actual question from the DB using the ID from the form
        # (Using the same style as your earlier code)
        actual_question = db.session.execute(
            db.select(question).where(question.ID == q_id)
        ).scalar_one_or_none()

        if actual_question:
            total_questions += 1
            is_correct = False
            
            # 2. Compare User Answer vs Correct Answer
            # Note: Ensure you compare strings to strings
            if user_answer == actual_question.CorrectA:
                score += 1
                is_correct = True
            
            # 3. (Optional) Save details to display on a results page
            results_summary.append({
                'question': actual_question.QName,
                'your_answer': user_answer,
                'correct_answer': actual_question.CorrectA,
                'is_correct': is_correct
            })

    # 4. Pass the final data to a results template
    return render_template('quiz_result.html', 
                           score=score, 
                           total=total_questions, 
                           summary=results_summary)





if __name__ == '__main__':
    with app.app_context():  # Needed for DB operations outside a request
        db.create_all()      # Creates the database and tables
        db.Model.metadata.reflect(db.engine)
        print("Reflected tables:", db.Model.metadata.tables.keys())
        print("Database file URI:", app.config['SQLALCHEMY_DATABASE_URI'])
    app.run(host='0.0.0.0', port=3000, debug=True)
