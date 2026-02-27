from flask import Blueprint, render_template, request, send_from_directory, current_app
from sqlalchemy.sql.expression import or_
from models import Thesis, db
import os

thesis_bp = Blueprint('thesis', __name__)

@thesis_bp.route('/thesis')
def to_thesis():
    return render_template('thesis_archive/thesis.html')

@thesis_bp.route('/thesis/search', methods=['GET', 'POST'])
def search_thesis():
    if request.method == 'POST':
        q = request.form.get('Search', '')
    else:
        q = request.args.get("q", "")
    search_pattern = f"%{q}%"
    result = db.session.execute(db.select(Thesis).where(or_(
        Thesis.Name.like(search_pattern),
        Thesis.ID.like(search_pattern),
        Thesis.Author.like(search_pattern),
        Thesis.Supervisor.like(search_pattern),
        Thesis.Category.like(search_pattern)
    ))).scalars()
    return render_template('thesis_archive/thesis_search_result.html', result=result)

@thesis_bp.route('/thesis/<thesisname>')

def serve_thesis_pdf(thesisname):

    filename = f"{os.path.basename(thesisname)}.pdf"

    directory = os.path.join(current_app.root_path, 'templates')

    return send_from_directory(directory, filename, as_attachment=False)
