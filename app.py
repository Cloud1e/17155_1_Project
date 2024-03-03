from flask import Flask, redirect, url_for, jsonify, request, send_from_directory, session
from pymongo import MongoClient
from flask_cors import CORS
from service import cipher
import secrets
import os.path

app = Flask(__name__, static_folder='./build', static_url_path='/')
CORS(app)
client = MongoClient("mongodb+srv://vivektallav:sflab17@17155-1project.tu4ysq1.mongodb.net/")
db = client['myDatabase']

# Details on the Secret Key: https://flask.palletsprojects.com/en/2.3.x/config/#SECRET_KEY
# NOTE: The secret key is used to cryptographically-sign the cookies used for storing
#       the session data.
# NOTE: app_secret_key.txt should have one line, which is the secret key.
#       app_secret_key.txt has been added to .gitignore.
if not os.path.exists('app_secret_key.txt'):
    f = open('app_secret_key.txt', 'w')
    f.write(secrets.token_hex())
    f.close()
f = open("app_secret_key.txt", "r")
app.secret_key = f.read()
f.close()

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


@app.route('/admin')
def hello_admin():
    return '<h1>Hello Admin</h1>Connected to MongoDB!<br/>Document Info: ' + get_database()

# User home
@app.route('/home')
def hello_user():
    name = session['username']
    return 'Hello %s' % name

@app.route("/createUser", methods=["GET", "POST"])
def createUser():
    json = request.get_json()
    message = ""
    user_found = users.find_one({"username": json["username"]})
    if json["username"] == 'admin' or user_found:
        message = 'User already exists!'
        return jsonify({'message': message}), 400  
    if json["password"].count(' ') > 0 or json["password"].count('!') > 0:
        message = 'Invalid password!'
        return jsonify({'message': message}), 400
    encrypted_pass = cipher.encrypt(json["password"], 1)
    user = {
        "password": encrypted_pass,
        "username": json["username"]
    }
    users.insert_one(user)
    session['username'] = json["username"]
    session['encrypted_pass'] = encrypted_pass
    return jsonify({'message': "User " + json["username"] + " Created!"}), 201  

@app.route("/login/", methods=["GET", "POST"])
def login():
    print('post request working')
    json = request.get_json()
    print(json)
    username = json['username']
    password = json['password']
    encrypted_pass = cipher.encrypt(password, 1)
    session['username'] = username
    session['encrypted_pass'] = encrypted_pass
    return '1'

@app.route("/loginTry/", methods=["GET"])
def loginTry():
    print('get request working')
    username = session['username']
    encrypted_pass = session['encrypted_pass']
    user_found = users.find_one({"username": username})
    if user_found is not None:
        if encrypted_pass == user_found["password"]:
            del session['encrypted_pass']
            session['login_success'] = True
            message = 'Login success!'
            # return jsonify({'message': message}), 200
            return success()
        else:
            del session['username']
            del session['encrypted_pass']
            message = 'Incorrect password!'
            return jsonify({'message': message}), 400  
    else:
        del session['username']
        del session['encrypted_pass']
        message = 'User does not exist!'
        return jsonify({'message': message}), 400  

def success():
    name = session['username']
    if name == 'admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_user'))

# @app.route('/login', methods = ['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         user = request.form['nm']
#         return redirect(url_for('success', name = user))
#     else:
#         user = request.args.get('nm')
#         return redirect(url_for('success', name = user))

@app.route('/project_<project>')
def project_detail(project):
    return 'Project: %s' % project
    
if __name__ == "__main__":
    app.run(debug=True)