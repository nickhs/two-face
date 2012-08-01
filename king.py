from rq import Queue, use_connection
from serf import create, upvote

use_connection()
q = Queue('main', default_timeout=1200)

def create_new_user(username):
    return q.enqueue(create, username=username)


def upvote_post(person, title=''):
    return q.enqueue(upvote, username=person.username,
            password=person.password, instance_id=person.instance_id,
            title=title)
