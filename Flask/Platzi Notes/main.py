from flask import request, make_response, redirect, render_template, session, url_for, flash
from flask_login import login_required, current_user
from flask_bootstrap import Bootstrap
import unittest
from app import create_app
from app.forms import DeleteTodoForm, LoginForm, TodoForm, UpdateTodoForm
from app.firestore_service import delete_todo, get_users, get_todos, put_todo, get_user, update_todo

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


@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id
    user = get_user(username)
    todo_form = TodoForm()
    delete_todo_form = DeleteTodoForm()
    update_todo_form = UpdateTodoForm()
    context = {
        'user_ip': user_ip,
        'todos': get_todos(user.id),
        'username': username,
        'todo_form': todo_form,
        'delete_todo_form': delete_todo_form,
        'update_todo_form': update_todo_form
    }
    print(context)
    if todo_form.validate_on_submit():
        put_todo(user_id=username, descripcion=todo_form.descripcion.data)

        flash('Tu tarea se creo con éxito!')

        return redirect(url_for('hello'))

    return render_template('hello.html', **context)


@app.route('/todos/delete/<todo_id>', methods=['post'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id=user_id, todo_id=todo_id)

    return redirect(url_for('hello'))

@app.route('/todos/update/<todo_id>/<int:done>', methods=['post'])
def update(todo_id, done):
    user_id = current_user.id
    update_todo(user_id=user_id, todo_id=todo_id, done=done)

    return redirect(url_for('hello'))


@app.errorhandler(404)
def error404(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def erro500(error):
    return render_template('404.html', error=error)
