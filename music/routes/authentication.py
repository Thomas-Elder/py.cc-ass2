
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask_login import login_user, logout_user, login_required, current_user

from ..db.dynamodb import get_user
from .forms import LoginForm, RegisterForm

bp = Blueprint('authentication', __name__, url_prefix='/authentication')

@bp.route('/register', methods=('GET', 'POST'))
def register():

    form = RegisterForm()

    if request.method == 'POST':

        if form.validate_on_submit():

            return redirect(url_for('authentication.login'))

        else:
            return render_template('authentication/register.html', form=form)

    else:
        return render_template('authentication/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if request.method == 'POST':

        if form.validate_on_submit():
            login_user(get_user(form.email.data))
            return redirect(url_for('subscription.music'))

        else:
            return render_template('authentication/login.html', form=form)   

    else:
        return render_template('authentication/login.html', form=form)   

@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))