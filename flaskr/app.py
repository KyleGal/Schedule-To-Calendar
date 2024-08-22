from flask import Flask, request, url_for, redirect, flash, jsonify, send_file, render_template
from flask_cors import CORS, cross_origin
from werkzeug.exceptions import BadRequest, BadRequestKeyError
from add_to_calendar import add_to_calendar

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/login", methods=['post'])
def login():
    try:
        print("GETTING DATA")
        
        username = request.form['user']
        password = request.form['pass'] # Should be secure if sent across https
        start_date = request.form['startDate']
        print(username, password, start_date)

        add_to_calendar(username, password, start_date)
        # TODO: HANDLE INVALID LOGIN
        # result = {
        #     'message'  : 'Login data received',
        #     'username' : username,
        #     'password' : password,
        # }
        return render_template("index.html")
        return "Schedule Added" # jsonify(result)
    except BadRequest as e:
        print(f"{e}")
    except Exception as e:
        flash(f"Possible Invalid Login")
        
