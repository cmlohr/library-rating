from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

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
    review = db.Column(db.String(250), nullable=True)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    img_url = db.Column(db.String(250), unique=True, nullable=False)


db.create_all()


class AddStory(FlaskForm):
    title = StringField("Story Title", validators=[DataRequired()])
    author = StringField("Story Author", validators=[DataRequired()])
    year = StringField("Year Published", validators=[DataRequired()])
    rating = StringField("Rating", validators=[DataRequired()])
    url = StringField("Story URL", validators=[DataRequired()])
    img_url = StringField("Story Image URL", validators=[DataRequired()])
    review = StringField("Review", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    ranking = StringField("Rank", validators=[DataRequired()])
    submit = SubmitField("Add Story")


class RateStory(FlaskForm):
    rating = StringField("Rating")
    review = StringField("Review")
    ranking = StringField("Ranking")
    description = TextAreaField("Description")
    submit = SubmitField("Done")


# add_story = True
# if add_story:
#     test_story = TopTen(
#         id=1,
#         url='www.story.com',
#         title='HatsCats',
#         year=2021,
#         author='Dude',
#         review='Cool Beans!!',
#         rating=5.3,
#         ranking=1,
#         description='yo words and stuff',
#         img_url='https://images.pexels.com/photos/6341566/pexels-photo-6341566.jpeg?auto=compress&cs=tinysrgb&h=750&w=1260',
#     )
#     db.session.add(test_story)
#     db.session.commit()

@app.route("/")
def home():
    listicle = TopTen.query.order_by(TopTen.rating).all()
    for story in range(len(listicle)):
        listicle[story].ranking = len(listicle) - story
    db.session.commit()
    return render_template("index.html", listicle=listicle)


@app.route("/edit", methods=["GET", "POST"])
def rate_story():
    form = RateStory()
    story_id = request.args.get("id")
    story = TopTen.query.get(story_id)
    if form.validate_on_submit():
        story.rating = float(form.rating.data)
        story.review = form.review.data
        story.ranking = form.ranking.data
        story.description = form.description.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", story=story, form=form)


@app.route("/delete")
def delete_story():
    story_id = request.args.get("id")
    story = TopTen.query.get(story_id)
    db.session.delete(story)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddStory()
    if request.method == "POST":
        story = TopTen(
            url=request.form["url"],
            title=request.form["title"],
            year=request.form["year"],
            author=request.form["author"],
            review=request.form["review"],
            rating=request.form["rating"],
            description=request.form["description"],
            img_url=request.form["img_url"],
            ranking=request.form["ranking"]
        )
        db.session.add(story)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html", form=form)


@app.route("/select")
def select():
    return render_template("select.html")


if __name__ == '__main__':
    app.run(debug=True)
