import os

from tripadvisor.database.schema import database
from tripadvisor.database.schema import Hotel


def setup_database():

    try:
        os.remove("./tripadvisor/files/hotels.db")

    except OSError as err:
        print(err)
        pass

    with database:
        database.create_tables([Hotel])
