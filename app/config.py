from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:amg123456@127.0.0.1:5432/biblioteca"
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://localhost\SQLEXPRESS:@127.0.0.1:5000/biblioteca"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

db = SQLAlchemy(app)

