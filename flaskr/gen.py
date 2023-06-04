import functools
import random
from faker import Faker
from faker_music import MusicProvider
from flask import (
    Blueprint, flash, render_template, request, session, url_for
)


from flaskr.db import get_db
fake = Faker()
fake.add_provider(MusicProvider)
bp = Blueprint('gen', __name__,)
url_prefix = '/song_list'


@bp.route('/generated_list/', methods=('GET', 'POST'))
def generate():
    db = get_db()
    count = db.execute('SELECT COUNT(*) FROM songs').fetchone()[0]
    if count == 0:
        genre_lst = []
        artist_lst = []
        song_qty = random.randint(10, 100)
        genre_qty = random.randint(4, 8)
        artist_qty = random.randint(4, 20)
        for y in range(genre_qty):
            genre_lst.append(fake.music_genre())
        for y in range(artist_qty):
            artist_lst.append(fake.name())
        for i in range(song_qty):
            title = fake.sentence(nb_words=3)
            artist = random.choice(artist_lst)
            genre = random.choice(genre_lst)
            length = fake.random_int(min=60, max=300)
            db.execute(
                'INSERT INTO songs (title, artist, genre, length)'
                ' VALUES (?, ?, ?, ?)',
                (title, artist, genre, length)
            )
    db.commit()
    genre_choice = db.execute('SELECT DISTINCT genre FROM songs;').fetchall()
    data = db.execute('SELECT * FROM songs').fetchall()
    flash('List of songs generated')
    db.close()
    return render_template('song_list.html', data=data, genre_choice=genre_choice)
