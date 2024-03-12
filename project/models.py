from app import db

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    table_title = db.Column(db.String(100))
    table_text = db.Column(db.String(200))
    literature = db.Column(db.String(100))
    requirements_file = db.Column(db.String(100), nullable=True)
