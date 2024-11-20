from flask import Blueprint, jsonify, request

content_bp = Blueprint('content', __name__)

@content_bp.route('/upload', methods=['POST'])
def upload():
    data = request.files['file']
    return jsonify({"message": f"File {data.filename} uploaded successfully!"})
