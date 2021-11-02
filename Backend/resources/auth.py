import datetime
import uuid

import bcrypt
import flask_jwt_extended
import peewee

from flask_restful import Resource, reqparse
from playhouse.shortcuts import model_to_dict

from model.base import database
from model.user import User


class Login(Resource):
    def __init__(self):
        super().__init__()

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', required=True)
        self.parser.add_argument('password', required=True)



    # @flask_jwt_extended.jwt_required()
    def post(self):
        
        # jwt_user_email = flask_jwt_extended.get_jwt_identity()
        args = self.parser.parse_args(strict=True)
        try:
                user = User.get(User.email == args["email"])
                user = model_to_dict(user)
        except peewee.DoesNotExist:
                return {'message': "Invalid registeration!"}, 404


        if user:
            expires_delta = datetime.timedelta(hours=1)
            token = flask_jwt_extended.create_access_token(identity=user.get("email"), expires_delta=expires_delta)
            
            return {
                "message": "Login Successful",
                "user": user,
                "jwtToken": token,
                "expiresin": expires_delta.total_seconds()
            }, 200

        else:
            return {'message': "Invalid registeration!"}, 404




class Signin(Resource):

    def __init__(self):
        super().__init__()

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', required=True)
        self.parser.add_argument('username', required=True)
        self.parser.add_argument('password', required=True)


    def post(self):

        args = self.parser.parse_args(strict=True)
        print(f"New User: {args}")

        query = User.select().where(User.email == args["email"])

        if query.exists():
            return {'message': 'User already registered!!'}, 409

        else:

            hashed_password = bcrypt.hashpw(args["password"].encode("utf-8"), bcrypt.gensalt())

            with database.atomic() as txn:
                try:

                    User.create(
                        id=uuid.uuid4().hex,
                        email=args["email"],
                        name=args["username"],
                        password=hashed_password
                    )

                    txn.commit()

                except peewee.IntegrityError:
                    txn.rollback()

                    return {"message": "Error creating User"}, 409


            try:
                user = User.get(User.email == args["email"])
                user = model_to_dict(user)

            except peewee.DoesNotExist:
                    return {"message": "Error creating User"}, 500

            expires_delta = datetime.timedelta(hours=1)

            token = flask_jwt_extended.create_access_token(identity=user.get("email"), expires_delta=expires_delta)

            return {
                "message": "Signup Successful",
                "user": user,
                "jwtToken": token,
                "expiresin": expires_delta.total_seconds()
            }
        
