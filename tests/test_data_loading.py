from generator import load_races, load_classes, load_skills, load_backgrounds


def test_load_races():
    races_data = load_races()

    assert races_data is not None
    assert len(races_data.races) > 0


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
