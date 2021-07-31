import os

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask_login import current_user

from ..db.s3 import get_img
from ..db.dynamodb import get_songs, get_user_songs, rm_user_song, put_user_song
from .forms import QueryForm

bp = Blueprint('subscription', __name__, url_prefix='/subscription')

@bp.route('/music/query_songs', methods=["GET"])
@bp.route('/music', methods=["GET"])
def music(query_songs=[]):
    form = QueryForm()

    # set up query_songs
    #query_songs = []
    get_songs()
    # get user songs and images:
    user_songs = get_user_songs(current_user.email) #list

    # If we're local, use place holder images.
    if os.environ['FLASK_ENV'] == "dev":
            for song in user_songs:
                song.img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Test-Logo.svg/783px-Test-Logo.svg.png"
    else:
        for song in user_songs:
            song.img_url = get_img(song.artist)

    return render_template('subscription/music.html', current_user=current_user, user_songs=user_songs, query_songs=query_songs, form=form)


@bp.route('/music/remove', methods=["POST"])
def remove():

    # parse request
    print(f"Removing: {request.form['artist']}:{request.form['title']}")

    # remove song 
    rm_user_song(current_user.email, request.form['artist'], request.form['title'])

    # redirect to music
    return redirect(url_for('subscription.music'))

@bp.route('/music/subscribe', methods=["POST"])
def subscribe():

    # parse request
    print(f"Subscribing: {request.form['artist']}:{request.form['title']}")

    # add song 
    put_user_song(current_user.email, request.form['artist'], request.form['title']) 

    # redirect to music  
    return redirect(url_for('subscription.music'))

@bp.route('/music/query', methods=["POST"])
def query():
    # parse request
    print(f"Subscribing: {request.form['artist']}:{request.form['title']}:{request.form['year']}")

    # query db
    query_songs = get_songs(artist=request.form['artist'], title=request.form['title'], year=request.form['year'])

    # redirect to music  
    return redirect(url_for('subscription.music', query_songs=query_songs))