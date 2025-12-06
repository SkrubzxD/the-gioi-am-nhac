import sqlite3
conn = sqlite3.connect('example.db')  # Creates a new database file if it doesn’t exist
cursor = conn.cursor()
table_creation_query = """
    CREATE TABLE Thesis (
        ID VARCHAR(255) NOT NULL PRIMARY KEY,
        Author CHAR(25) NOT NULL,
        Category CHAR(25),
        Score INT
    );
"""
cursor.execute(table_creation_query)
cursor.close()

"""
class Thesis(db.Model):
    ID = db.Column(db.String(25), primary_key = True, nullable=False)
    Author = db.Column(db.String(25),nullable = False)
    Category = db.Column(db.String(25), nullable = False)
    Supervisor = db.Column(db.String(25), nullable = False)
    Name = db.Column(db.String(255),nullable = False)
    File_name = db.Column(db.String(25), nullable = False)

"""