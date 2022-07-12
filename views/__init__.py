from flask import Flask, render_template, request, redirect, url_for, session
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

from app import app
from model import *
import json
from datetime import date, datetime
import pytz

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
    if "username" in session:
          # specify the collections name
        reports = db.readings
        # convert the mongodb object to a list
        myquery = { "Unit":36 }
        dates = list(reports.find(myquery,{"_id": 0, "Unit": 0, "Value":0, "ThumbnailName": 0, "FileName":0}))
        datelist = []
        datalist = []
        minvalue = 1000000
        maxvalue = 0

        for date in dates:
            str_date = str(datetime.strftime(date["Date"], "%d-%m-%Y %I:%M:%S %p"))
            datelist.append(str_date)
    
        dates_dump = json_util.dumps(list(datelist))
        data = list(reports.find(myquery,{"_id": 0,"Date":0, "Unit": 0,"ThumbnailName": 0, "FileName":0}))
        for element in data:
            datalist.append(element["Value"])
            if element["Value"] != 0 and element["Value"] < minvalue:
                minvalue = element["Value"]
            if element["Value"] > maxvalue:
                maxvalue = element ['Value']


        data_dump = json_util.dumps(list(datalist))
        return render_template("charts.html", reports_date=dates_dump, reports_info=data_dump, min_data = minvalue, max_data = maxvalue)
    else:
        return render_template('login.html')


#Devices Page
@app.route('/devices', methods=["GET"])
def devices():
    if "username" in session:
        # specify the collections name
        devices = db.devices
        datetimenow = datetime.now()
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

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message
    resp.message("The Robots are coming! Head for the hills!")

    return str(resp)

@app.route("/process", methods=['GET', 'POST'])
def sms_readandprocess():
    account_sid = 'SK7c441cae49f9082ba3e3e5d61cc6fb4e'
    auth_token = 'K44v54cdEy6OoOQ2oGtmDvoxXAMlWMQZ'
        # auth_token = os.environ['K44v54cdEy6OoOQ2oGtmDvoxXAMlWMQZ']

    datetimenow = datetime.now()
    timezone = pytz.timezone("America/New_York")
    d_aware = timezone.localize(datetimenow)
    d_aware.tzinfo
    client = Client(account_sid, auth_token)
    records=[]
    messages = client.messages.list(limit=250, to='+17623204402')
    for record in messages:
        records.append(record)

    return render_template("processed-sms.html", device_reports=records,  timenow = d_aware)