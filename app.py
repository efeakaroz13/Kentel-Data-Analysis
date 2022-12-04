# EFE AKARÖZ 2022 ALL RIGHTS RESERVED
from flask import Flask, render_template, request, redirect, abort, make_response
import pyrebase
import requests
from credentials import CONF
from cryptography.fernet import Fernet
import time
import os
import json

key = b'wq4l6o7Dqvp7ev7R6L23tW40v1Dj8S-6IoJ3ZdMZP3Y='

crypter = Fernet(key)


def encrypt(text):

    return crypter.encrypt(str(text).encode()).decode()


def decrypt(text):
    # crypter.decrypt(str(text).encode())
    return crypter.decrypt(text.encode()).decode()


value = CONF().value
print(value)
firebase = pyrebase.initialize_app(CONF().firebaseConfig)
db = firebase.database()
auth = firebase.auth()
app = Flask(__name__)


@app.route("/")
def index():
    email = request.cookies.get("email")
    if email != None or email != "":
        try:
            email = decrypt(email)
            password = request.cookies.get("password")
            password = decrypt(password)
            auth.sign_in_with_email_and_password(email, password)
            alldatabase = json.loads(requests.get(
                CONF().firebaseConfig["databaseURL"]+"/"+CONF().value+".json").content)
            for d in alldatabase["userdata"]:
                current = alldatabase["userdata"][d]
                emailofcurrentdata = current["email"]
                if email == emailofcurrentdata:
                    datagonnauser = current
                    break
            fullname = datagonnauser["fullname"]

            return render_template("homepage.html", email=email, data=datagonnauser, fullname=fullname)
        except Exception as e:
            print(str(e))
            return render_template("index.html")
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    try:
        ifemailexists = decrypt(request.cookies.get("email"))
    except:
        ifemailexists = ""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            auth.sign_in_with_email_and_password(email, password)
            response = make_response(redirect("/"))
            email = encrypt(email)
            password = encrypt(password)
            response.set_cookie("email", email)
            response.set_cookie("password", password)
            return response
        except Exception as e:
            return render_template("login.html", error=True, code_err=str(e))
    return render_template("login.html", email=ifemailexists)


@app.route("/register", methods=["POST", "GET"])
def register():

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        fullname = request.form.get("fullname")
        registrationtime = time.time()
        email = email.lower()
        try:
            ipaddr = request.environ['HTTP_X_FORWARDED_FOR']
            if ipaddr == None:
                ipaddr = request.environ['REMOTE_ADDR']
        except:
            ipaddr = request.environ['REMOTE_ADDR']
        data = {
            "username": username,
            "email": email,
            "fullname": fullname,
            "regtime": registrationtime,
            "ipaddr": ipaddr,
            "userAgent": request.headers.get('User-Agent'),


        }
        db.child(value).child("userdata").child(username).update(data)
        response = make_response(redirect("/login"))
        response.set_cookie("email", encrypt(email))
        try:
            auth.create_user_with_email_and_password(email, password)
        except:
            return render_template("register.html", error=True)
        return response
    if request.method == "GET":
        return render_template("register.html")


@app.route("/collect")
def collect():
    timestarted = time.time()
    apikey = request.args.get("apikey")
    ipaddr = request.args.get("ipaddr")
    useragent = request.headers.get("User-Agent")
    username = request.args.get("username")
    try:
        json.loads(open(f"{apikey}.json", "r").read())
        ipaddr.split(".")[2]
        useragent.split("Mozilla")[1]

        os.system(
            f'./kentel "{username}" "{ipaddr}" "{useragent}" "{apikey}" ')

    except:
        pass

    timefinished = time.time()
    return {"Response Time": timefinished-timestarted}


@app.route("/createproject", methods=["POST", "GET"])
def createproject():
    try:
        email = decrypt(request.cookies.get("email"))
        password = decrypt(request.cookies.get("password"))
        alldatabase = json.loads(requests.get(
            CONF().firebaseConfig["databaseURL"]+"/"+CONF().value+".json").content)
        for d in alldatabase["userdata"]:
            current = alldatabase["userdata"][d]
            emailofcurrentdata = current["email"]
            if email == emailofcurrentdata:
                datagonnauser = current
                break
        fullname = datagonnauser["fullname"]
    except:
        return redirect("/login")

    return render_template("createproject.html",data=datagonnauser)


app.run(debug=True)
