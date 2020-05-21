# this import still confuses me
from app import app
from flask import render_template, request, redirect, jsonify, make_response, send_from_directory, abort, url_for, flash
from flask_wtf import FlaskForm # flask_wtf is a thin wrapper over WTforms
from wtforms import StringField, PasswordField
from datetime import datetime
import os

from werkzeug.utils import secure_filename

# Mock data
# Note that the users_dict keys must be equal to the "username" attrib for this to work
users_dict = {
    "Squishy Baby":{
        "username": "Squishy Baby",
        "bio": "The squishiest baby",
        "twitter_handle": "@squish_squish",
        "password": "password1234"
    },
    "Bjorn the Fell-handed": {
        "username": "Bjorn the Fell-handed",
        "bio": "Venerable Dreadnought of the Space Wolves", 
        "twitter_handle": "@in_the_emporers_name",
        "password":"password1234"
    },
    "Roboute Guilliman": {
        "username": "Roboute Guilliman",
        "bio": "Primarch of the Ultramarines",
        "twitter_handle": "@rowboat_girlyman",
        "password":"password1234"
    },
    "Ezekyle Abaddon": {
        "username": "Ezekyle Abaddon",
        "bio": "Warmaster of Chaos", 
        "twitter_handle": "@failbaddon",
        "password":"password1234"
    }
}

@app.route("/")
def index():
    print(app.config["DB_NAME"])

    return render_template("public/index.html")

@app.route("/about")
def about():
    return render_template("public/about.html")

# Sign-up web page to demo forms
# This version is vanilla and NOT secure
# commented out in favour of another sign_up route below
"""
@app.route("/sign-up-deprecated", methods=["GET", "POST"])
def sign_up_deprecated():
    if request.method == "POST":
        req_dict = request.form
        # grabs all POST request data as dict
        # The keys will be the `name` attrs of each input element

        print(req_dict)
        # Note: in this case request.url is just the signup page.
        return redirect(request.url)

    return render_template("public/sign_up.html")
"""

# ==================== SECURE FORMS WITH WTFORMS ====================
# Secure forms using flask-WTF. Grabbed from PrettyPrinted YT Channel
# see also: http://wtforms.simplecodes.com/docs/0.6/fields.html#basic-fields
# Needs a secret key:
app.config["SECRET_KEY"] = "Thisisasecretkey!"

class LoginForm(FlaskForm):
    username = StringField("username")
    password = PasswordField("password")

@app.route("/secure_form", methods=["GET", "POST"])
def secure_form():
    form = LoginForm() # instantiate FlaskForm instance

    # Grab POSTed values on submit:
    if form.validate_on_submit():
        print(f"username = {form.username.data}, password is {form.password.data}")
        return redirect(request.url)

    # the form=form flag then passes `form` to secure_form.html
    return render_template("public/secure_form.html", form=form)


@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%d %b %Y")

# ============================== JINJA ==============================
@app.route("/jinja")
def jinja():
 
    my_name = "Julian"
    langs = ["Python", "R", "JS", "Ruby"]
    friends_dict = {
        "Bjorn the Fell-Handed": 10000,
        "Abaddon": 10000,
        "Apollo Diomedes": 300
    }
    colours_tuple = ("red", "green")
    t0 = datetime.utcnow()
    my_html = "<h1>This could have been a script tag.</h1>"

    class GitRemote:
        def __init__(self, name, description, url):
            self.name = name
            self.description = description
            self.url = url

        def pull(self):
            return f"Pullin repo {self.name}"
        
        def clone(self):
            return f"Cloning into {self.url}"

    my_remote = GitRemote(name="flask_jinja", 
    description="template design tutorial", 
    url="https://github.com")

    def repeat(x, qty):
        return x * qty

    return render_template("public/jinja.html", 
    my_name=my_name, 
    langs=langs, 
    friends_dict=friends_dict, 
    colours_tuple=colours_tuple, 
    GitRemote=GitRemote, 
    my_remote=my_remote,
    repeat=repeat, 
    t0=t0,
    my_html=my_html)

# ============================== DYNAMIC URLS ==============================
# Dynamic urls for users
"""
@app.route("/profile/<username>")
def profile(username):

    # init a None object so that Jinja-level 
    # validation will catch an unfound user later
    user = None
    if username in users_dict:
        user = users_dict[username] # user is a dict

    return render_template("public/profile.html", username=username, user=user)
"""

# Another silly example of dynamic urls
@app.route("/multiple/<foo>/<bar>/<baz>")
def multi(foo, bar, baz):
    return f"foo is {foo}, bar is {bar}, baz is {baz}"

# GETing and POSTing JSON. Note that Flask routes allow GET by default.
@app.route("/json", methods=["POST"])
def json():

    if request.is_json:
        print("Yes, I see json")
        req = request.get_json()
        print(type(req)) #>>dictionary
        print(req)

        response = {
            "message": "JSON received", 
            "name": req.get("name")
        }

        # Make a json response
        res = make_response(jsonify(response), 200)
    else:
        res = make_response(jsonify({"message": "No JSON received!"}), 400)

    return res

