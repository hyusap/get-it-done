from flask import Flask, render_template
import sql

app = Flask(__name__)
db = sql.database('main.db')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
