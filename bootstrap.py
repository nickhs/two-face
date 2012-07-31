from king import *

auth.User.drop_table()
Command.drop_table()
Post.drop_table()
Person.drop_table()

auth.User.create_table()
Command.create_table()
Post.create_table()
Person.create_table()

admin = auth.User(username='admin', admin=True, active=True)
admin.set_password('admin')
admin.save()
