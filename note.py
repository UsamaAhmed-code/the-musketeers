from flask import Flask, jsonify, make_response, request
import jwt
import json
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SomeSecretKey'

# give the notes to the user if there r any
@app.route("/get-notes")
def get_notes_data():
    
    cookies = request.cookies

    token = cookies.get("notes")

    notes = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")

    return jsonify(notes)

# save the notes in the user browser cookies
@app.route("/save-notes", methods=["POST", "GET"])
def save_notes_data():
   
    # turn the notes into a jwt
    if request.method == "POST":
        notes = request.data.decode("utf-8")
        notes_as_json = json.loads(notes)
        decoded_notes = jwt.encode(notes_as_json, app.config["SECRET_KEY"])
        cookie_expire = datetime.datetime.now() + datetime.timedelta(days=5*365)

    # return the jwt as a cookie
    res = make_response("", 200)

    res.set_cookie("notes", decoded_notes, expires=cookie_expire)
    
    return res


if __name__ == "__main__":
    app.run()
