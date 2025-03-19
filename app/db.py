import sqlite3
from datetime import datetime

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close() 

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as file: 
        db.executescript(file.read().decode('utf8'))

@click.command('init-db')
def init_db_commnad():
    init_db()
    click.echo('Initialised the database.')

sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def set_admin(username):
    db = get_db()
    db.execute("UPDATE user SET admin = 1 WHERE username = ?", (username,))
    db.commit()
    click.echo(f"User {username} is now an admin.")

@click.command('set-admin')
@click.argument('username')
@with_appcontext
def set_admin_command(username):
    set_admin(username)

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_commnad)
    app.cli.add_command(set_admin_command)
    