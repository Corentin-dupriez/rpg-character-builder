from pydantic import BaseModel, Field
from typing import List


class Race(BaseModel):
    name: str
    weight: int = Field(gt=0)
    traits: List[str]
    description: str


class RaceData(BaseModel):
    races: List[Race]


class ClassInfo(BaseModel):
    name: str
    weight: int = Field(gt=0)
    primary_stat: str
    skills: List[str]
    description: str


class ClassesData(BaseModel):
    classes: List[ClassInfo]


class Skills(BaseModel):
    skills: List[str]


class Background(BaseModel):
    name: str
    skills: List[str]
    description: str


class BackgroundsData(BaseModel):
    backgrounds: List[Background]
