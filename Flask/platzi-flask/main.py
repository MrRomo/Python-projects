from flask import Flask, request, make_response, redirect, render_template

app = Flask (__name__)

todos = ['todo 1', 'todo 2', 'todo 3']

@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    response.set_cookie('user_ip', user_ip)
    return response

@app.route('/hello')
def hello():
    user_ip = request.cookies.get('user_ip')
    context = {
        'user_ip':user_ip,
        'todos': todos
    }
    return render_template('hello.html', **context )

@app.errorhandler(404)
def error404(error):
    return render_template('404.html',error=error)

@app.errorhandler(500)
def erro500(error):
    return render_template('404.html',error=error)