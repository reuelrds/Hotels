from model.base import database
from model.hotel import Hotel
from model.user import User


def setup_database():

    with database:
        database.create_tables([Hotel, User])
