from pydantic import BaseModel
from typing import List

class QuestionContext(BaseModel):
    candidate_role: str
    candidate_experience: int
    phase: str
    question_count: int
    covered_days: List[int]
    remaining_required_days: List[int]
    current_topic_day: int
    current_topic_title: str
    previous_answers: List[dict] # list of dict containing 'question', 'answer', 'evaluation'
    probe_type: str
    difficulty: str
