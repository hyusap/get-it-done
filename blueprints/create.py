from flask import Blueprint, request, render_template, flash, redirect
# from database.sql import db_read, db_execute
from database.sql import Topics, Courses, Teachers, Classes, Work


create = Blueprint('create', __name__)


@create.route('/')
def create_index():
    return render_template('creation/create.html')


@create.route('/course', methods=["GET", "POST"])
def make_course():
    if request.method == 'GET':
        data = Topics.select()
        return render_template('creation/course.html', data=data)
    else:
        name = request.form.get('name')
        id = request.form.get('under')
        Courses.create(name=name, topic=id, plaintext=name.replace(" ", "").lower())
        flash(f"You created course \"{name}\" successfully! Please wait for it to be approved by an admin!")
        return redirect('/home')


@create.route('/teacher', methods=["GET", "POST"])
def make_teacher():
    if request.method == 'GET':
        return render_template('creation/teacher.html')
    else:
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        Teachers.create(first_name=firstname, last_name=lastname)
        flash(f"You created teacher \"{firstname} {lastname}\" successfully!")
        return redirect('/home')


@create.route('/class', methods=["GET", "POST"])
def make_class():
    if request.method == 'GET':
        teachers = Teachers.select()
        courses = Courses.select()
        return render_template('creation/class.html', teachers=teachers, courses=courses)
    else:
        course = request.form.get('course')
        teacher = request.form.get('teacher')
        period = request.form.get('period')
        Classes.create(course=course, teacher=teacher, period=period)
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

        Work.create(from_class=class_id, name=name, description=description, url=url, due_by=date)

        flash(f"You created the item successfully!")
        return redirect('/home')
