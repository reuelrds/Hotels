from flask_restful import Resource

from model.hotel import Hotel


class Destination(Resource):

    def get(self):

        destinations = []
        
        for hotel in Hotel.select(Hotel.city, Hotel.country).distinct().dicts():

            destinations.append(hotel)


        return {'destinations': destinations}, 200
