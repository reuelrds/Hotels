import os

from tripadvisor.database.schema import database
from tripadvisor.database.schema import Hotel


def setup_database():

    try:
        os.remove("./tripadvisor/database/hotels.db")

    except OSError:
        pass

    with database:
        database.create_tables([Hotel])
