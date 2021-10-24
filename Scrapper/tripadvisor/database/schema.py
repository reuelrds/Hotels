import peewee

database = peewee.SqliteDatabase("./tripadvisor/files/hotels.db")


# Pewee related Setup
class BaseModel(peewee.Model):
    class Meta:
        database = database


class Hotel(BaseModel):

    id = peewee.TextField(
        index=True,
        verbose_name="Unique ID"
    )

    hotel_id = peewee.TextField(
        index=True,
        verbose_name="Hotel ID"
    )

    name = peewee.TextField(
        verbose_name="Hotel Name",
    )
    address = peewee.TextField(
        null=True,
        verbose_name="Hotel Address",
    )
    unit_price = peewee.IntegerField(
        null=True,
        verbose_name="Price for a Single Room",
    )
    rating = peewee.FloatField(
        null=True,
        verbose_name="Hotel Rating",
    )
    review_count = peewee.IntegerField(
        null=True,
        verbose_name="Hotel Review Count",
    )
    description = peewee.TextField(
        null=True,
        verbose_name="Hotel Description",
    )
    city = peewee.TextField(
        null=True,
        verbose_name="Hotel City",
    )

    country= peewee.TextField(
        null=True,
        verbose_name="Hotel Country",
    )
    # amenities = peewee.TextField(
    #     null=True,
    #     verbose_name="Hotel Amenities",
    # )
