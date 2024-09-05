from flask import Flask, request, flash, jsonify, render_template
from flask_session import Session
from flask_cors import CORS, cross_origin
from werkzeug.exceptions import BadRequest, BadRequestKeyError
from add_to_calendar import add_to_calendar, LoginResult

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
sess = Session()

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/login", methods=['post'])
def login():
    try:
        print("GETTING DATA")
        
        # Obtain form data
        username = request.form['user']
        password = request.form['pass'] # Should be secure if sent across https
        start_date = request.form['startDate']
        print(username, password, start_date)

        # Check login
        return_val = add_to_calendar(username, password, start_date)
        if return_val == LoginResult.INVALID_LOGIN:
            flash('Login failed: Invalid credentials or Duo Mobile authentication was not approved.', 'danger')
        elif return_val == LoginResult.NO_CLASSES_FOUND:
            flash('No classes were found!', 'warning')
        else:
            flash('Schedule successfully added!', 'success')
        
        return render_template("index.html")
    except BadRequest as e:
        print(f"{e}")
        

        
if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)

    app.debug = True
    app.run()
