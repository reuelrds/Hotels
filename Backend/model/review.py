import peewee
from model.base import BaseModel
from model.hotel import Hotel


class Review(BaseModel):

    id = peewee.AutoField()
    review_text = peewee.TextField(verbose_name="The Review Text")

    review_date = peewee.DateTimeField(verbose_name="Date that the review as written")

    reviewer_name = peewee.DateTimeField(
        verbose_name="The name of the person who wrote the review"
    )

    reviewer_profile_image = peewee.DateTimeField(
        verbose_name="The profile image url of the reviewer"
    )

    hotel = peewee.ForeignKeyField(Hotel, field=Hotel.hotel_id, backref="reviews")
