from flask import Flask, render_template, request, send_file, redirect, url_for
from stego import encode_message, decode_message
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    status = ""
    decoded_msg = ""

    try:
        if request.method == "POST":
            action = request.form.get("action")

            if action == "encode":
                image = request.files["image"]
                message = request.form["message"]
                image_path = "input.png"
                image.save(image_path)
                encode_message(image_path, message, "encoded.png")
                return send_file("encoded.png", as_attachment=True)

            elif action == "decode":
                image = request.files["image"]
                image_path = "encoded.png"
                image.save(image_path)
                decoded_msg = decode_message(image_path)
                status = "success"

        return render_template("index.html", status=status, message=decoded_msg)

    except Exception as e:
        print("Error:", e)
        return render_template("index.html", status="error")

if __name__ == "__main__":
    app.run(debug=True)
