# this import still confuses me
from app import app
from flask import render_template, request, redirect, jsonify, make_response
from datetime import datetime

@app.route("/")
def index():
    return render_template("public/index.html")

@app.route("/about")
def about():
    return render_template("public/about.html")

@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        req_dict = request.form
        # grabs all POST request data as dict
        # The keys will be the `name` attrs of each input element

        print(req_dict)
        # Note: in this case request.url is just the signup page.
        return redirect(request.url)

    return render_template("public/sign_up.html")

@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%d %b %Y")

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

# Mock data
users_dict = {
    "bjornthefellhanded": {
        "name": "Bjorn the Fell-handed",
        "bio": "Venerable Dreadnought of the Space Wolves", 
        "twitter_handle": "@in_the_emporers_name"
    },
    "robouteguilliman": {
        "name": "Roboute Guilliman",
        "bio": "Primarch of the Ultramarines",
        "twitter_handle": "@rowboat_girlyman"
    },
    "abaddon": {
        "name": "Ezekyle Abaddon",
        "bio": "Warmaster of Chaos", 
        "twitter_handle": "@failbaddon"
    }
}

# Dynamic urls for users
@app.route("/profile/<username>")
def profile(username):

    # init a None object so that Jinja-level 
    # validation will catch an unfound user later
    user = None
    if username in users_dict:
        user = users_dict[username] # user is a dict

    return render_template("public/profile.html", username=username, user=user)

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

# Async requests