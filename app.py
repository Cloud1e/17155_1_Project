from flask import Flask, redirect, url_for, jsonify, request, send_from_directory
from pymongo import MongoClient
from flask_cors import CORS
from service import cipher

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

# users
@app.route('/user')
def hello_user():
    name = request.args.get('name')
    return 'Hello %s' % name

@app.route("/user/create", methods=["POST"])
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
    return jsonify({'message': "User " + json["username"] + " Created!"}), 201  


@app.route("/user/login", methods=["POST"])
def login():
    json = request.get_json()
    print(json)
    username = json['username']
    password = json['password']
    encrypted_pass = cipher.encrypt(password, 1)
    user_found = users.find_one({"username": username})
    if user_found is not None:
        if encrypted_pass == user_found["password"]:
            message = 'Login success!'
            return jsonify({'message': message}), 200  
        else:
            message = 'Incorrect password!'
            return jsonify({'message': message}), 400  
    else:
        message = 'User does not exist!'
        return jsonify({'message': message}), 400  

@app.route('/success/<name>')
def success(name):
    if name == 'admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_user', name = name))

# @app.route('/login', methods = ['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         user = request.form['nm']
#         return redirect(url_for('success', name = user))
#     else:
#         user = request.args.get('nm')
#         return redirect(url_for('success', name = user))

@app.route('/projects/<project>')
def project_detail(project):
    return 'Project: %s' % project
    
if __name__ == "__main__":
    app.run(debug=True)