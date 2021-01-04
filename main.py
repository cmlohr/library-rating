from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
import sqlite3
app = Flask(__name__)
Bootstrap(app)

archive = []

db = sqlite3.connect("archive.db")
cursor = db.cursor()
# db creation
# cursor.execute("CREATE TABLE archive (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) "
#                "NOT NULL, url varchar(250) NOT NULL UNIQUE, rating FLOAT NOT NULL)")
cursor.execute("INSERT INTO archive VALUES(1, 'Beowulf', 'Unknown', "
               "'https://archive.org/stream/cu31924013339373/cu31924013339373_djvu.txt', '9.5')")
db.commit()

@app.route('/')
def home():
    return render_template("index.html", archive=archive)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_story = {
            "title": request.form["title"],
            "url": request.form["url"],
            "author": request.form["author"],
            "rating": request.form["rating"]
        }
        archive.append(new_story)
        return redirect(url_for('home'))
    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)

