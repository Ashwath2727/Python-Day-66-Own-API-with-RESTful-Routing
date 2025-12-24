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

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    with app.app_context():
        print("===========================> Creating tables")
        db.create_all()
        print("============================> Finished Creating tables")
    app.run(debug=True)
