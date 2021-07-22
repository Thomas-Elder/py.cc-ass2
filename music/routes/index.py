from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, g
from music.db.database import get_user, put_user, get_users, get_song, get_songs

bp = Blueprint('', __name__)

@bp.route('/')
def index():

    user = get_user(email='s33750870@student.rmit.edu.au')
    all_users = get_users()

    song = get_song(title='1904', artist='The Tallest Man on Earth')
    all_songs = get_songs()

    return render_template('index.html', user=user, all_users=all_users, song=song, all_songs=all_songs)