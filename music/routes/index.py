from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, g
from music.db_spike import get_movie, put_movie

bp = Blueprint('index', __name__, url_prefix='/index')

@bp.route('/')
@bp.route('/index', methods=("GET", "POST"))
def index():

    put_movie("The Big New Movie", 2015, "Nothing happens at all.", 0)

    data = get_movie("The Big New Movie", 2015)

    return render_template('index.html', data=data)