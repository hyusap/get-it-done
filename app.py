from flask import Flask, render_template, request, session, redirect
from database.sql import Work

from blueprints.navigation import navigation
from blueprints.create import create
from blueprints.admin import admin

from config import config

app = Flask(__name__)
app.secret_key = config.secret_key
app.register_blueprint(navigation, url_prefix='/home')
app.register_blueprint(create, url_prefix='/create')
app.register_blueprint(admin, url_prefix='/admin')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/classes/<class_id>')
def classes(class_id):
    data = Work.select().where(Work.class_id == class_id).order_by(Work.due_by)
    print(data)
    return render_template('navigation/classes.html', data=data)


@app.route('/admin-token', methods=['GET', 'POST'])
def admintoken():
    if session.get('admin') == config.admin_token:
        return redirect('/admin')
    if request.method == 'POST':
        session['admin'] = request.form.get('token-input')
        print(session['admin'])
        return redirect('/admin')
    return render_template('admin/admin-token.html')

if __name__ == '__main__':
    app.run('0.0.0.0')
