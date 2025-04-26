from flask import Flask, render_template, request, redirect, session, url_for, jsonify, send_file
import threading
import os
import json
import logging
from io import BytesIO
import re

with open("config/config.json") as f:
    config = json.load(f)
DASHBOARD_PASSWORD = config.get("dashboard_password", "changeme")

app = Flask(__name__)
app.secret_key = os.urandom(24)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

log_buffer = []

def strip_ansi_codes(text):
    ansi_escape = re.compile(r'(\x1B[@-_][0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def add_log(message):
    cleaned_message = strip_ansi_codes(message)
    log_buffer.append(cleaned_message)

def start_web_server():
    server_thread = threading.Thread(target=lambda: app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False))
    server_thread.start()

import builtins
original_print = builtins.print

def custom_print(*args, **kwargs):
    message = " ".join(str(arg) for arg in args)
    add_log(message)
    original_print(*args, **kwargs)

def hijack_print():
    builtins.print = custom_print

@app.route("/")
def home():
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == DASHBOARD_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template("login.html", error="Incorrect password.")
    return render_template("login.html")

@app.route("/discord-selfbot")
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/api/logs")
def api_logs():
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(log_buffer[-200:])

@app.route("/api/clear", methods=["POST"])
def api_clear():
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    log_buffer.clear()
    return jsonify({"success": True})

@app.route("/api/export", methods=["GET"])
def api_export():
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    log_data = "\n".join(log_buffer)
    return send_file(BytesIO(log_data.encode()), mimetype='text/plain', as_attachment=True, download_name="logs.txt")