
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from ..db import s3

bp = Blueprint('subscription', __name__, url_prefix='/subscription')

@bp.route('/music', methods=("GET", "POST"))
def music():
    s3.get_img()
    return render_template('subscription/music.html')