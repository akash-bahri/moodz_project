from flask import Blueprint, jsonify, request

main = Blueprint('user', __name__)

@main.route('/register', methods=['GET'])
def register():
    #data = request.json
    #return jsonify({"message": f"User {data['username']} registered successfully!"})
    return jsonify("User registered successfully!")

@main.route('/login', methods=['POST'])
def login():
    #data = request.json
    return jsonify({"message": "Login successful!"})
