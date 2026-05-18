from flask import Flask, render_template, request, redirect, url_for, session, g
from werkzeug.utils import escape
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'reviews.db')

app = Flask(__name__)
app.secret_key = 'replace-with-a-secure-secret-key'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


def init_db():
    if not os.path.exists(DATABASE):
        with sqlite3.connect(DATABASE) as conn:
            conn.execute(
                '''
                CREATE TABLE reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    trail TEXT NOT NULL,
                    rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
                    comment TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                '''.strip()
            )
            conn.commit()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/hiking')
def hiking():
    return render_template('hiking.html')


@app.route('/packing')
def packing():
    return render_template('packing.html')


@app.route('/weather')
def weather():
    return render_template('weather.html')


@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    db = get_db()
    if request.method == 'POST':
        name = escape(request.form.get('name', '').strip())
        trail = escape(request.form.get('trail', '').strip())
        rating = request.form.get('rating', '5')
        comment = escape(request.form.get('comment', '').strip())

        if not name or not trail or not comment:
            session['message'] = 'Please complete every field before submitting.'
            return redirect(url_for('reviews'))

        try:
            rating_value = int(rating)
        except ValueError:
            rating_value = 5

        db.execute(
            'INSERT INTO reviews (name, trail, rating, comment) VALUES (?, ?, ?, ?)',
            (name, trail, rating_value, comment)
        )
        db.commit()
        session['message'] = 'Thank you! Your review has been added to the Connecticut hiking community.'
        return redirect(url_for('reviews'))

    rows = db.execute('SELECT name, trail, rating, comment, created_at FROM reviews ORDER BY created_at DESC LIMIT 10').fetchall()
    message = session.pop('message', None)
    return render_template('reviews.html', reviews=rows, message=message)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
