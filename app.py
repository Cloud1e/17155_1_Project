from flask import Flask, redirect, url_for, request, send_from_directory
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__, static_folder='./build', static_url_path='/')
CORS(app)
client = MongoClient("mongodb+srv://vivektallav:vivMongo24@17155-1project.tu4ysq1.mongodb.net/")
db = client['myDatabase']

# create collection
users = db["user"]
projects = db["project"]
hwsets = db["hardware"]

def get_database():
    # Retrieve a collection named "usernames from database
    documents = users.find({})
    return str(list(documents))

@app.route('/', methods=['GET'])
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/database')
def home():
    return 'Connected to MongoDB!<br/>Document Info: ' + get_database()

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