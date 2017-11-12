"""
This is a WIP and a learning experience.
Flask Documentation: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
"""

print("BEGIN")

# TODO: Add security. Some password/token passed along with ALL requests. (mandate HTTPS!!!)
# NOTE: Server permissions should (SHALL) be set to mitigate issues/keep shenanigans low.
# TODO: View page. Show all uploads, require password/token.

import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '/var/www/html/dingle/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/up", methods=["POST"])
def up():
    if request.method == "POST":  # Check not neccessarily needed. Later feature? DELETE?
        if 'file' not in request.files:
            return "Bad request. no file", 400  # 400 -> Bad Request.
        sent_file = request.files["file"]
        # Should be a non issue for my purpose --- but mind as well handle something weird.
        if sent_file.filename == '':
            return "Bad request.", 400  # 400 -> Bad Request.
        if sent_file and allowed_file(sent_file.filename):
            file_name = secure_filename(sent_file.filename)
            sent_file.save(os.path.join(
                app.config["UPLOAD_FOLDER"], file_name))
            return redirect(url_for("upped", file_name=file_name))


@app.route("/up/upped/<file_name>")
def upped(file_name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], file_name)


# MISC / RANDOM stuff.


@app.route("/echoer", methods=["POST", "GET"])
def index():
    return """<form action="/echo" method="GET"><input name="text"><input type="submit" value="Echo"></form>"""


@app.route("/echoer/echo", methods=["POST"])
def echo():
    return "You said: " + request.form['text'] + "\n" + str(request.form) + "\n"


@app.route("/greet/")
@app.route("/greet/<user>")
def greet(user=None):
    return render_template("home.html", method=request.method, user=user)


# vars from address specified with < >
@app.route("/user/<name>")
def user(name):
    return "Howdy, {}".format(name)


# For int in URL var specify int data type
@app.route("/post/<int:post_id>")
def post(post_id):
    return "Howdy, {}".format(post_id)


if __name__ == "__main__":
    app.run()
    # app.run(debug=True)
