from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
from functools import wraps
import requests

import hashlib, string, math, passGen
from zxcvbn import zxcvbn

import os

app = Flask(__name__)

# Declare session norms.
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Check if user is logged in.
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if (session.get("user_id")): return f(*args, **kwargs)
        else: return redirect("/login")

    return decorated

# Make sure nothing is cached.
@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

class Password():
    def __init__(self, pword):
        self.pw = pword
        self.length = len(pword)
        self.hash = self.hash_str()
        self.strength = self.strength()
    def strength(password):
        if pawned(hash_string(password)):
            return 0
        return (zxcvbn(password)['score'] / 4) * 100
    def hash_string(s):
        return hashlib.sha1(s.encode('utf-8')).hexdigest()
    def pawned(hash):
        url = f"https://api.pwnedpasswords.com/range/{hash[:5]}"
        headers = {
            'Add-Padding': 'true',
        }
    
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.text.splitlines()
            suffix = hash[5:].upper()
    
            for line in data:
                if line.split(':')[0] == suffix:
                    return True
            return False
        except requests.exceptions.RequestException as e:
            print(e)
            return False

# Homepage
@app.route("/")
def index():
    return render_template("index.html")

# Not Found
@app.errorhandler(HTTPException)
def error(e):
    code = e.code
    return render_template("error.html", error={"code": code, "name": e.name}), code

@app.route("/tmp")
def tmp():
    return render_template("tmp.html")

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/create-session", methods=["POST"])
def create_session():
    token = request.json.get('token')
    try:
        verified = auth.verify(token)
        session["user_id"] = verified["uid"]
        session["email"] = verified["email"]
        return {"successful": True}, 200
    except Exception:
        return {"successful": False}, 401

# Password Generator
@login_required
@app.route("/password-generator", methods=["GET", "POST"])
def password_gen():
    if request.method == "POST":
        data = request.get_json()
        length = data["length"]
        if not length: return -1

        pool = data["pool"]
        common_punct = False
        extra_punct = False
        lowercase = False
        uppercase = False
        digits = False
        if "common_punctuation" in pool: common_punct = True
        if "extra_punctuation" in pool: extra_punct = True
        if "uppercase_letters" in pool: uppercase = True
        if "lowercase_letters" in pool: lowercase = True
        if "digits" in pool: digits = True
        pw = passGen.generate(common_punct, extra_punct, uppercase, lowercase, digits, int(length))
        return jsonify({"pw": pw})
    else:
        return render_template("passwordGen.html")

# Password-Strength-Checker
@login_required
@app.route("/strength", methods=["GET", "POST"])
def password_strength():
    if request.method == "POST":
        pw = request.get_json()["string"]
        if not pw: return -1
        return jsonify({ "strength": Password(pw).strength })
    else:
        return render_template("passwordStrength.html")

@login_required
@app.route("/passphrase-generator", methods=["GET", "POST"])
def passphrase():
    if request.method == "POST":
        data = request.get_json()
        if not data: return -1
        return jsonify({"pw": passGen.transform(data["phrase"])})
    else:
        return render_template("passphrase.html")

if __name__ == "__main__":
    app.run(debug=True)
