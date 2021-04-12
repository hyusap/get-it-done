from flask import Flask, render_template, request, session, redirect
from database.sql import db_read

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
    data = db_read(
        """ select name, strftime('%m-%d-%Y', due_by), description, url, id from work
                where class_id = ?
                order by due_by;""",
        [class_id]
    )
    print(data)
    return render_template('navigation/classes.html', data=data)


@app.route('/admin-token', methods=['GET', 'POST'])
def admintoken():
    if request.method == 'POST':
        session['admin'] = request.form.get('token-input')
        print(session['admin'])
        return redirect('/admin')
    return render_template('admin/admin-token.html')

if __name__ == '__main__':
    app.run('0.0.0.0')
