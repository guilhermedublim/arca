from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Gui/Documents/Projetos/arca/arca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'f72ad5e885b6f80af8ab99c5faf3bdd4561165956e4af1a5f0764a21c6bd4ec5'
app.config['DEBUG'] = True

db = SQLAlchemy()
db.init_app(app)