from generator import load_races, load_classes, load_skills, load_backgrounds
from generator import build_character


def test_load_races():
    races_data = load_races()

    assert races_data is not None
    assert len(races_data.races) > 0


def test_load_race_has_required_data():
    races_data = load_races().races

    for race in races_data:
        assert race.name
        assert race.weight > 0


def test_load_classes():
    classes_data = load_classes()

    assert classes_data is not None
    assert len(classes_data.classes) > 0


def test_load_skills():
    skills_data = load_skills()

    assert skills_data is not None
    assert len(skills_data.skills) > 0


def test_load_backgrounds():
    backgrounds_data = load_backgrounds()

    assert backgrounds_data is not None
    assert len(backgrounds_data.backgrounds) > 0


def test_races_class_affinities_match_existing_classes():
    races_data = load_races().races
    classes_names = [class_data.name for class_data in load_classes().classes]

    for race in races_data:
        for class_name in race.class_affinities:
            assert class_name in classes_names


def test_races_skills_affinities_match_existing_classes():
    races_data = load_races().races
    skills_names = [skill for skill in load_skills().skills]

    for race in races_data:
        for skill_name in race.skills_affinities:
            assert skill_name in skills_names


def test_create_character_has_required_fields_no_description():
    character = build_character()

    assert character.race
    assert character.character_class
    assert character.skills
    assert character.background
    assert character.description == ""
