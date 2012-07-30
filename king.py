from flask import Flask, request, url_for, redirect, render_template
from flask_peewee.db import Database
from flask_peewee.auth import Auth
from flask_peewee.admin import Admin
from peewee import *
from wtfpeewee.orm import model_form
import datetime

DATABASE = {
    'name': 'test.db',
    'engine': 'peewee.SqliteDatabase',
}
SECRET_KEY = 'dasasdads'

app = Flask(__name__)
app.config.from_object(__name__)
db = Database(app)
auth = Auth(app, db)
admin = Admin(app, auth)


class Post(Model):
    post_id = TextField()
    created = DateTimeField(default=datetime.datetime.now)
    post_modified = DateTimeField()


class Villain(Model):
    name = TextField()
    password = TextField()
    location = TextField()
    created = DateTimeField(default=datetime.datetime.now)


class Command(Model):
    name = TextField()
    status = TextField()
    user = None  #FIXME
    post = None  #FIXME


admin.register(Post)
admin.register(Command)
admin.register(Villain)
admin.setup()

CommandForm = model_form(Command)

@app.route('/')
def main():
    return 'Hello World!'


@app.route('/command', methods=['POST', 'GET'])
def new_command():
    return 'hey'

@app.route('/command/<int:id>', methods=['POST'])
def command(id):
    app.logger.info("Received status update for " + str(id))

    if request.form['state'] == 'errored':
        app.logger.error("Task failed!")





if __name__ == '__main__':
    app.run(debug=True)
