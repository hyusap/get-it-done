from flask import Blueprint, request, render_template, flash, redirect
# from database.sql import db_read, db_execute


def db_read(*args):
    return 'hey'


def db_execute(*args):
    return 'hey'


create = Blueprint('create', __name__)


@create.route('/')
def create_index():
    return render_template('creation/create.html')


@create.route('/course', methods=["GET", "POST"])
def make_course():
    if request.method == 'GET':
        data = db_read('select name, id from topics')
        return render_template('creation/course.html', data=data)
    else:
        name = request.form.get('name')
        id = request.form.get('under')
        db_execute(
            'insert into courses (name, topic_id, plaintext) values (?, ?, ?)',
            [name, id, name.replace(" ", "").lower()]
        )
        flash(f"You created course \"{name}\" successfully! Please wait for it to be approved by an admin!")
        return redirect('/home')


@create.route('/teacher', methods=["GET", "POST"])
def make_teacher():
    if request.method == 'GET':
        return render_template('creation/teacher.html')
    else:
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        db_execute(
            'insert into teachers (first_name, last_name) values (?, ?)',
            [firstname, lastname]
        )
        flash(f"You created teacher \"{firstname} {lastname}\" successfully!")
        return redirect('/home')


@create.route('/class', methods=["GET", "POST"])
def make_class():
    if request.method == 'GET':
        teachers = db_read('select id, first_name, last_name from teachers')
        courses = db_read('select id, name from courses')
        return render_template('creation/class.html', teachers=teachers, courses=courses)
    else:
        course = request.form.get('course')
        teacher = request.form.get('teacher')
        period = request.form.get('period')
        db_execute(
            'insert into classes (course_id, teacher_id, period) values (?, ?, ?)',
            [course, teacher, period]
        )
        flash(f"You created the class successfully! Please wait for it to be approved by an admin!")
        return redirect('/home')


@create.route('/item', methods=["GET", "POST"])
def make_item():
    if request.method == 'GET':
        return render_template('creation/item.html')
    else:
        class_id = request.form.get('class_id')
        name = request.form.get('name')
        description = request.form.get('description')
        url = request.form.get('url')
        date = request.form.get('date')

        db_execute(
            'insert into work (class_id, name, description, url, due_by) values (?, ?, ?, ?, ?)',
            [class_id, name, description, url, date]
        )

        flash(f"You created the item successfully!")
        return redirect('/home')
