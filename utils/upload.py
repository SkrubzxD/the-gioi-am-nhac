import os
from flask import current_app, flash
from werkzeug.utils import secure_filename

def allowed_file(filename, allowed_extensions):
    """Check if the file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def upload_file(file, folder_name, allowed_extensions="pdf,png,jpg,jpeg,mp3,wav,glb"):
    """
    Generic utility to handle file uploads.
    :param file: The file object from request.files
    :param folder_name: Subfolder within 'static' (e.g., 'audio', 'images/instruments')
    :return: The relative path to the stored file or None if failed
    """
    if not file or file.filename == '':
        return None

    if allowed_extensions and not allowed_file(file.filename, allowed_extensions.split(',')):
        flash(f"File type not allowed. Allowed: {', '.join(allowed_extensions.split(','))}", "error")
        return None

    filename = secure_filename(file.filename)
    
    # Ensure the target directory exists
    target_dir = os.path.join(current_app.root_path, 'static', folder_name)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    file_path = os.path.join(target_dir, filename)
    file.save(file_path)
    
    # Return the relative path for database storage
    return f"/static/{folder_name}/{filename}"
