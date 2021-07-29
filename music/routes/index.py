from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, g
from flask_login import current_user

from ..db.dynamodb import get_user, put_user, get_users, get_song, get_songs

bp = Blueprint('', __name__)

@bp.route('/')
@bp.route('/index')
def index():

    return render_template('index.html', current_user=current_user)