from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from flaskr.db import get_db

bp = Blueprint('done', __name__, )


@bp.route('/names')
def names():
    db = get_db()
    data = db.execute('SELECT COUNT(DISTINCT artist) FROM songs;').fetchone()
    db.close()
    flash('Quantity of uniq artists in list is:')
    return render_template('func_1.html', data=data)


@bp.route('/tracks')
def tracks():
    db = get_db()
    data = db.execute('SELECT MAX (id) FROM songs;').fetchone()
    db.close()
    return render_template('func_2.html', data=data)


@bp.route('/genre', methods=['GET', 'POST'])
def genre():
    if request.method == 'POST':
        gen = request.form["nm"]
        # return f'{request.form["nm"]}'
        return redirect(url_for("done.gen_list", genre_c=gen))
    else:
        db = get_db()
        genre_choice = db.execute('SELECT DISTINCT genre FROM songs;').fetchall()
        db.close()
        return render_template('func_3.html', data=genre_choice)


@bp.route('/<genre_c>')
def gen_list(genre_c):
    db = get_db()
    genre_list = db.execute('SELECT * FROM songs WHERE genre = ?', (genre_c,)).fetchall()
    qty = db.execute('SELECT genre, COUNT (id) AS total_length FROM songs WHERE genre = ? GROUP BY genre',
                     (genre_c,)).fetchone()
    db.close()
    return render_template('func_3_res.html', data=genre_list, qty=qty)


@bp.route('/tracks_sec')
def tracks_sec():
    db = get_db()
    data = db.execute('SELECT id, title, length FROM songs;').fetchall()
    db.close()
    return render_template('func_4.html', data=data)


@bp.route('/statistic')
def statistic():
    db = get_db()
    avg_length = round(db.execute('SELECT AVG (length) FROM songs').fetchone()[0], 2)
    total_length = db.execute('SELECT SUM (length) FROM songs').fetchone()[0]
    db.close()
    return render_template('func_5.html', avg_length=avg_length, total_length=total_length)
