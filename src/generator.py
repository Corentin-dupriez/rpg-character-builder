import random
import json
from pathlib import Path
from typing import Dict
from models import RaceData, Character, ClassesData, Skills, Race

BASE_DIR = Path(__file__).resolve().parent.parent
data_folder = BASE_DIR / "data"


def open_file(file_name: str) -> Dict:
    with open(data_folder / file_name, encoding="utf-8") as f:
        return json.load(f)


def load_races() -> RaceData:
    data = open_file("races.json")
    return RaceData.model_validate(data)


def load_classes() -> ClassesData:
    data = open_file("classes.json")
    return ClassesData.model_validate(data)


def load_skills() -> Skills:
    data = open_file("skills.json")
    return Skills.model_validate(data)


_RACES = load_races()
_CLASSES = load_classes()
_SKILLS = load_skills()


def choose_race() -> Race:
    return random.choices(_RACES.races, weights=[r.weight for r in _RACES.races], k=1)[
        0
    ]


def choose_class(race: Race) -> str:
    affinities = race.class_affinities
    classes = []
    weights = []
    for c in _CLASSES.classes:
        modifier = affinities.get(c.name, 1.0)
        classes.append(c)
        weights.append(c.weight * modifier)

    return random.choices(classes, weights=weights, k=1)[0]


def choose_skills() -> list:
    return random.sample(_SKILLS.skills, k=3)


def build_character() -> Character:
    race = choose_race()
    return Character(
        race=race,
        character_class=choose_class(race),
        skills=choose_skills(),
        description="",
    )


def print_character(character: Character) -> None:
    print(
        f"Race: {character.race.name}\nClass: {character.character_class.name}\nSkills: {', '.join(character.skills)}"
    )


created_character = build_character()

print_character(created_character)
