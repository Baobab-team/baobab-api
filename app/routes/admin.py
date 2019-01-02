import flask
from flask import render_template, request, redirect, flash, Blueprint
from flask_login import login_user, logout_user, login_required

from app.forms import LoginForm
from app.models.users import User

bp = Blueprint('auth', __name__, url_prefix='/')


@bp.route("/login", methods=['POST', 'GET'])
def admin():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            if user.check_password(form.password.data):

                login_user(user,remember=form.remember.data)

                flash('Logged in successfully.')
                return redirect('/admin')
            else:
                flash('Email or password dont match')
        else:
            flash('No user with given email')

    return render_template("admin/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')

    return redirect("/")



