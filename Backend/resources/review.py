from flask_restful import Resource, reqparse
from playhouse.shortcuts import model_to_dict

from model.hotel import Hotel
from model.review import Review


class Review(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("hotel_id")

    def get(self):

        args = self.parser.parse_args(strict=True)
        hotel = Hotel.get_or_none(Hotel.hotel_id == args["hotel_id"])

        reviews = list(hotel.reviews.limit(5).dicts())
        for review in reviews:
            review["review_date"] = review["review_date"].isoformat()

            del review["hotel"]

        if hotel:

            return {"reviews": reviews}, 200

        else:
            return {"message": "Hotel not Found"}, 404
