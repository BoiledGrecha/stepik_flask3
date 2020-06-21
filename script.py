from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import *
from data import teachers
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stepik.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

for i in teachers:
    teacher = Teacher(name = i["name"], about = i["about"], rating = i["rating"],
        picture = i["picture"], goals = json.dumps(i["goals"]),
        free = json.dumps(i["free"]))
    db.session.add(teacher)
    
db.session.commit()
