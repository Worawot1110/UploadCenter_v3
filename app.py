from flask import Flask, render_template, request, jsonify

from config import HOST, PORT, MAX_UPLOAD_SIZE
from uploader import Uploader
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_SIZE

uploader = Uploader()

ALLOWED_EXTENSIONS = {
    "jpg", "jpeg", "png", "gif", "webp",
    "pdf",
    "doc", "docx",
    "xls", "xlsx",
    "ppt", "pptx",
    "zip", "rar", "7z",
    "mp4", "mov", "avi", "mkv"
}

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

def generate_filename(filename):

    filename = secure_filename(filename)

    ext = filename.rsplit(".", 1)[1].lower()

    name = filename.rsplit(".", 1)[0]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    uid = uuid.uuid4().hex[:8]

    return f"{timestamp}_{uid}_{name}.{ext}"

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "file" not in request.files:
        return jsonify({
            "success": False,
            "message": "No file."
        }), 400

    files = request.files.getlist("file")

    results = []

    for file in files:

        if not allowed_file(file.filename):

            results.append({
                "success": False,
                "filename": file.filename,
                "message": "ไม่อนุญาตให้อัปโหลดไฟล์ประเภทนี้"
            })

            continue

        stored_name = generate_filename(file.filename)

        results.append(
            uploader.upload(
                file,
                stored_name
            )
        )

    return jsonify(results)

@app.errorhandler(RequestEntityTooLarge)
def file_too_large(e):
    return jsonify({
        "success": False,
        "message": f"ไฟล์มีขนาดเกิน {MAX_UPLOAD_SIZE // (1500 * 1500)} MB"
    }), 413

if __name__ == "__main__":
    app.run(
        host=HOST,
        port=PORT,
        debug=True
    )