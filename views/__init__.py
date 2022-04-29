from flask import render_template, request, redirect, url_for, session
from app import app
from model import *
import datetime



@app.route('/', methods=["GET"])
def home():
    if "username" in session:
        return render_template('index.html')
    else:
        return render_template('login.html')

# Register new user
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        registerUser()
        return redirect(url_for("login"))

#Check if email already exists in the registratiion page
@app.route('/checkusername', methods=["POST"])
def check():
    return checkusername()

# Everything Login (Routes to renderpage, check if username exist and also verifypassword through Jquery AJAX request)
@app.route('/login', methods=["GET"])
def login():
    if request.method == "GET":
        if "username" not in session:
            return render_template("login.html")
        else:
            return redirect(url_for("home"))


@app.route('/checkloginusername', methods=["POST"])
def checkUserlogin():
    return checkloginusername()

@app.route('/checkloginpassword', methods=["POST"])
def checkUserpassword():
    return checkloginpassword()

#The admin logout
@app.route('/logout', methods=["GET"])  # URL for logout
def logout():  # logout function
    session.pop('username', None)  # remove user session
    return redirect(url_for("home"))  # redirect to home page with message

#Forgot Password
@app.route('/forgot-password', methods=["GET"])
def forgotpassword():
    return render_template('forgot-password.html')

#404 Page
@app.route('/404', methods=["GET"])
def errorpage():
    return render_template("404.html")

#Blank Page
@app.route('/blank', methods=["GET"])
def blank():
    return render_template('blank.html')

#Buttons Page
@app.route('/buttons', methods=["GET"])
def buttons():
    return render_template("buttons.html")

#Cards Page
@app.route('/cards', methods=["GET"])
def cards():
    return render_template('cards.html')

#Charts Page
@app.route('/charts', methods=["GET"])
def charts():
    return render_template("charts.html")

#Devices Page
@app.route('/devices', methods=["GET"])
def devices():
    if "username" in session:
            # specify the collections name
        devices = db.devices
        datetimenow = datetime.datetime.now()
        # convert the mongodb object to a list
        data = list(devices.find())

        return render_template("devices.html", device_info=data, timenow = datetimenow)
    else:
        return render_template('login.html')


#Maps Page
@app.route('/maps', methods=["GET"])
def maps():
    if "username" in session:
        devices = db.devices
        # convert the mongodb object to a list
        data = list(devices.find({},{"_id": 0, "Owner": 0, "Installation Location":0}))

        return render_template("maps.html", device_data=data)
    else:
        return render_template('login.html')
    # specify the collections name
 


#Tables Page
@app.route('/tables', methods=["GET"])
def tables():
    if "username" in session:
          # specify the collections name
        reports = db.readings
        # convert the mongodb object to a list
        data = list(reports.find())
        return render_template("tables.html",reports_info=data)
    else:
        return render_template('login.html')


#Utilities-animation
@app.route('/utilities-animation', methods=["GET"])
def utilitiesanimation():
    return render_template("utilities-animation.html")

#Utilities-border
@app.route('/utilities-border', methods=["GET"])
def utilitiesborder():
    return render_template("utilities-border.html")

#Utilities-color
@app.route('/utilities-color', methods=["GET"])
def utilitiescolor():
    return render_template("utilities-color.html")

#utilities-other
@app.route('/utilities-other', methods=["GET"])
def utilitiesother():
    return render_template("utilities-other.html")


@app.route('/user/<username>')

def user(username):
#    user = User.query.filter_by(username=username).first_or_404()
    users = db.users
    user = users.find_one({"username": username})
    
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)