# main.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
import pyrebase
import os

main = Blueprint('main', __name__)

def init_firebase():
    config = {
      'apiKey': "AIzaSyDv-C6wf8u9CKylG65tzuuTdjjG9ksIRWY",
      'authDomain': "sif-rack.firebaseapp.com",
      'projectId': "sif-rack",
      'storageBucket': "sif-rack.appspot.com",
      'messagingSenderId': "284017095380",
      'appId': "1:284017095380:web:3525e17839e353d4a94141",
      'measurementId': "G-WVE6GYDJV8",
      'serviceAccount': "key.json"
    };
    
    firebase = pyrebase.initialize_app(config)
    
    return firebase

@main.route('/')
def index(loggedin = False):
    return render_template('index.html', loggedin=loggedin)

@main.route('/profile')
def profile():
    return render_template('profile.html', name=request.args.get('name'), loggedin=True)

#############################

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/login', methods=['POST'])
def login_post():
    firebase = init_firebase()
    firebasedb = firebase.database()
    firebasestorage = firebase.storage()
    
    firebaseemail = request.form.get('email')
    firebasepassword = request.form.get('password')
    print(firebaseemail)
    print(firebasepassword)
    
    try:
        auth = firebase.auth()
        auth.sign_in_with_email_and_password(firebaseemail, firebasepassword)
        firebasedb.child("users").push({"logged in": "Yes"})
        loggedin = True
    except:
        flash('Please check your firebase login details and try again.')
        return redirect(url_for('main.login'))
    
    head, sep, tail = firebaseemail.partition('@')
    print(head)
    return redirect(url_for('main.profile', name=head))

@main.route('/signup')
def signup():
    return render_template('signup.html')

@main.route('/signup', methods=['POST'])
def signup_post():
    firebase = init_firebase()
    db = firebase.database()
    storage = firebase.storage()
    
    firebaseemail = request.form.get('email')
    firebasepassword = request.form.get('password')
    
    auth = firebase.auth()
    auth.create_user_with_email_and_password(firebaseemail, firebasepassword)

    return redirect(url_for('main.login'))

@main.route('/logout')
def logout():
    return redirect(url_for('main.index'))

###############################

@main.route('/wifi')
def wifi():
    return render_template('wifi.html')

@main.route('/wifi', methods=['POST'])
def wifi_post():
    wifissid = request.form.get('email')
    wifipassword = request.form.get('password')
    print(wifissid)
    print(wifipassword)

    from pynq.lib import Wifi
    port = Wifi()

    port.connect(wifissid, wifipassword)

    response = os.system("ping -c 1 " + "www.google.com")
    
    if response == 0:
        return render_template('wifi.html')
    else:
        return redirect(url_for('main.wifi'))
    
    
