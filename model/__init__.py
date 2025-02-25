from app import app
from flask import request, session
from helpers.database import *
from helpers.hashpass import *
from helpers.mailer import *
from bson import json_util, ObjectId
import json

def checkloginusername():
    username = request.form["username"]
    check = db.users.find_one({"username": username})
    if check is None:
        return "No User"
    else:
        return "User exists"

def checkloginpassword():
    username = request.form["username"]
    check = db.users.find_one({"username": username})
    password = request.form["password"]
    hashpassword = getHashed(password)
    if hashpassword == check["password"]:
#        sendmail(subject="Login on JRG Watr Dashboard", sender="JRG Watr Dashboard", recipient=check["email"], body="You successfully logged in on JRG Watr Dashboard")
        session["username"] = username
        return "correct"
    else:
        return "wrong"
    
def checkusername():
    username = request.form["username"]
    check = db.users.find_one({"username": username})
    if check is None:
        return "Available"
    else:
        return "Username taken"

def registerUser():
    fields = [k for k in request.form]                                      
    values = [request.form[k] for k in request.form]
    data = dict(zip(fields, values))
    user_data = json.loads(json_util.dumps(data))
    user_data["password"] = getHashed(user_data["password"])
    user_data["confirmpassword"] = getHashed(user_data["confirmpassword"])
    db.users.insert(user_data)
    sendmail(subject="Registration for JRG Watr Dashboard", sender="JRG Watr Dashboard", recipient=user_data["email"], body="You successfully registered on JRG Watr Dashboard")
    print("Done")


    
