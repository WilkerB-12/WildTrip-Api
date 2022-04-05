"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Base, TravelerUser,CompanyUser
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route("/sign-in-company", methods=['POST'])
def createCompany():
    body=request.json
    company=CompanyUser.create(
        email=body['email'],
        password=body['password'],
        phone_number=body['phone_number'],
        cloudinary_url=body['cloudinary_url'],
        company_name=body['company_name'],
        address=body['address'],
        instagram_url=body['instagram_url']
    )
    dictionary= company.serialize()
    print(dictionary)
    return jsonify(dictionary),201

@app.route("/sign-in-traveler", methods=['POST'])
def createTraveler():
    body=request.json
    traveler=TravelerUser.create(
        email=body['email'],
        password=body['password'],
        phone_number=body['phone_number'],
        cloudinary_url=body['cloudinary_url'],
        name=body['name'],
        lastname=body['lastname'],
        nickname=body['nickname']
    )
    dictionary= traveler.serialize()
    print(dictionary)
    return jsonify(dictionary),201



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5432))
    app.run(host='0.0.0.0', port=PORT, debug=False)
