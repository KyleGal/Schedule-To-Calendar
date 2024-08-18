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
        
        username = request.form['user']
        password = request.form['pass']
        print(username, password)
        add_to_calendar(username, password)

        # result = {
        #     'message'  : 'Login data received',
        #     'username' : username,
        #     'password' : password,
        # }
        return "Schedule Added" # jsonify(result)
    except BadRequest as e:
        print(f"{e}")
    

