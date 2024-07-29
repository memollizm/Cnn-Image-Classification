from flask import Flask, render_template, request, redirect,url_for
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)
model = load_model("model/cnn_model.keras")


UPLOAD_FOLDER = "static/uploads/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = {"png","jpg","jpeg","gif"}


def allowed_file(filename):
    return '.' in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS


def predict_image(img_path):
    img = image.load_img(img_path, target_size=(62,62))
    img = image.img_to_array(img)
    img = np.expand_dims(img,axis=0)
    img = img / 255.0
    prediction = model.predict(img)
    return 'Dog' if prediction[0][0] > 0.5 else 'Cat'



@app.route("/", methods = ["GET","POST"])
def upload_file():
    if request.method == "POST":
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        
        if file.filename == '':
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            prediction = predict_image(filepath)
            return render_template("index.html", filename = filename, prediction=prediction)
    return render_template("index.html")


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return redirect(url_for("static", filename = "uploads/" + filename))


if __name__ == "__main__":
    app.run(debug=True)