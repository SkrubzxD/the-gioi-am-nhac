from flask import Blueprint, render_template, request
from models import db, question
from utils.quiz_db import get_random_questions

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/quiz/')
def to_quiz():
    return render_template('quiz/quiz.html')

@quiz_bp.route('/quiz/question')
def to_quest():
    data = get_random_questions(db, limit=3)
    return render_template('quiz/question.html', questions=data)

@quiz_bp.route("/submit-quiz", methods=["POST"])
def submit_quiz():
    score = 0
    total_questions = 0
    results_summary = []
    question_ids = list(request.form.keys())
    questions_db = db.session.execute(db.select(question).where(question.ID.in_(question_ids))).scalars().all()
    question_map = {q.ID: q for q in questions_db}

    for q_id, user_answer in request.form.items():
        actual_question = question_map.get(q_id)
        if actual_question:
            total_questions += 1
            is_correct = (user_answer == actual_question.CorrectA)
            if is_correct:
                score += 1
            results_summary.append({
                'question': actual_question.QName, 'your_answer': user_answer,
                'correct_answer': actual_question.CorrectA, 'is_correct': is_correct
            })
        return render_template('quiz/quiz_result.html', score=score, total=total_questions, summary=results_summary)
    
    @quiz_bp.route('/quiz/learning')
    def to_learning():
        return render_template('quiz/learning.html')
    