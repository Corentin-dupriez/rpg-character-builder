import random
import json
from pathlib import Path
from typing import Dict
from models import (
    RaceData,
    Character,
    ClassesData,
    Skills,
    Race,
    ClassInfo,
    BackgroundsData,
    Background,
)

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


def load_backgrounds() -> BackgroundsData:
    data = open_file("backgrounds.json")
    return BackgroundsData.model_validate(data)


_RACES = load_races()
_CLASSES = load_classes()
_SKILLS = load_skills()
_BACKGROUNDS = load_backgrounds()


def choose_race() -> Race:
    return random.choices(_RACES.races, weights=[r.weight for r in _RACES.races], k=1)[
        0
    ]


def choose_class(race: Race) -> ClassInfo:
    affinities = race.class_affinities
    classes = []
    weights = []
    for c in _CLASSES.classes:
        modifier = affinities.get(c.name, 1.0)
        classes.append(c)
        weights.append(c.weight * modifier)

    return random.choices(classes, weights=weights, k=1)[0]


def weighted_samples(items: list, weights: list, k: int) -> list:
    if k > len(items):
        raise ValueError("k cannot be larger than the population")

    items = items.copy()
    weights = weights.copy()
    chosen = []

    for _ in range(k):
        choice = random.choices(items, weights=weights, k=1)[0]
        idx = items.index(choice)
        items.pop(idx)
        weights.pop(idx)
        chosen.append(choice)

    return chosen


def choose_skills(race: Race, class_info: ClassInfo) -> list:
    skills_affinities = race.skills_affinities
    class_skills_affinities = class_info.skills
    weights = []
    for s in _SKILLS.skills:
        modifier = skills_affinities.get(s, 1.0) * class_skills_affinities.get(s, 1.0)
        weights.append(modifier)

    return weighted_samples(_SKILLS.skills, weights, 3)


def choose_background(class_info: ClassInfo) -> Background:
    weigths = []

    for b in _BACKGROUNDS.backgrounds:
        weigths.append(b.weight * b.class_affinities.get(class_info.name, 1.0))

    return random.choices(_BACKGROUNDS.backgrounds, weights=weigths, k=1)[0]


def build_character() -> Character:
    race = choose_race()
    character_class = choose_class(race)
    background = choose_background(character_class)
    return Character(
        race=race,
        character_class=character_class,
        skills=choose_skills(race, character_class),
        background=background,
        description="",
    )


def print_character(character: Character) -> None:
    print(
        f"Race: {character.race.name}\nClass: {character.character_class.name}\nSkills: {', '.join(character.skills)}\nBackground: {character.background.name}"
    )


created_character = build_character()

print_character(created_character)
