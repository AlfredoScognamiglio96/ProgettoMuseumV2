from datetime import datetime                                          #Modulo per l'attuale date time
from MuseumProject import db, login_manager                            #LoginManager gestisce le funzionalità legate alla sessione
from flask_login import UserMixin                                      #UserMixin fornisce l implementazione di verifica di dati immessi

#Decorator Function per ricaricare l id dell admin dalla sessione
@login_manager.user_loader
def load_user(user_id):
    return Administrator.query.get(int(user_id))                                                #Ottiene l id dell utente e lo restituisce al LoginManager


class Administrator(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(45), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    posts = db.relationship('Post', backref='poster', lazy=True)                                #Un Admin può inserire più post (Relazione 1:N)
                                                                                                #Lazy=True è un parametro che effettua una SELECT durante il caricamento
                                                                                                #della classe
                                                                                                #Tramite il par.backref possiamo ottenere l utente che ha creato il post
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    descrizione = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post_image = db.Column(db.String(20), nullable=False, default='defaultPNG.png')
    admin_id = db.Column(db.Integer, db.ForeignKey('administrator.id'), nullable=False)         #Chiave esterna che fa riferimento alla tab.Administrator
