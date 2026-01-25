import os
import random
import json
from typing import Dict
from models import RaceData, Character, ClassesData, Skills

data_folder = os.path.join(
    os.path.abspath(os.path.join(os.getcwd(), os.pardir)), "data"
)


def open_file(file_name) -> Dict:
    with open(os.path.join(data_folder, file_name)) as f:
        data = json.load(f)

    return data


def load_races() -> RaceData:
    data = open_file("races.json")
    return RaceData.model_validate(data)


def load_classes() -> ClassesData:
    data = open_file("classes.json")
    return ClassesData.model_validate(data)


def load_skills() -> Skills:
    pass


def choose_race() -> str:
    races = {race.name: race.weight for race in load_races().races}

    names = list(races.keys())
    weights = list(races.values())

    return random.choices(names, weights=weights, k=1)[0]


def choose_class() -> str:
    classes = {
        class_data.name: class_data.weight for class_data in load_classes().classes
    }

    classes_names = list(classes.keys())
    weights = list(classes.values())

    return random.choices(classes_names, weights=weights, k=1)[0]


def build_character() -> Character:
    return Character(
        race=choose_race(), character_class=choose_class(), skills=[], description=""
    )


created_character = build_character()

print(created_character)
