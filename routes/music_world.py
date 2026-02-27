from flask import Blueprint, render_template

music_world_bp = Blueprint('music_world', __name__)

@music_world_bp.route('/music_world/')
def to_musicworld():
    return render_template('music_world/music_world.html', modelname='monochord.glb')

@music_world_bp.route('/music_world/<string:inname>')
def render_3d(inname):
    filename = inname if inname.endswith('.glb') else inname + ".glb"
    return render_template('music_world/music_world.html', modelname=filename)
