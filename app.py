from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


@app.route('/')
def hello_world():
    pass


@app.route("/add-artist/", methods=["GET", "POST"])
def add_artist():
    if request.method == "POST":
        name_artist = request.form["name"]
        print(name_artist)
        execute(f"INSERT INTO artist (name) VALUES ('{name_artist}')")
        return redirect("/artists")
    else:
        return render_template("add-artist.html")


@app.route("/artists/")
def get_artists():
    artists = execute("SELECT * FROM artist").fetchall()
    return render_template("artists.html", artists=artists)


def execute(query):
    with sqlite3.connect("music.db") as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return cursor


if __name__ == '__main__':
    app.run(debug=True)
