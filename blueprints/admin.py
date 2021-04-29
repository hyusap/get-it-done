from flask import Blueprint, render_template, redirect, url_for, session
from config import config
from functools import wraps
from database.sql import Topics, Courses, Teachers, Classes

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
    data = Topics.select()
    return render_template('admin/home.html', data=data)


@admin.route('/<topic>')
@admin_only
def topics(topic):
    data = Courses.select().join(Topics).where(Courses.topic.plaintext == topic)
    print(data)
    return render_template('admin/topics.html', data=data, topic=topic)


@admin.route('/<topic>/<course>')
@admin_only
def courses(topic, course):
    data = (Classes.select()
            .join(Teachers)
            .join(Courses)
            .join(Topics)
            .where(Classes.course.topic.plaintext == topic and Classes.course.plaintext == course))

    print(data)
    return render_template('admin/courses.html', data=data, topic=topic, course=course)


@admin.route('/update/<action>/topic/<course_id>/<redirect_topic>')
@admin_only
def approve_course(action, course_id, redirect_topic):
    if action == 'approve':
        c = Courses.get_by_id(course_id)
        c.approved = True
        c.save()
    elif action == 'decline':
        Courses.delete_by_id(course_id)
    return redirect(url_for('admin.topics', topic=redirect_topic))


@admin.route('/update/<action>/course/<class_id>/<redirect_topic>/<redirect_course>')
@admin_only
def approve_class(action, class_id, redirect_topic, redirect_course):
    if action == 'approve':
        c = Classes.get_by_id(class_id)
        c.approved = True
        c.save()
    elif action == 'decline':
        Classes.delete_by_id(class_id)
    return redirect(url_for('admin.courses', topic=redirect_topic, course=redirect_course))
