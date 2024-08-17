from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest, BadRequestKeyError
from add_to_calendar import add_to_calendar

app = Flask(__name__)

@app.route("/login", methods=['POST'])
def run_calendar_api():
    try:
        print("GETTING DATA")
        data = request.get_json()
        
        username = data.get('username')
        password = data.get('password')

        add_to_calendar(username, password)

        result = {
            'message'  : 'Login data received',
            'username' : username,
            'password' : password,
        }
        return jsonify(result)
    except BadRequest as e:
        print(f"{e}")
    

