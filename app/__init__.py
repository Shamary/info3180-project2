from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY']="some secret key"
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://qotncqxpjnadou:dd7b939d5a654ab064c63ae28754bd4770bd91a052bb5f89209c5e044f3cc43d@ec2-54-163-254-76.compute-1.amazonaws.com:5432/da45gk7jcucbaa"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db=SQLAlchemy(app)

login_m=LoginManager()
login_m.init_app(app)
login_m.login_view='login'


app.config.from_object(__name__)
from app import views