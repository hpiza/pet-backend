from flask import Flask, request, jsonify
from datetime import timedelta
from flask_jwt_extended import create_access_token, get_jwt_identity, JWTManager, jwt_required


def populate_pet_list():
    pet_list.append(Pet("Jack Russell", 4, "white", 12.4).__dict__)
    pet_list.append(Pet("Dalmata", 6, "white", 15.6).__dict__)
    pet_list.append(Pet("Pitbull", 9, "brown", 18.3).__dict__)


server = Flask(__name__)
server.config["JWT_SECRET_KEY"] = "my secret key"
server.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=5)
pet_list = list()
populate_pet_list()
jwt = JWTManager(server)


@server.route("/welcome")
def welcome():
    return "Welcome to the Pet web service"


def user_valid(username, password):
    return username == "admin" and password == "hello123"


@server.route('/')
def hello_world():
    return 'Welcome to the Pet web service!'


@server.route("/login", methods=['POST'])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]
    if not user_valid(username, password):
        return jsonify({"error": "Bad username or password"}), 401

    token = create_access_token(identity=username)
    return jsonify(bearer_token=token), 200


class Pet:
    def __init__(self, breed, age, color, weight):
        self.breed = breed
        self.age = age
        self.color = color
        self.weight = weight


def pets_post():
    if not request.data:
        return jsonify({"error": "Pet data is missing"}), 404

    pet_list.append(request.json)
    result = {"message": "I received your pet data",
              "pet": request.json}
    return jsonify(result), 201


def pets_get():
    return jsonify(pet_list), 200


def user_allowed(username):
    return username == "admin"


@server.route("/pets", methods=['GET', 'POST'])
@jwt_required()
def pets():
    current_user = get_jwt_identity()
    if not user_allowed(current_user):
        return jsonify({"error": "Invalid user"}), 403

    if request.method == 'GET':
        return pets_get()
    else:
        return pets_post()
