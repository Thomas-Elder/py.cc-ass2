
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from .forms import LoginForm, RegisterForm

bp = Blueprint('authentication', __name__, url_prefix='/authentication')

@bp.route('/register', methods=('GET', 'POST'))
def register():

    form = RegisterForm()

    if request.method == 'POST':

        if form.validate_on_submit():

            return redirect(url_for('login'))

        else:
            return render_template('authentication/register.html', form=form)

    else:
        return render_template('authentication/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if request.method == 'POST':

        if form.validate_on_submit():

            return redirect(url_for('subscription.music'))

        else:
            return render_template('authentication/login.html', form=form)   

    else:
        return render_template('authentication/login.html', form=form)   

@bp.route('/logout', methods=['GET', 'POST'])
def logout():

    return redirect(url_for('index'))