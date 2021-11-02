import datetime
import random
import re
import sys

sys.path.append(os.getcwd())

import peewee
import randomuser
import tqdm

import pandas as pd

from Backend.model.base import database
from Backend.model.review import Review

df = pd.read_csv(
    "./Backend/ML/files/dataset/dataset_finale.tsv",
    usecols=["ReviewedDate", "HotelName", "ReviewText"],
    sep="\t",
    encoding="latin-1",
)
df = df.dropna()

with database:
    database.create_tables([Review])

data_source = []
fields = [
    Review.review_text,
    Review.review_date,
    Review.hotel,
    Review.reviewer_name,
    Review.reviewer_profile_image,
]
date_pattern = re.compile(
    r"^\d\d-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d\d$"
)

for k, v in tqdm.tqdm(df.iterrows(), total=len(df)):

    if len(v["ReviewText"]) <= 20:
        continue

    if not date_pattern.match(v["ReviewedDate"]):
        continue

    data_source.append(
        [
            v["ReviewText"],
            datetime.datetime.strptime(v["ReviewedDate"], "%d-%b-%y"),
            v["HotelName"],
        ]
    )


user_list = randomuser.RandomUser.generate_users(
    len(data_source), get_params={"inc": "name,picture", "nat": "us,dk,fr,gb,ca"}
)


for row in data_source:

    reviewer = random.choice(user_list)
    row.extend([reviewer.get_full_name(), reviewer.get_picture()])


with database.atomic():

    for idx in tqdm.tqdm(range(0, len(data_source), 999)):
        Review.insert_many(data_source[idx : idx + 999], fields=fields).execute()
