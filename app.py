from flask import Flask, render_template, session, url_for, request, redirect
from flask import render_template
import db

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "tom_waits_is_grits"
global currentTour
currentTour = "None"

@app.route("/")
def index():
    user = "Login"
    if "user" in session:
        user = session["user"]
        return redirect(url_for("home"))
    return render_template('index.html', title="Scavenger Tours", user=user)

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("index"))
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if db.verify(username, password):
            session["user"] = username
            return redirect(url_for("index"))
    return render_template("signin.html", title="Login")

@app.route("/logout")
def logout():
    session.pop("user")
    return redirect(url_for("index"))

@app.route("/getUser")
def getUser():
    if "user" in session:
        return session["user"]
    else:
        return ""

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST" and request.form["username"] and request.form["password"]:
        db.addUser(request.form["username"], request.form["password"])
        return redirect(url_for("login"))
    return render_template("signup.html", title="Register")

@app.route("/home")
def home():
    global currentTour
    points = db.getUser(session["user"])[0][3]
    return render_template('homepage.html', title="Welcome", currentTour = currentTour, user = getUser(), points = points)

@app.route("/tours")
def tours():
    cities = db.getCityList()
    return render_template('tours.html', title="Choose a City", cities=cities)

@app.route("/error")
def error():
    return render_template('error.html')

@app.route("/<city>")
def city(city):
    tours = db.getTourList(city)
    images = []
    for tour in tours:
        img = db.getTour(tour)[0][8]
        images.append(img)
    return render_template('city.html', city = city, tours = tours, images = images)

@app.route("/<city>/<tour>", methods=["GET","POST"])
def touroverview(city, tour):
    global currentTour
    description = db.getTour(tour)[0][1]
    image = db.getTour(tour)[0][8]
    if request.method == "POST":
        db.addCurrentTourtoUser(getUser(),tour)
        currentTour = tour
        return redirect(url_for("home"))
    return render_template('touroverview.html', city=city, tour=tour, description = description, image = image)

@app.route("/google")
def google():
    return render_template('google.html')

@app.route("/map")
def map():
    return render_template('map.html')

@app.route("/create")
def create():
    return render_template('create.html')

if __name__ == "__main__":
    app.debug=True
    app.run()
