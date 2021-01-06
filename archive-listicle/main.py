from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345678'
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///top-ten.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class TopTen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    url = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    img_url = db.Column(db.String(250), unique=True, nullable=False)


db.create_all()
# game = True
# if game:
#     test_story = TopTen(
#         id=1,
#         url='www.story.com',
#         title='HatsCats',
#         year=2021,
#         author='Dude',
#         rating=5.3,
#         ranking=1,
#         description='yo words and stuff',
#         img_url='https://images.pexels.com/photos/6341566/pexels-photo-6341566.jpeg?auto=compress&cs=tinysrgb&h=750&w=1260',
#     )
#     db.session.add(test_story)
#     db.session.commit()

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/edit")
def edit():
    return render_template("edit.html")


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/select")
def select():
    return render_template("select.html")


if __name__ == '__main__':
    app.run(debug=True)
