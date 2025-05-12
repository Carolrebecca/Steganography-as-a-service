from flask import Flask, render_template, request, send_file
from stego import encode_message, decode_message
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form['action']
        if action == 'encode':
            image = request.files['image']
            message = request.form['message']
            image_path = "input.png"
            image.save(image_path)
            encode_message(image_path, message, "encoded.png")
            return send_file("encoded.png", as_attachment=True)
        elif action == 'decode':
            image = request.files['image']
            image_path = "encoded.png"
            image.save(image_path)
            message = decode_message(image_path)
            return f"<h1>Decoded Message:</h1><p>{message}</p>"
    return render_template('index.html')
