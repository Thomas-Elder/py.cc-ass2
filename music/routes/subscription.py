
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

bp = Blueprint('subscription', __name__, url_prefix='/subscription')

@bp.route('/music', methods=("GET", "POST"))
def music():

    return render_template('subscription/music.html')