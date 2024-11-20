from flask import Blueprint, jsonify, request

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['GET'])
def register():
    #data = request.json
    #return jsonify({"message": f"User {data['username']} registered successfully!"})
    return jsonify("User registered successfully!")

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    return jsonify({"message": "Login successful!"})
