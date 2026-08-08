from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime

class CandidateProfile(BaseModel):
    role: str
    experience: int
    strengths: List[str] = []
    gaps: List[str] = []
    difficulty: str

class TopicRecord(BaseModel):
    day: int
    title: str

class InterviewState(BaseModel):
    session_id: str
    candidate_id: str
    candidate_profile: CandidateProfile
    phase: str = "OPENING"
    turn_count: int = 0
    question_count: int = 0
    primary_question_count: int = 0
    follow_up_count: int = 0
    covered_days: List[int] = []
    required_days: List[int] = []
    current_topic: Optional[TopicRecord] = None
    current_question_id: Optional[str] = None
    difficulty: str = "INTERMEDIATE"
    probe_type: Optional[str] = None
    transcript: List[Dict[str, Any]] = [] # list of {"role": "...", "content": "..."}
    evaluations: List[Any] = [] # list of Evidence structures
    evidence: List[Any] = []
    started_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
