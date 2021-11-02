import datetime
import math
import random
import os

import flask

from pathlib import Path

from flask_restful import Resource, reqparse

from model.base import database
from model.hotel import Hotel as HotelModel

from ML.infer import recommendation


class Hotel(Resource):
    def __init__(self):
        super().__init__()

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('destination')
        self.parser.add_argument('checkinDate')
        self.parser.add_argument('checkoutDate')
        self.parser.add_argument('rooms')
        self.parser.add_argument('guests')
        self.parser.add_argument('aspectFilter')

    @staticmethod
    def _get_hotel_images(image_count):
        return random.sample(list(os.listdir("./files/hotel_images")), image_count) 

    @staticmethod
    def _get_random_hotels(city, country, booking_duration):
        hotels = []
            
        for hotel in HotelModel.select().where(HotelModel.city == city, HotelModel.country == country).dicts():

            hotel["total_price"] = round(hotel["unit_price"] + math.log(hotel["unit_price"]) * booking_duration, 2)
            hotels.append(hotel)

        if len(hotels) > 7:
            hotels = random.sample(hotels, 7)


        for hotel, image_path in zip(hotels, Hotel._get_hotel_images(len(hotels))):

            hotel["image_url"] = image_path

        return hotels    


    def get(self):

        args = self.parser.parse_args(strict=True)
        city = args["destination"].split(",")[0].strip()
        country = args["destination"].split(",")[-1].strip()

        print(city)
        print(country)
        print(args)


        checkin_date = datetime.datetime.strptime(args["checkinDate"], "%Y-%m-%dT%H:%M:%S.%fZ")
        checkout_date = datetime.datetime.strptime(args["checkoutDate"], "%Y-%m-%dT%H:%M:%S.%fZ")

        booking_duration = (checkout_date - checkin_date).total_seconds() // (86400)


        if args["aspectFilter"] == "":
            print("Retuning Random Hotels")

            hotels = Hotel._get_random_hotels(city, country, booking_duration)

            return {
                "message": "",
                "hotels": hotels
            }, 200

            

        else:
            
            hotel_list = recommendation(args["destination"], args["aspectFilter"], 7)
            print()
            print()
            print()
            print(hotel_list)
            print()
            print()
            print()

            if hotel_list:

                hotels = []
                for hotel in HotelModel.select().where(HotelModel.hotel_id.in_(hotel_list)).dicts():

                    hotel["total_price"] = round(hotel["unit_price"] + math.log(hotel["unit_price"]) * booking_duration, 2)
                    hotels.append(hotel)

                for hotel, image_path in zip(hotels, Hotel._get_hotel_images(len(hotels))):
                    hotel["image_url"] = image_path

                return {
                    "message": "",
                    'hotels': hotels
                }, 200


            else:
                hotels = Hotel._get_random_hotels(city, country, booking_duration)
                return {
                    "message": "We couldn't find any hotels maching your specifications. But here's a list of hotels from the same destination that might interest you...",
                    'hotels': hotels
                }, 200





# class RecommendHotel(Resource):

#     def get(self):
        
#         return {'hotels': []}
