from datetime import datetime
from MuseumProject import db, login_manager
from flask_login import UserMixin

#Funzione per ricaricare l id dell admin dalla sessione
@login_manager.user_loader
def load_user(user_id):
    return Administrator.query.get(int(user_id))


class Administrator(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(45), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    posts = db.relationship('Post', backref='poster', lazy=True)                                #Un Admin può inserire più post

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    descrizione = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    admin_id = db.Column(db.Integer, db.ForeignKey('administrator.id'), nullable=False)         #Chiave esterna che fa riferimento alla tab.Administrator