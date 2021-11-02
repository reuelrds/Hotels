import peewee

database = peewee.SqliteDatabase("./files/hotels.db")

# Pewee related Setup
class BaseModel(peewee.Model):
    class Meta:
        database = database