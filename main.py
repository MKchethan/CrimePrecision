from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.json_util import dumps
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configure MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['Crime_Precision']
users_collection = db['User_Data']


@app.route('/')
def home():
    return "Crime Precision"


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    print(36, email, password)

    login_successful = list(users_collection.find({'$and': [{'mail': email}, {'password': password}]}))

    if email == "" or password == "":
        response = {"message": "Please enter the valid email address and password"}
        return jsonify(response), 401
    elif login_successful:
        response = {'message': 'Login successful'}
        return jsonify(response), 200
    else:
        response = {'message': 'Invalid credentials'}
        return jsonify(response), 401


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    college_name = data.get('college_name')
    password = data.get('password')

    existing_user = users_collection.find_one({'email': email})

    if name == "" or email == "" or phone_number == "" or college_name == "" or password == "":
        response = {"message": "Please enter the valid field values"}
        return response, 401
    if existing_user:
        response = {'message': 'Email already exists. Try a different email.'}
        return jsonify(response), 400
    else:
        # hashed_password = generate_password_hash(password, method='sha256')
        new_user = {
            'name': name,
            'email': email,
            'phone_number': phone_number,
            'college_name': college_name,
            'password': password
        }

        users_collection.insert_one(new_user)
        response = {'message': 'Account created successfully'}
        return jsonify(response), 201


if __name__ == '__main__':
    app.run(debug=True)
