from flask import Blueprint, render_template, request, abort, redirect, url_for, flash, send_from_directory, current_app
from sqlalchemy.sql.expression import or_
from models import Instrument, db
import os

library_bp = Blueprint('library', __name__)

@library_bp.route('/library/')
def to_library():
    instruments = db.session.query(Instrument).order_by(Instrument.Vietnamese_Name).all()
    return render_template('music_library/library.html', instruments=instruments)

@library_bp.route('/library/search', methods=['GET', 'POST'])
def search_library():
    if request.method == 'POST':
        search_term = request.form.get('Search', '')
    else:
        search_term = request.args.get('q', '')
    
    search_pattern = f"%{search_term}%"
    results = db.session.execute(
        db.select(Instrument).where(or_(
            Instrument.Name.like(search_pattern),
            Instrument.Vietnamese_Name.like(search_pattern),
            Instrument.Category.like(search_pattern),
            Instrument.Region.like(search_pattern),
            Instrument.Description.like(search_pattern)
        ))
    ).scalars().all()
    return render_template('music_library/library_search_result.html', results=results, search_term=search_term)

@library_bp.route('/library/instrument/<instrument_id>')
def view_instrument(instrument_id):
    instrument = db.session.get(Instrument, instrument_id)
    if not instrument:
        abort(404)
    return render_template('music_library/instrument_detail.html', instrument=instrument)

@library_bp.route('/library/add', methods=['GET', 'POST'])
def add_instrument():
    if request.method == 'GET':
        return render_template('music_library/instrument_form.html', instrument=None, action='add')
    
    try:
        new_instrument = Instrument(
            ID=request.form.get('ID'),
            Name=request.form.get('Name'),
            Vietnamese_Name=request.form.get('Vietnamese_Name'),
            Category=request.form.get('Category'),
            Region=request.form.get('Region'),
            Description=request.form.get('Description'),
            History=request.form.get('History'),
            Playing_Technique=request.form.get('Playing_Technique'),
            Audio_File=request.form.get('Audio_File'),
            Video_URL=request.form.get('Video_URL'),
            Image_Main=request.form.get('Image_Main'),
            Image_Gallery=request.form.get('Image_Gallery')
        )
        db.session.add(new_instrument)
        db.session.commit()
        flash('Instrument added successfully!', 'success')
        return redirect(url_for('library.view_instrument', instrument_id=new_instrument.ID))
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding instrument: {str(e)}', 'error')
        return redirect(url_for('library.add_instrument'))

@library_bp.route('/library/edit/<instrument_id>', methods=['GET', 'POST'])
def edit_instrument(instrument_id):
    instrument = db.session.get(Instrument, instrument_id)
    if not instrument:
        abort(404)
    
    if request.method == 'GET':
        return render_template('music_library/instrument_form.html', instrument=instrument, action='edit')
    
    try:
        instrument.Name = request.form.get('Name')
        instrument.Vietnamese_Name = request.form.get('Vietnamese_Name')
        instrument.Category = request.form.get('Category')
        instrument.Region = request.form.get('Region')
        instrument.Description = request.form.get('Description')
        instrument.History = request.form.get('History')
        instrument.Playing_Technique = request.form.get('Playing_Technique')
        instrument.Audio_File = request.form.get('Audio_File')
        instrument.Video_URL = request.form.get('Video_URL')
        instrument.Image_Main = request.form.get('Image_Main')
        instrument.Image_Gallery = request.form.get('Image_Gallery')
        db.session.commit()
        flash('Instrument updated successfully!', 'success')
        return redirect(url_for('library.view_instrument', instrument_id=instrument_id))
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating instrument: {str(e)}', 'error')
        return redirect(url_for('library.edit_instrument', instrument_id=instrument_id))

@library_bp.route('/library/delete/<instrument_id>', methods=['POST'])
def delete_instrument(instrument_id):
    instrument = db.session.get(Instrument, instrument_id)
    if not instrument:
        abort(404)
    try:
        db.session.delete(instrument)
        db.session.commit()
        flash('Instrument deleted successfully!', 'success')
        return redirect(url_for('library.to_library'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting instrument: {str(e)}', 'error')
        return redirect(url_for('library.view_instrument', instrument_id=instrument_id))

@library_bp.route('/library/audio/<filename>')
def serve_audio(filename):
    audio_dir = os.path.join(current_app.root_path, 'static', 'audio')
    return send_from_directory(audio_dir, filename)
