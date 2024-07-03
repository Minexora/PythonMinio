import logging
from flask_cors import CORS
from minio_class import MinIOClass
from shortner_class import URLShortener
from flask import Flask, redirect, request, jsonify

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
CORS(app)
shortener = URLShortener()
minio_cls = MinIOClass()


@app.route("/shorten", methods=["POST"])
def shorten():
    print("shorten")
    original_url = request.json.get("url")
    if not original_url:
        return jsonify({"error": "URL is required"}), 400
    short_url = shortener.shorten_url(original_url)
    return jsonify({"short_url": request.host_url + short_url})


@app.route("/<short_url>", methods=["POST", "GET"])
def redirect_to_original(short_url):
    original_url = shortener.get_original_url(short_url)
    if not original_url:
        return jsonify({"error": "URL not found"}), 404
    return redirect(original_url)


@app.route("/upload-file", methods=["POST"])
def upload_file():
    change_file = request.form.get("change_file")
    file_share = request.form.get("file_share")
    res = []
    for _, file in request.files.items():
        file_name = file.filename
        mime_type = file.mimetype
        file_data = file.read()

        is_ok, file_res = minio_cls.upload_file(object_name=file_name, data=file_data, file_share=file_share, content_type=mime_type, change_file=change_file)
        if is_ok:
            if file_share:
                res.append({"file_name": file_name, "url": file_res})
            else:
                res.append({"file_name": file_name, "status": "Uploaded"})
            return jsonify({"response": res}), 200
        else:
            return jsonify({"error": file_res}), 400


@app.route("/get-file-list", methods=["GET"])
def get_file_list():
    return jsonify({"response": minio_cls.file_detail_list}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5050, host="0.0.0.0")
