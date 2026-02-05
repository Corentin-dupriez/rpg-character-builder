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
    """
    Opens a json file from the data folder based on the provided file name.
    Args:
        file_name: the name of the file to open
    Returns:
        A dictionary representing the json object
    Raises:
        FileNotFoundError: if the file doesn't exist
        json.JSONDecodeError: if the file is not a valid JSON
    """
    with open(data_folder / file_name, encoding="utf-8") as f:
        return json.load(f)


def load_races() -> RaceData:
    """
    Load and validates the race data from the races json file.
    Returns:
        RaceData: an object containing the several Race objects
    Raises:
        pydantic.ValidationError: If the JSON data does not conform
            to the `RaceData` schema.
        FileNotFoundError: If the races JSON file cannot be found.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    data = open_file("races.json")
    return RaceData.model_validate(data)


def load_classes() -> ClassesData:
    """
    Load and validates the classes data from the classes json file.
    Returns:
        ClassesData: an object containing several ClassInfo objects
    Raises:
        pydantic.ValidationError: If the JSON data doesn't conform
            to the `ClassesData` schema.
        FileNotFoundError: If the classes JSON file cannot be found.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    data = open_file("classes.json")
    return ClassesData.model_validate(data)


def load_skills() -> Skills:
    """
    Load and validates the skills data from the skills json file.
    Returns:
        Skills: an object containing a list of skills
    Raises:
        pydantic.ValidationError: If the JSON data doesn't conform
            to the `Skills` schema.
        FileNotFoundError: If the classes JSON file cannot be found.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    data = open_file("skills.json")
    return Skills.model_validate(data)


def load_backgrounds() -> BackgroundsData:
    """
    Load and validates the backgrounds data from the backgrounds json file.
    Returns:
        BackgroundsData: an object containing several backgrounds objects
    Raises:
        pydantic.ValidationError: If the JSON data doesn't conform
            to the `BackgroundsData` schema.
        FileNotFoundError: If the classes JSON file cannot be found.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    data = open_file("backgrounds.json")
    return BackgroundsData.model_validate(data)


# Instantiate the data from the JSON files to keep in memory
_RACES = load_races()
_CLASSES = load_classes()
_SKILLS = load_skills()
_BACKGROUNDS = load_backgrounds()


def choose_race() -> Race:
    """
    Generates a random choice of race.
    The likelihood of a race being picked depends on the specific weights of each race.
    Returns:
        Race: a randomly selected `Race` instance
    """
    return random.choices(_RACES.races, weights=[r.weight for r in _RACES.races], k=1)[
        0
    ]


def choose_class(race: Race) -> ClassInfo:
    """
    Generates a random choice of class.
    The likelihood of a class being picked depends on the class affinities of the race passed as input
    Args:
        race: a Race object representing the race used to generate the class. This will be used to calculate the weights for chosing the class.
    Returns:
        ClassInfo: a randomly selected `ClassInfo` instance
    """
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


def build_character(generate_description: bool = False) -> Character:
    race = choose_race()
    character_class = choose_class(race)
    background = choose_background(character_class)
    if generate_description:
        description = "hello"
    else:
        description = ""
    return Character(
        race=race,
        character_class=character_class,
        skills=choose_skills(race, character_class),
        background=background,
        description=description,
    )


def print_character(character: Character) -> None:
    print(
        f"Race: {character.race.name}\nClass: {character.character_class.name}\nSkills: {', '.join(character.skills)}\nBackground: {character.background.name}"
    )


if __name__ == "__main__":
    created_character = build_character()

    print_character(created_character)
