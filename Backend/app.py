import os

from dotenv import load_dotenv

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from resources.auth import Login
from resources.auth import Signin

from resources.hotel import Hotel
from resources.review import Review

from resources.destination import Destination
from utils.init import setup_database


load_dotenv()


app = Flask(__name__, static_folder="./files/hotel_images", static_url_path="")
CORS(app)
api = Api(app)

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

setup_database()
jwt = JWTManager(app)


api.add_resource(Signin, "/auth/signup")
api.add_resource(Login, "/auth/login")
api.add_resource(Destination, "/destinations")
api.add_resource(Hotel, "/hotels")
api.add_resource(Review, "/reviews")

if __name__ == "__main__":
    app.run(debug=True)
