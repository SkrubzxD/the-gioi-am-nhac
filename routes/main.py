from flask import Blueprint, render_template
from models import STUDENT, db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def main_home():
    return render_template('home.html')

@main_bp.route('/vnmap')
def to_vnmap():
    return render_template('vnmap.html')

@main_bp.route('/gallery/')
def to_gallery():
    return render_template('home.html')

@main_bp.route('/gallery/infographic')
def to_infographic():
    return render_template('thesis_archive/thesis_search_result.html')

@main_bp.route('/music_world/')
def to_musicworld():
    return render_template('music_world.html')

@main_bp.route('/music_world/3dpreview/')
@main_bp.route('/3d_model_viewer/3dpreview')
def to_3dpreview():
    return render_template('3d_model_viewer/3dpreview.html')

@main_bp.route('/music_world/3dpreview/<string:inname>')
def render_3d(inname):
    filename = inname + ".glb"
    return render_template('3d_model_viewer/3d_view.html', modelname=filename)

@main_bp.route('/testdb')
def test_db():
    profiles = db.session.query(STUDENT).all()
    return render_template('quiz/testdb.html', profiles=profiles)

@main_bp.route('/<path:subpath>')
def spa_catch_all(subpath: str):
    return render_template('home.html')
