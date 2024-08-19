from flask import Flask, request, jsonify, send_file
from flask_cors import CORS, cross_origin
from werkzeug.exceptions import BadRequest, BadRequestKeyError
from add_to_calendar import add_to_calendar

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def main():
    return send_file("../frontend/index.html")

@app.route("/login", methods=['post'])
def login():
    try:
        print("GETTING DATA")
        
        # TODO: Ensure sure all form data is inputted
        username = request.form['user']
        password = request.form['pass'] # TODO: Make password info secure
        start_date = request.form['startDate']
        print(username, password, start_date)

        add_to_calendar(username, password, start_date)

        # result = {
        #     'message'  : 'Login data received',
        #     'username' : username,
        #     'password' : password,
        # }
        return "Schedule Added" # jsonify(result)
    except BadRequest as e:
        print(f"{e}")
    

