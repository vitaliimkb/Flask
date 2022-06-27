from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


@app.route('/')
def hello_world():
    context = dict()
    songs = execute(f"""
                SELECT song.id, song.name, artist.name FROM song 
                INNER JOIN artist ON song.artist_id = artist.id
            """).fetchall()
    artists = execute(f"""
                SELECT * FROM artist
        """).fetchall()

    context['songs'] = songs
    context['artists'] = artists
    context['heading'] = "Main"
    return render_template("index.html", **context)


# ------------------------Artists----------------------------------------


@app.route("/add-artist/", methods=["GET", "POST"])
def add_artist():
    if request.method == "POST":
        name_artist = request.form["name"]
        execute(f"INSERT INTO artist (name) VALUES ('{name_artist}')")
        return redirect("/artists")
    else:
        return render_template("add-artist.html", heading="Add artist")


@app.route("/artists/")
def get_artists():
    artists = execute("SELECT * FROM artist").fetchall()
    return render_template("artists.html", artists=artists, heading="Artists")


@app.route("/artists/<int:pk>/delete")
def artist_delete(pk):
    execute(f"DELETE FROM artist WHERE id={pk}")
    return redirect("/artists")


@app.route("/artists/<int:pk>/edit", methods=["GET", "POST"])
def artist_edit(pk):
    if request.method == "POST":
        name_artist = request.form["name"]
        execute(f"UPDATE artist SET name='{name_artist}' WHERE id={pk}")
        return redirect("/artists")
    else:
        artist = execute(f"SELECT * FROM artist WHERE id={pk}").fetchone()
        return render_template("add-artist.html", artist=artist, heading="Edit artist")


# ------------------------Artists----------------------------------------


# ------------------------Genres----------------------------------------


@app.route("/add-genre/", methods=["GET", "POST"])
def add_genre():
    if request.method == "POST":
        name_genre = request.form["name"]
        execute(f"INSERT INTO genre (name) VALUES ('{name_genre}')")
        return redirect("/genres")
    else:
        return render_template("add-genre.html", heading="Add genre")


@app.route("/genres/")
def get_genres():
    genres = execute("SELECT * FROM genre").fetchall()
    return render_template("genres.html", genres=genres, heading="Genres")


@app.route("/genres/<int:pk>/delete")
def genre_delete(pk):
    execute(f"DELETE FROM genre WHERE id={pk}")
    return redirect("/genres")


@app.route("/genres/<int:pk>/edit", methods=["GET", "POST"])
def genre_edit(pk):
    if request.method == "POST":
        name_genre = request.form["name"]
        execute(f"UPDATE genre SET name='{name_genre}' WHERE id={pk}")
        return redirect("/genres")
    else:
        genre = execute(f"SELECT * FROM genre WHERE id={pk}").fetchone()
        return render_template("add-genre.html", genre=genre, heading="Edit genre")


# ------------------------Genres----------------------------------------


# ------------------------Songs----------------------------------------

@app.route("/add-song", methods=["GET", "POST"])
def add_song():
    if request.method == "POST":
        insert_full_song()
        return redirect("/songs")
    else:
        return render_template("add-song.html", **get_artists_and_genres(), heading="Add song")


@app.route("/songs")
def get_songs():
    songs = execute("""
        SELECT song.id, song.name, artist.name FROM song 
        INNER JOIN artist ON song.artist_id = artist.id
    """).fetchall()
    return render_template("songs.html", songs=songs, heading="Songs")


@app.route("/songs/<int:pk>/delete")
def song_delete(pk):
    execute(f"DELETE FROM song WHERE id={pk}")
    execute(f"DELETE FROM song_genre WHERE song_id={pk}")
    return redirect("/songs")


@app.route("/songs/<int:pk>/edit", methods=["GET", "POST"])
def edit_track(pk):
    if request.method == "POST":
        update_full_song(pk)
        return redirect("/")
    else:
        song = execute(f"""SELECT a.id, a.name AS artist, s.name AS song
                            FROM song AS s
                            INNER JOIN artist a ON s.artist_id = a.id
                            WHERE s.id = {pk}""").fetchone()

        genres = execute(f"""SELECT id, name FROM song_genre 
        INNER JOIN genre g on g.id = song_genre.genre_id 
        WHERE song_id={pk}""").fetchall()
        return render_template("edit-song.html", song=song, **get_artists_and_genres(), current_genres=genres)


def insert_full_song():
    title = request.form['title']
    artist = request.form['artist']
    genres = request.form.getlist('genres')

    last_song_id = execute(f"INSERT INTO song (name, artist_id) VALUES {title, artist}").lastrowid
    for genre in genres:
        execute(f"INSERT INTO song_genre (song_id, genre_id) VALUES {last_song_id, genre}")


def update_full_song(pk):
    title = request.form['title']
    artist = request.form['artist']
    genres = request.form.getlist('genre')
    execute(f"UPDATE song SET name='{title}', artist_id={artist} WHERE id={pk}")
    execute(f"DELETE FROM song_genre WHERE song_id={pk}")
    for genre in genres:
        execute(f"INSERT INTO song_genre (song_id, genre_id) VALUES {pk, genre}")


def get_artists_and_genres():
    context = dict()
    artists = execute("SELECT * FROM artist ORDER BY name")
    genres = execute("SELECT * FROM genre ORDER BY name")
    context['artists'] = artists
    context['genres'] = genres
    return context


# ------------------------Songs----------------------------------------


# ------------------------Other----------------------------------------

@app.route("/search")
def search():
    context = dict()
    query = request.values['query']
    songs = execute(f"""
            SELECT song.id, song.name, artist.name FROM song 
            INNER JOIN artist ON song.artist_id = artist.id
            WHERE song.name LIKE '%{query}%'
        """).fetchall()
    artists = execute(f"""
            SELECT * FROM artist WHERE artist.name LIKE '%{query}%'
    """).fetchall()

    context['songs'] = songs
    context['artists'] = artists
    context['heading'] = "Search results"
    return render_template("index.html", **context)


@app.route("/songs/<int:pk>/detail")
def song_detail(pk):
    song = execute(f"""
        SELECT s.id, a.name AS artist, s.name AS song_name, GROUP_CONCAT(g.name) AS genre
        FROM song as s 
        INNER JOIN song_genre sg on s.id = sg.song_id
        INNER JOIN genre g on g.id = sg.genre_id
        INNER JOIN artist a on s.artist_id = a.id
        WHERE s.id = {pk}
    """).fetchone()
    return render_template("song-detail.html", song=song)


@app.route("/artists/<int:pk>/songs")
def songs_by_artist(pk):
    songs = execute(f"""
                SELECT song.id, song.name, artist.name FROM song 
                INNER JOIN artist ON song.artist_id = artist.id
                WHERE artist_id = {pk}
            """).fetchall()
    return render_template("index.html", songs=songs)

def execute(query):
    with sqlite3.connect("C:/Users/Vitalii/PycharmProjects/Flask/music.db") as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return cursor

# song edit
# song by artist


if __name__ == '__main__':
    app.run(debug=True)
# ------------------------Other----------------------------------------
