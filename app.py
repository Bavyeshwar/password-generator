from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
from functools import wraps
import requests

import hashlib
import string
import math

import os

import passGen

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

    def hash_str(self):
        sha1_hash = hashlib.sha1()
        sha1_hash.update((self.pw).encode('utf-8'))
        return sha1_hash.hexdigest()
    def pwned(self):
        url = f'https://api.pwnedpasswords.com/range/{self.hash[:5]}'
        params = {
            'Add-Padding': True,
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.text.splitlines()
            suffix = self.hash[5:].upper()

            for line in data:
                api_suffix = line.split(':')[0]
                if api_suffix == suffix: return True
            return False
        except requests.exceptions.RequestException as e:
            print(f"error: {e}")
            return e

    def strength(self):
        size = 0
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        punctuation = string.punctuation
        digits = string.digits
        if any(char in lower for char in self.pw): size += len(lower)
        if any(char in upper for char in self.pw): size += len(upper)
        if any(char in digits for char in self.pw): size += len(digits)
        if any(char in punctuation for char in self.pw): size += len(punctuation)

        strength = (math.log2(size ** len(self.pw)))
        if self.pwned(): strength = strength - 50.0

        R = 94
        L = 20
        BENCHMARK = (math.log2(R ** L))
        percentage = int((strength / BENCHMARK) * 100)
        return min(100, max(0, percentage))

# Homepage
@app.route("/")
def index():
    return render_template("index.html")

# Not Found
@app.errorhandler(HTTPException)
def not_found(e):
    return render_template("404.html", error={"code": e.code, "name": e.name}), 404

@app.route("/tmp")
def tmp():
    return render_template("tmp.html")

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# Login


# Register


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
