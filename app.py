from flask import Flask, redirect, url_for, jsonify, request, send_from_directory, session
from pymongo import MongoClient
from flask_cors import CORS
from service import cipher
from classes.hardwareSet import hardwareSet
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
@app.route('/home/', methods=['GET'])
def hello_user():
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/createUser/", methods=["POST"])
def createUser():
    json = request.get_json()
    username = json['username']
    password = json['password']
    encrypted_pass = cipher.encrypt(password, 1)
    session['username'] = username
    session['encrypted_pass'] = encrypted_pass
    return '1'

@app.route("/createUserTry/", methods=["GET"])
def createUserTry():
    username = session['username']
    encrypted_pass = session['encrypted_pass']
    user_found = users.find_one({"username": username})
    
    if username == 'admin' or user_found:
        del session['username']
        del session['encrypted_pass']
        message = 'User already exists!'
        return jsonify({'message': message}), 400  
    if encrypted_pass.count(' ') > 0 or encrypted_pass.count('!') > 0:
        del session['username']
        del session['encrypted_pass']
        message = 'Invalid password!'
        return jsonify({'message': message}), 400
    
    user = {
        "password": encrypted_pass,
        "username": username
    }
    users.insert_one(user)
    # return jsonify({'message': "User " + username + " Created!"}), 201
    return enter_success()

@app.route("/login/", methods=["POST"])
def login():
    json = request.get_json()
    username = json['username']
    password = json['password']
    encrypted_pass = cipher.encrypt(password, 1)
    session['username'] = username
    session['encrypted_pass'] = encrypted_pass
    return '1'

@app.route("/loginTry/", methods=["GET"])
def loginTry():
    username = session['username']
    encrypted_pass = session['encrypted_pass']
    user_found = users.find_one({"username": username})
    if user_found is not None:
        if encrypted_pass == user_found["password"]:
            del session['encrypted_pass']
            session['login_success'] = True
            message = 'Login success!'
            # return jsonify({'message': message}), 200
            return enter_success()
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

def enter_success():
    username = session['username']
    if username == 'admin':
        return redirect(url_for('hello_admin'))
    else:
        user_found = users.find_one({"username": username})
        session['_id'] = str(user_found['_id'])
        message = 'Success! Enter account: ' + session['_id'] + ' with username: ' + username
        return jsonify({'message': message}), 200

@app.route('/project_<project>')
def project_detail(project):
    return 'Project: %s' % project

@app.route("/project/create", methods=["POST"])
def createProject():
    json = request.get_json()
    projectid = json["projectid"]
    project_found = projects.find_one({"projectid": projectid})
    if project_found is None:
        authusers = [i for i in json["authusers"]]
        project = {
            "projectname": json["projectname"],
            "projectid": json["projectid"],
            "description": json["description"],
            "authusers": authusers
        }
        projects.insert_one(project)
        message = "Project " + json["projectname"] + " Added With ID: " + json["projectid"] + "!"
        return jsonify({'message': message}), 201
    else:
        message = "Project ID already exists"
        return jsonify({'message': message}), 400

# Determine whether the user has the permission to access the project
@app.route("/project/get", methods=["POST"])
def getProject():
    json = request.get_json()
    project_found = projects.find_one({"projectid": json["projectid"]})
    if project_found:
        if json["username"] in project_found["authusers"]:
            message =  "Project Accessed!"
            return jsonify({'message': message}), 201
        else:
            message =  "Access Denied!"
            return jsonify({'message': message}), 400
    else:
        message =  "Project Does Not Exist!"
        return jsonify({'message': message}), 400

@app.route("/project/getByID", methods=["POST"])
def getProjectByID():
    json = request.get_json()
    project_found = projects.find_one({"projectid": json["projectid"]})
    if project_found is None:
        return jsonify({'message': "Project Does Not Exist!"}), 400
    else:
        data = {
            "projectname": project_found["projectname"],
            "projectid": project_found["projectid"],
            "description": project_found["description"],
            "authusers": project_found["authusers"],
        }
        return jsonify(data), 201

@app.route("/project/addUser", methods=["POST", "GET"])
def joinProject():
    json = request.get_json()
    projectId = json["projectid"]
    userName = json["username"]
    project_found = projects.find_one({"projectid": projectId})
    if project_found:
        #if user hasn't been added already
        if userName not in project_found["authusers"]:
            authusers = [i for i in project_found["authusers"]]
            authusers.append(userName)
            result = projects.update_one({"projectid": projectId}, 
                                         {"$set": {"authusers": authusers}})
            message = "Successfully added " + userName + " to " + projectId + "!"
            return jsonify({'message': message}), 201
        else:
            message = userName + " is already an authorized user!"
            return jsonify({'message': message}), 400
    else:
        message = "Project Does Not Exist!"
        return jsonify({'message': message}), 400

@app.route("/project/removeUser", methods=["POST", "GET"])
def leaveProject():
    json = request.get_json()
    projectId = json["projectid"]
    userName = json["username"]
    project_found = projects.find_one({"projectid": projectId})
    if project_found:
        # if user hasn't been added already, else has been added
        if userName not in project_found["authusers"]:
            message = userName + " is not an authorized user!"
            return jsonify({'message': message}), 400
        else:
            authusers = [i for i in project_found["authusers"]]
            authusers.remove(userName)
            result = projects.update_one({"projectid": projectId}, 
                                         {"$set": {"authusers": authusers}})
            message = "Successfully removed " + userName + " from " + projectId + "!"
            return jsonify({'message': message}), 201
    else:
        message = "Project Does Not Exist!"
        return jsonify({'message': message}), 400

# hwsets
@app.route("/hwsets/getAvailability", methods=["POST"])
def getHwAvailability():
    json = request.get_json()
    name = json["hardwarename"]
    hw_found = hwsets.find_one({"hardwarename": name})
    if hw_found is not None:
        availability = hw_found["availability"]
        return str(availability)
    else:
        availability = -1
        return str(availability)

@app.route("/hwsets/getCapacity", methods=["POST"])
def getHwCapacity():
    json = request.get_json()
    name = json["hardwarename"]
    hw_found = hwsets.find_one({"hardwarename": name})
    if hw_found is not None:
        capacity = hw_found["capacity"]
        return str(capacity)
    else:
        capacity = -1
        return str(capacity)

@app.route("/hwsets/checkOut", methods=["POST"])
def checkOut():
    json = request.get_json()
    name = json["hardwarename"]
    hw_found = hwsets.find_one({"hardwarename": name})
    if hw_found:
        capacity = hw_found["capacity"]
        availability = hw_found["availability"]
        hw = hardwareSet(capacity, availability)
        num = int(json["quantity"])
        hw.check_out(num)
        availability = hw.get_availability()
        query = {"hardwarename":name}
        newvalues = {"$set": {"availability": availability}}
        hwsets.update_one(query, newvalues)
        return str(availability)
    else:
        availability = -1
        return str(availability)

@app.route("/hwsets/checkIn", methods=["POST"])
def checkIn():
    json = request.get_json()
    name = json["hardwarename"]
    hw_found = hwsets.find_one({"hardwarename": name})
    if hw_found:
        capacity = hw_found["capacity"]
        availability = hw_found["availability"]
        hw = hardwareSet(capacity, availability)
        num = int(json["quantity"])
        hw.check_in(num)
        availability = hw.get_availability()
        query = {"hardwarename": name}
        newvalues = {"$set": {"availability": availability}}
        hwsets.update_one(query, newvalues)
        return str(availability)
    else:
        availability = -1
        return str(availability)

if __name__ == "__main__":
    app.run(debug=True)