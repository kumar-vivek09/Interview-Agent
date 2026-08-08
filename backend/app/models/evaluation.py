from pydantic import BaseModel
from typing import List, Optional

class Evidence(BaseModel):
    evidenceId: str
    questionId: str
    day: int
    type: str # STRENGTH, GAP, MISCONCEPTION, STRONG_REASONING, PRODUCTION_AWARENESS
    dimension: str # e.g. SYSTEM_DESIGN, MCP, RAG
    observation: str
    severity: str # LOW, MEDIUM, HIGH

class Evaluation(BaseModel):
    questionId: str
    correctness: int
    depth: int
    reasoning: int
    production: int
    evidence: List[Evidence]
