from flask import Flask, render_template
from database.sql import database, db_read

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    data = db_read('select name, plaintext from topics')
    return render_template('home.html', data=data)


@app.route('/home/<topic>')
def topics(topic):
    data = db_read(
        'select courses.name, t.plaintext, courses.plaintext from courses join topics t on t.id = courses.topic_id where t.plaintext = ?',
        [topic]
    )
    print(data)
    return render_template('topics.html', data=data)


@app.route('/home/<topic>/<course>')
def courses(topic, course):
    data = db_read(
        """
        select t.first_name, t.last_name, classes.period from classes
            join teachers t on t.id = classes.teacher_id
            join courses c on c.id = classes.course_id
            join topics t2 on t2.id = c.topic_id
            where t2.plaintext = ? and c.plaintext = ?
        """,
        [topic, course]
    )
    print(data)
    return render_template('courses.html', data=data)


if __name__ == '__main__':
    app.run()
