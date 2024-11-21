from flask import Blueprint, jsonify, request

main = Blueprint('content', __name__)

@main.route('/upload', methods=['POST'])
def upload():
    data = request.files['file']
    return jsonify({"message": f"File {data.filename} uploaded successfully!"})
