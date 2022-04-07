"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_jwt_extended import JWTManager,create_access_token
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import CompanyPost, db, Base, TravelerUser,CompanyUser
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY']="secret-wildtrip"
jwt=JWTManager(app)
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

@app.route("/token",methods=['POST'])
def create_token():
    email=request.json.get("email",None)
    password=request.json.get("password",None)
    user=CompanyUser.query.filter_by(email=email, password=password).first()
    if user is None:
        user=TravelerUser.query.filter_by(email=email, password=password).first()
    if user is None:
        return jsonify({"msg":"Error en el email o en la contraseña"}),401
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id })

@app.route('/user-company/<int:id>', methods=['GET'])
def handle_users_company(id):
        user=CompanyUser.query.get(id)
        if user is None:
            return jsonify({
                "msg":"not found"
            })
        return jsonify(user.serialize()),200

@app.route('/user-traveler/<int:id>', methods=['GET'])
def handle_users_traveler(id):
        user=TravelerUser.query.get(id)
        if user is None:
            return jsonify({
                "msg":"not found"
            })
        return jsonify(user.serialize()),200

@app.route("/sign-in-company", methods=['POST'])
def createCompany():
    new_email=request.json.get("email",None)
    new_company_name=request.json.get("company_name",None)
    registered_email=CompanyUser.query.filter_by(email=new_email).first()
    registered_company_name=CompanyUser.query.filter_by(company_name=new_company_name).first()
    if registered_email is not None:
        return jsonify({"msg":"El email ya está en uso"}),400
    elif registered_company_name is not None:
        return jsonify({"msg":"El nombre de la compañía ya está en uso"}),400
    else:
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
    new_email=request.json.get("email",None)
    new_nickname=request.json.get("nickname",None)
    registered_email=TravelerUser.query.filter_by(email=new_email).first()
    registered_nickname=TravelerUser.query.filter_by(nickname=new_nickname).first()
    if registered_email is not None:
        return jsonify({"msg":"El email ya está en uso"}),400
    elif registered_nickname is not None:
        return jsonify({"msg":"El nickname ya está en uso"}),400
    else:
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

@app.route("/posts",methods=['GET','POST'])
def handlePost():
    if request.method== 'GET':
        posts=CompanyPost.query.all()
        return jsonify(list(map(
            lambda post: post.serialize(),
            posts
        ))),201
    
    else:
        body=request.json
        posts=CompanyPost.create(
            cloudinary_url=body['cloudinary_url'],
            city=body['city'],
            state=body['state'],
            country=body['country'],
            title=body['title'],
            date=body['date'],
            description=body['description'],
            company_name=body['company_name']
        )
        dictionary= posts.serialize()
        print(dictionary)
        return jsonify(dictionary),201
@app.route("/companies")
def handleCompanies():
        companies=CompanyUser.query.all()
        return jsonify(list(map(
            lambda user: user.serialize(),
            companies
        ))),201
##@app.route("/posts/<int:>",methods=['GET'])
##def get_one_post
    



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5432))
    app.run(host='0.0.0.0', port=PORT, debug=False)
