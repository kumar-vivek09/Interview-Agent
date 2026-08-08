import json
from pathlib import Path
from app.models.curriculum import Curriculum, DayDefinition

class CurriculumRetriever:
    def __init__(self, data_path: str = "data/curriculum.json"):
        self.data_path = Path(data_path)
        self.curriculum = self._load_curriculum()
        self.day_map = {day.day: day for day in self.curriculum.days}

    def _load_curriculum(self) -> Curriculum:
        with open(self.data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return Curriculum(**data)

    def get_day(self, day_number: int) -> DayDefinition:
        return self.day_map.get(day_number)

    def get_all_days(self) -> list[DayDefinition]:
        return self.curriculum.days

    def get_topic_title(self, day_number: int) -> str:
        day = self.get_day(day_number)
        return day.title if day else "Unknown Topic"

curriculum_retriever = CurriculumRetriever()
