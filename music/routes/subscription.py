import os

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask_login import current_user

from ..db.s3 import get_img
from ..db.dynamodb import get_songs
from .forms import QueryForm

bp = Blueprint('subscription', __name__, url_prefix='/subscription')

@bp.route('/music', methods=("GET", "POST"))
def music():
    
    form = QueryForm()

    songs = get_songs() #list

    if os.environ['FLASK_ENV'] == "dev":
        for song in songs:
            song.img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Test-Logo.svg/783px-Test-Logo.svg.png"
    else:
        for song in songs:
            song.img_url = get_img(song.artist)

    return render_template('subscription/music.html', current_user=current_user, songs=songs, form=form)