# Async requests with Fetch API
# in a guestbook function
@app.route("/guestbook")
def geustbook():
    return render_template("public/guestbook.html")

@app.route("/guestbook/create-entry", methods=["POST"])
def create_entry():
    req = request.get_json()
    print(req)
    res = make_response(jsonify(req), 200)

    return res

# dynamic query strings example; not much to it
@app.route("/query")
def query():
    if request.args: 
        print(request.args)
    return "Query received", 200

# ============================== FILE UPLOADS ==============================
# This example will upload an image

# set a path to save images to
# use absolute path
# If a file of the same name already exists in dir, img.save will override silently. 
app.config["IMAGE_UPLOADS"] = "/Users/don/Documents/flask_jnash/app/static/img"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024

def allowed_image(filename):
    """File extension sanity check on filename. 
    Returns True if allowed, False otherwise.
    """
    if not "." in filename:
        return False
    ext = filename.rsplit(".")[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):
    """Filesize check."""
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        print(request)
        if request.files: # if there's a file
            if not allowed_image_filesize(request.cookies["filesize"]):
                print("File exceeded max size")
                return redirect(request.url)
            img = request.files["image"]

            # file input validation checks
            if img.filename == "":
                print("Image must have a filename!")
                return redirect(request.url)
            if not allowed_image(img.filename):
                print("That image extension is not allowed")
                return redirect(request.url)
            else: # sanitize filename in case it's malicious code
                filename = secure_filename(img.filename)
                img.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            print("Image saved!")
            return redirect(request.url)

    return render_template("public/upload_image.html")

# ============================== FILE DOWNLOADS ==============================
# Allocate a single dir at app/static/client for public access
# files available for download access will be kept only here
# do NOT use send_file(), because it's not secure

# app.config["CLIENT_FILES"] specified in config.py
@app.route("/get-image/<string:image_name>")
def get_image(image_name):
    try:
        return send_from_directory(
            app.config["CLIENT_FILES"], 
            filename=image_name, 
            as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route("/get-csv/<string:filename>")
def get_csv(filename):
    try:
        return send_from_directory(
            app.config["CLIENT_FILES"], 
            filename=filename, 
            as_attachment=True)
    except FileNotFoundError:
        abort(404)

# Demo using the path variable
# Not very user-friendly way of doing things, though
# folder structure is there, but not populated with files
@app.route("/get-report/<path:path>")
def get_report(path):
    try:
        return send_from_directory(
            app.config["CLIENT_REPORTS"], 
            filename=path, 
            as_attachment=True)
    except FileNotFoundError:
        abort(404)

# ============================== FLASK SESSIONS ==============================
# Sessions are sufficiently elaborate to require their own note: see note-sessions.md

# you'll need to set a session-specific secret key 
# to encode the session obj
app.config["SECRET_KEY"] = "9PYROHT5kaPCyHUC"

from flask import session
# Note that this sign-in has no relation to the "/sign-up" route
# Also note that this route is to demo sessions only, and has the security of damp tissue
@app.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        req = request.form
        print(req)

        username = req.get("username")
        password = req.get("password")

        if username not in users_dict:
            print("username not found!")
            return redirect(request.url)
        else:
            user = users_dict[username]

        if password != user["password"]:
            print("Invalid password")
            return redirect(request.url)
        else:
            # Now we start using a session
            # Store user's username in session
            session["USERNAME"] = user["username"]
            print("User added to session")
            return redirect(url_for("user_profile"))

    # see note on why session cookie values are not secure
    return render_template("public/sign_in.html")

@app.route("/profile")
def user_profile():
    """Distinct from the profile() method."""

    # If there's a USERNAME associated with the session dictionary
    if session.get("USERNAME", None) is not None:
        username = session.get("USERNAME")
        print(username)
        user = users_dict[username]
        return render_template("public/profile.html", user=user)
    else:
        print("Username not found in session")
        return redirect(url_for("sign_in"))

@app.route("/sign-out")
def sign_out():
    """If there is no session["USERNAME"], this redirects the /profile route to /sign-in"""
    session.pop("USERNAME")

    return redirect(url_for("sign_in"))

# ============================== MESSAGE FLASHING ==============================
# Message flashing, demonstrated within sign-up functionality
@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():

    print(type(request))
    if request.method == "POST":
        req = request.form

        username = req["username"]
        email = req["email"]
        password = req["password"] 

        if not len(password) >= 10:
            # Good idea to name your categories as a substring in bs4 classes
            flash("Password must be at least 10 characters long!", "warning")
            return redirect(request.url)

        print(username, email, password)
        flash("Account created!", "success")
        return redirect(request.url)

    return render_template("public/sign_up.html")

# ============================== ERROR HANDLING ==============================