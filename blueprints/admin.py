from flask import Blueprint, render_template, redirect, url_for, session
from config import config
from functools import wraps

admin = Blueprint('admin', __name__)


def db_read(*args):
    return 'hey'


def db_execute(*args):
    return 'hey'

def admin_only(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if session.get('admin') == config.admin_token:
            return function(*args, **kwargs)
        else:
            return 'badman'
    return wrapper


@admin.route('/')
@admin_only
def home():
    data = db_read('select name, plaintext from topics')
    return render_template('admin/home.html', data=data)


@admin.route('/<topic>')
@admin_only
def topics(topic):
    data = db_read(
        """ select courses.name, t.plaintext, courses.plaintext, courses.approved, courses.id, t.name from courses
                join topics t on t.id = courses.topic_id
                where t.plaintext = ?;""",
        [topic]
    )
    print(data)
    return render_template('admin/topics.html', data=data, topic=topic)


@admin.route('/<topic>/<course>')
@admin_only
def courses(topic, course):
    data = db_read(
        """ select t.first_name, t.last_name, classes.period, classes.id, classes.approved, t2.name, c.name from classes
                join teachers t on t.id = classes.teacher_id
                join courses c on c.id = classes.course_id
                join topics t2 on t2.id = c.topic_id
                where t2.plaintext = ? and c.plaintext = ?""",
        [topic, course]
    )
    print(data)
    return render_template('admin/courses.html', data=data, topic=topic, course=course)


@admin.route('/update/<action>/topic/<course_id>/<redirect_topic>')
@admin_only
def approve_course(action, course_id, redirect_topic):
    if action == 'approve':
        db_execute('update courses set approved = true where id = ?;', [course_id])
    elif action == 'decline':
        db_execute('delete from courses where id = ?;', [course_id])
    return redirect(url_for('admin.topics', topic=redirect_topic))


@admin.route('/update/<action>/course/<class_id>/<redirect_topic>/<redirect_course>')
@admin_only
def approve_class(action, class_id, redirect_topic, redirect_course):
    if action == 'approve':
        db_execute('update classes set approved = true where id = ?;', [class_id])
    elif action == 'decline':
        db_execute('delete from classes where id = ?;', [class_id])
    return redirect(url_for('admin.courses', topic=redirect_topic, course=redirect_course))
