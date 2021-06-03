from flask import Blueprint, render_template
# from database.sql import db_read
from database.sql import Topics, Courses, Teachers, Classes


def db_read(*args):
    return 'hey'


navigation = Blueprint('navigation', __name__)


@navigation.route('/')
def home():
    data = Topics.select()
    return render_template('navigation/home.html', data=data)


@navigation.route('/<topic>')
def topics(topic):
    data = Courses.select().join(Topics).where(Courses.topic.plaintext == topic and Courses.approved)
    print(data)
    return render_template('navigation/topics.html', data=data)


@navigation.route('/<topic>/<course>')
def courses(topic, course):
    data = (Classes.select()
            .join(Teachers, on=(Classes.teacher == Teachers.id))
            .join(Courses, on=(Classes.course == Courses.id))
            .join(Topics, on=(Courses.topic == Topics.id))
            .where(Classes.course.topic.plaintext == topic and Classes.course.plaintext == course and Classes.approved))
    print(data)
    return render_template('navigation/courses.html', data=data)
