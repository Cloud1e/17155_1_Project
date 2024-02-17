from flask import Flask, redirect, url_for, request
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/admin')
def hello_admin():
    return 'Hello Admin'

@app.route('/user')
def hello_user():
    name = request.args.get('name')
    return 'Hello %s' % name

@app.route('/success/<name>')
def success(name):
    if name == 'admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_user', name = name))

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name = user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name = user))

@app.route('/projects/<project>')
def project_detail(project):
    return 'Project: %s' % project
    
if __name__ == "__main__":
    app.run(debug=True)