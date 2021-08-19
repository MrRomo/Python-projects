from flask import request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
import unittest
from app import create_app
from app.forms import LoginForm
from app.firestore_service import get_users

app = create_app()

todos = ['todo 1', 'todo 2', 'todo 3']

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip
    return response

@app.route('/hello')
def hello():
    user_ip = session.get('user_ip')
    username = session.get('username')
    context = {
        'user_ip':user_ip,
        'todos': todos,
        'username': username
    }
    users = get_users()
    for user in users:
        print(user)

    return render_template('hello.html', **context )

@app.errorhandler(404)
def error404(error):
    return render_template('404.html',error=error)

@app.errorhandler(500)
def erro500(error):
    return render_template('404.html',error=error)


