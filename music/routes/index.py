from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

bp = Blueprint('index', __name__, url_prefix='/index')

@bp.route('/')
@bp.route('/index', methods=("GET"))
def index():

    return render_template('index.html')