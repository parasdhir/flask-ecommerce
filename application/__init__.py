
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'your_secret_key'
login_manager = LoginManager(app)
bcrpyt = Bcrypt(app)







from application import routes