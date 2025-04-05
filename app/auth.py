import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user

from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

login_manager = LoginManager()

class User(UserMixin):
    def __init__(self, id, username, password, email, admin):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.admin = admin
        

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        if user:
            return User(user['id'], user['username'], user['password'], user['email'], user['admin'])
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def init_login_manager(app):
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'


@bp.before_app_request
def load_logged_in_user():
    g.user = current_user

# @bp.before_app_request
# def load_logged_in_user():
#     user_id = session.get('user_id')

#     if user_id is None:
#         g.user = None
#     else:
#         g.user = get_db().execute(
#             'SELECT * FROM user WHERE id = ?', (user_id,)
#         ).fetchone()

@bp.route('/login', methods=('GET', 'POST'))
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user_data = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user_data is None:
            error = 'Incorrecdt username.'
        elif not check_password_hash(user_data['password'], password):
            error = 'Incorrect password'

        if error is None:
            user = User(user_data['id'], user_data['username'], user_data['password'], user_data['email'], user_data['admin'])
            login_user(user)
            return redirect(url_for('index'))
        
        flash(error)

    return render_template('auth/login.html')


@bp.route('/register', methods=('GET', 'POST'))
def register():

    print("hello register world")

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        db = get_db()
        error = None


    #     user = db.execute(
    #         'SELECT * FROM user WHERE username = ?', (username,)
    #     ).fetchone()

        if not username:
            error = 'Incorrecdt username.'
        elif not password:
            error = 'Incorrect password'
        elif not email:
            error = 'Incorrect Email'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password, email) VALUES (?,?,?)",
                    (username, generate_password_hash(password), email),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} or {email} is already registered"
            else:
                return (redirect(url_for("auth.login")))
        
        flash(error)

    return render_template('auth/register.html')

@bp.route('/logout', methods=('GET', 'POST'))
def logout(): 
    logout_user()
    return redirect(url_for('index'))