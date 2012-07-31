from flask import Flask, request, url_for, redirect, render_template
from flask_peewee.db import Database
from flask_peewee.auth import Auth
from flask_peewee.admin import Admin, ModelAdmin
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
    post_id = TextField(null=True)
    title = TextField()
    created = DateTimeField(default=datetime.datetime.now)
    post_modified = DateTimeField(null=True)

    def __unicode__(self):
        return self.title


class PostAdmin(ModelAdmin):
    columns=('post_id', 'title', 'created', 'post_modified')


class Person(Model):
    username = TextField()
    password = TextField()
    created = DateTimeField(default=datetime.datetime.now)
    instance_id = TextField(null=True)

    def __unicode__(self):
        return self.username


class PersonAdmin(ModelAdmin):
    columns=('username', 'password', 'created', 'instance_id')


class Command(Model):
    name = TextField()
    status = TextField()
    description = TextField()
    user = ForeignKeyField(Person, related_name='command')
    post = ForeignKeyField(Post, related_name='command', null=True)

    def __unicode__(self):
        return self.name


class CommandAdmin(ModelAdmin):
    columns=('name', 'status', 'user', 'post')
    foreign_key_lookups = {'user': 'username'}

admin.register(Post, PostAdmin)
admin.register(Command, CommandAdmin)
admin.register(Person, PersonAdmin)
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
