from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid

uploads = Blueprint("uploads", __name__)

@uploads.route("/upload-image", methods=["POST"])
def upload_image():

    file = request.files.get("image")

    if not file:
        return jsonify({"error": "No file provided"}), 400

    filename = secure_filename(file.filename)

    unique_name = f"{uuid.uuid4()}_{filename}"

    upload_folder = os.path.join(os.getcwd(), "uploads")

    os.makedirs(upload_folder, exist_ok=True)

    file.save(os.path.join(upload_folder, unique_name))

    return jsonify({
        "image_url": f"http://127.0.0.1:5000/uploads/{unique_name}"
    })


@uploads.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory("uploads", filename)