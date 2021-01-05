from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
Bootstrap(app)

# create sqlalchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-archive.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# sqlalchemy below
class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    url = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


db.create_all()


@app.route('/')
def home():
    archive = db.session.query(Story).all()
    return render_template("index.html", archive=archive)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_story = Story(
            title=request.form["title"],
            url=request.form["url"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        db.session.add(new_story)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        story_id = request.form["id"]
        story_update = Story.query.get(story_id)
        story_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    story_id = request.args.get('id')
    story_selected = Story.query.get(story_id)
    return render_template("rating.html", story=story_selected)


@app.route("/delete")
def delete():
    story_id = request.args.get('id')
    story_to_delete = Story.query.get(story_id)
    db.session.delete(story_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
