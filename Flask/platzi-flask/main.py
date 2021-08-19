from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
import unittest

app = Flask (__name__)
boostrap = Bootstrap(app)
    

todos = ['todo 1', 'todo 2', 'todo 3']
app.config['SECRET_KEY'] = 'secreto'

class LoginForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')

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

@app.route('/hello', methods=['get', 'post'])
def hello():
    user_ip = session.get('user_ip')
    login_form = LoginForm()
    username = session.get('username')
    context = {
        'user_ip':user_ip,
        'todos': todos,
        'login_form': login_form,
        'username': username
    }
    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username
        flash('Nombre de usuario registrao con exito')
        return redirect(url_for('index'))

    return render_template('hello.html', **context )

@app.errorhandler(404)
def error404(error):
    return render_template('404.html',error=error)

@app.errorhandler(500)
def erro500(error):
    return render_template('404.html',error=error)


