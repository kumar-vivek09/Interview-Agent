from pydantic import BaseModel
from typing import List

class ModuleDefinition(BaseModel):
    n: int
    title: str
    days: List[int]

class DayDefinition(BaseModel):
    day: int
    title: str
    type: str
    tools: List[str]
    objectives: List[str]

class Curriculum(BaseModel):
    cohort: str
    modules: List[ModuleDefinition]
    days: List[DayDefinition]
