import os
import random
import json
from models import RaceData

data_folder = os.path.join(
    os.path.abspath(os.path.join(os.getcwd(), os.pardir)), "data"
)


def load_races() -> RaceData:
    with open(os.path.join(data_folder, "races.json")) as file:
        data = json.load(file)

    return RaceData.model_validate(data)


races = {race.name: race.weight for race in load_races().races}

names = list(races.keys())
weights = list(races.values())

print(random.choices(names, weights=weights, k=1)[0])
