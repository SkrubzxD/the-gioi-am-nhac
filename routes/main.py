from flask import Blueprint, render_template
from models import STUDENT, db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def main_home():
    return render_template('home.html')

@main_bp.route('/vnmap')
def to_vnmap():
    return render_template('vnmap.html')
