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

    # set up query_songs
    query_songs = []

    # get user songs and images:
    user_songs = get_songs() #list

    if os.environ['FLASK_ENV'] == "dev":
            for song in user_songs:
                song.img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Test-Logo.svg/783px-Test-Logo.svg.png"
    else:
        for song in user_songs:
            song.img_url = get_img(song.artist)

    if request.method == 'GET':
        
        return render_template('subscription/music.html', current_user=current_user, user_songs=user_songs, query_songs=query_songs, form=form)

    elif request.method == 'POST':

        if form.validate_on_submit():

            # get query songs

            return render_template('subscription/music.html', current_user=current_user, user_songs=user_songs, query_songs=query_songs, form=form)

        else:
            return render_template('subscription/music.html', current_user=current_user, user_songs=user_songs, query_songs=query_songs, form=form)