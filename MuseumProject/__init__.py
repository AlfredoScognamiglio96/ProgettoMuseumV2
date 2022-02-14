from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager                           #Modello per gestire le sessioni degli utenti

app = Flask(__name__)                                          #__name__ è una var.speciale indicante il nome del modulo
app.config['SECRET_KEY'] = 'chiaveSegreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'    #Percorso creato nella directory del progetto che conterrà il file del DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)                                           #Istanza DB
login_manager = LoginManager(app)                              #Istanza LoginManager
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from MuseumProject import routes                                #Richiamo qui routes per evitare il problema degli import circolari