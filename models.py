from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func, or_

db = SQLAlchemy()
# ============ EXISTING MODELS ============
class STUDENT(db.Model):
    ID = db.Column(db.String(255), primary_key=True, nullable=False)
    NAME = db.Column(db.String(25), nullable=False)
    CLASS = db.Column(db.String(25))
    Score = db.Column(db.Integer)

class Thesis(db.Model):
    ID = db.Column(db.String(25), primary_key=True, nullable=False)
    Author = db.Column(db.String(25), nullable=False)
    Category = db.Column(db.String(25), nullable=False)
    Supervisor = db.Column(db.String(25), nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    File_name = db.Column(db.String(25), nullable=False)

class question(db.Model):
    ID = db.Column(db.String(255), primary_key=True, nullable=False)
    QName = db.Column(db.String(255), nullable=False)
    CorrectA = db.Column(db.String(25), nullable=False)
    DecoyB = db.Column(db.String(25), nullable=False)
    DecoyC = db.Column(db.String(25), nullable=False)
    DecoyD = db.Column(db.String(25), nullable=False)

# ============ NEW MUSIC INSTRUMENT MODEL ============
class Instrument(db.Model):
    __tablename__ = 'instruments'
    
    ID = db.Column(db.String(50), primary_key=True, nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    Vietnamese_Name = db.Column(db.String(255), nullable=False)
    Category = db.Column(db.String(100))  # String, Wind, Percussion, etc.
    Region = db.Column(db.String(100))  # North, Central, South Vietnam
    Description = db.Column(db.Text)
    History = db.Column(db.Text)
    Playing_Technique = db.Column(db.Text)
    
    # Audio and Video
    Audio_File = db.Column(db.String(255))  # Path to audio file
    Video_URL = db.Column(db.String(500))  # YouTube URL
    
    # Images
    Image_Main = db.Column(db.String(255))  # Main instrument image
    Image_Gallery = db.Column(db.Text)  # JSON array of additional images
    
    # Metadata
    Created_At = db.Column(db.DateTime, default=db.func.current_timestamp())
    Updated_At = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
