import random
from urllib.parse import quote

from flask import Flask, jsonify, render_template, request

from data.cafe_data import CafeData
from db_queries.cafe_queries import CafeQueries
from extensions import db
from models import cafe

from models.cafe import Cafe

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)


# Connect to Database
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = quote("ashwath@MVN123")
DB_HOST = "localhost"

SQLALCHEMY_DB_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DB_URI
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)

cafes = Cafe()
cafe_data = CafeData()
cafe_queries = CafeQueries()

api_key = "ashwath34MVN4312"


@app.route("/")
def home():
    cafes = cafe_data.get_cafes()
    print(f"home ===========> {cafes}")

    for cafe in cafes:
        cafe_queries.add_cafe(cafe)

    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random")
def get_random_cafe():

    rand_cafe = cafe_queries.get_random_cafe()

    print(f"random cafe = {rand_cafe}")

    return jsonify(cafes=rand_cafe.to_dict())


@app.route("/all")
def get_all_cafe():
    cafes = cafe_queries.get_all_cafes()

    cafes_dict_list = [cafe.to_dict() for cafe in cafes]

    return jsonify(cafes_dict_list)


@app.route("/search")
def get_cafe_by_location():

    location = request.args.get("location")

    cafes = cafe_queries.get_cafe_by_location(location)

    if cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in cafes])
    else:
        return jsonify({"error": {"Not Found": "Sorry, we dont have a cafe at that location"}})


# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add_cafe():

    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        seats=request.form.get("seats"),
        has_toilet=bool(request.form.get("has_toilet")),
        has_wifi=bool(request.form.get("has_wifi")),
        has_sockets=bool(request.form.get("has_sockets")),
        can_take_calls=bool(request.form.get("can_take_calls")),
        coffee_price=request.form.get("coffee_price"),
    )

    cafe_queries.add_cafe(new_cafe)

    return jsonify({"success": "Successfully added cafe"})

# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    new_price = request.args.get("new_price")
    result = cafe_queries.update_price(cafe_id, new_price)
    message = result.get("message")
    code = result.get("code")

    return jsonify(message), code

# HTTP DELETE - Delete Record
@app.route("/report-closed/<cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):

    input_key = request.args.get("api-key")
    print(f"input key = {input_key}")

    if input_key == api_key:
        result = cafe_queries.delete_cafe(cafe_id)

        return jsonify(result.get("message")), result.get("code")

    else:
        message = {"error": "Sorry, that's not allowed. Make sure you have the correct API key"}
        return jsonify(message=message), 403


if __name__ == '__main__':
    with app.app_context():
        print("===========================> Creating tables")
        db.create_all()
        print("============================> Finished Creating tables")
    app.run(debug=True)
