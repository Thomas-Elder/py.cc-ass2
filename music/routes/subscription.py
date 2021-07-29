
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask_login import current_user

from ..db import s3

bp = Blueprint('subscription', __name__, url_prefix='/subscription')

@bp.route('/music', methods=("GET", "POST"))
def music():

    return render_template('subscription/music.html', current_user=current_user)