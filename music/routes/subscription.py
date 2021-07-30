
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask_login import current_user

from ..db.s3 import get_img
from ..db.dynamodb import get_songs

bp = Blueprint('subscription', __name__, url_prefix='/subscription')

@bp.route('/music', methods=("GET", "POST"))
def music():
    
    songs = get_songs() #list

    for song in songs:
        song.img_url = get_img(song.artist)

    return render_template('subscription/music.html', current_user=current_user, songs=songs)