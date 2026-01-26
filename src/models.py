from pydantic import BaseModel, Field
from typing import List


class Race(BaseModel):
    name: str
    weight: int = Field(gt=0)
    traits: List[str]
    class_affinities: dict
    skills_affinities: dict
    description: str


class RaceData(BaseModel):
    races: List[Race]


class ClassInfo(BaseModel):
    name: str
    weight: int = Field(gt=0)
    primary_stat: str
    skills: dict
    description: str


class ClassesData(BaseModel):
    classes: List[ClassInfo]


class Skills(BaseModel):
    skills: List[str]


class Background(BaseModel):
    name: str
    personality_traits: list[str]
    weight: float
    class_affinities: dict
    skill_affinities: dict
    personality_traits: list[str]
    flaws: list[str]
    motivations: list[str]
    notable_events: list[str]


class BackgroundsData(BaseModel):
    backgrounds: List[Background]


class Character(BaseModel):
    race: Race
    character_class: ClassInfo
    skills: List[str]
    background: Background
    description: str
