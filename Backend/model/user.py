import peewee
from model.base import BaseModel


class User(BaseModel):

    id = peewee.TextField(
        index=True,
        unique=True,
        verbose_name="Unique ID"
    )

    email = peewee.TextField(
        index=True,
        unique=True,
        verbose_name="User Email",
    )

    name = peewee.TextField(
        verbose_name="User Name",
    )
    password = peewee.TextField(
        verbose_name="User password",
    )
    