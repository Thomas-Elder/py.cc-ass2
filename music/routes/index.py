from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, g
from music.database import get_user, put_user

bp = Blueprint('', __name__)

@bp.route('/')
def index():

    data = get_user('s33750870@student.rmit.edu.au', 'Tom Elder0')

    return render_template('index.html', data=data)