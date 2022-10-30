#EFE AKARÖZ 2022 ALL RIGHTS RESERVED
from flask import Flask,render_template,request,redirect,abort,make_response
import pyrebase
import requests
from credentials import CONF
from cryptography.fernet import Fernet
import time


key = b'wq4l6o7Dqvp7ev7R6L23tW40v1Dj8S-6IoJ3ZdMZP3Y='

crypter = Fernet(key)

def encrypt(text):

    return crypter.encrypt(str(text).encode()).decode()

def decrypt(text):
    #crypter.decrypt(str(text).encode())
    return crypter.decrypt(text.encode()).decode()





firebase = pyrebase.initialize_app(CONF().firebaseConfig)
db = firebase.database()
auth = firebase.auth()
app = Flask(__name__)
@app.route("/")
def index():
    email = request.cookies.get("email")
    if email != None or email !="":
        try:
            email = decrypt(email)
            password = request.cookies.get("password")
            password = decrypt(password)
            auth.sign_in_with_email_and_password(email,password)
            return render_template("homepage.html",email=email)
        except:
            return render_template("index.html")
    return render_template("index.html")

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            auth.sign_in_with_email_and_password(email,password)
            response = make_response(redirect("/"))
            email = encrypt(email)
            password = encrypt(password)
            response.set_cookie("email",email)
            response.set_cookie("password",password)
        except Exception as e:
            return render_template("login.html",error=True,code_err=str(e))
    return render_template("login.html")

@app.route("/register",methods=["POST","GET"])
def register():

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        fullname = request.form.get("fullname")
        registrationtime = time.time()
        try:
            ipaddr = request.environ['HTTP_X_FORWARDED_FOR']
            if ipaddr == None:
                ipaddr= request.environ['REMOTE_ADDR']
        except:
            ipaddr = request.environ['REMOTE_ADDR']
        data = {
            "username":username,
            "email":email,
            "fullname":fullname,
            "regtime":registrationtime,
            "ipaddr":ipaddr,
            "userAgent":request.headers.get('User-Agent'),
            
            
        }

    if request.method == "GET":
        return render_template("register.html")



app.run(debug=True)