from flask import Blueprint, render_template
# from database.sql import db_read


def db_read(*args):
    return 'hey'

navigation = Blueprint('navigation', __name__)


@navigation.route('/')
def home():
    data = db_read('select name, plaintext from topics')
    return render_template('navigation/home.html', data=data)


@navigation.route('/<topic>')
def topics(topic):
    data = db_read(
        """ select courses.name, t.plaintext, courses.plaintext from courses
                join topics t on t.id = courses.topic_id
                where t.plaintext = ? and approved = true;""",
        [topic]
    )
    print(data)
    return render_template('navigation/topics.html', data=data)


@navigation.route('/<topic>/<course>')
def courses(topic, course):
    data = db_read(
        """ select t.first_name, t.last_name, classes.period, classes.id from classes
                join teachers t on t.id = classes.teacher_id
                join courses c on c.id = classes.course_id
                join topics t2 on t2.id = c.topic_id
                where t2.plaintext = ? and c.plaintext = ? and classes.approved = true;""",
        [topic, course]
    )
    print(data)
    return render_template('navigation/courses.html', data=data)
