from flask import Flask, redirect, url_for, request
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/login')
def login():
    return 'Login Page'

@app.route('/admin')
def hello_admin():
    return 'Hello Admin'

@app.route('/user')
def hello_user():
    name = request.args.get('name')
    return 'Hello %s' % name

@app.route('/login_success/<name>')
def hello(name):
    if name == 'admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_user', name = name))

@app.route('/projects/<project>')
def project_detail(project):
    return 'Project: %s' % project
    
if __name__ == "__main__":
    app.run(debug=True)