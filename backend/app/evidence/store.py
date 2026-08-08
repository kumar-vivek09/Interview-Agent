from typing import List, Dict, Optional
from app.models.evaluation import Evidence

class EvidenceStore:
    def __init__(self):
        self.session_evidence: Dict[str, List[Evidence]] = {}
        
    def add_evidence(self, session_id: str, evidence: List[Evidence]):
        if session_id not in self.session_evidence:
            self.session_evidence[session_id] = []
        self.session_evidence[session_id].extend(evidence)
        
    def get_evidence(self, session_id: str) -> List[Evidence]:
        return self.session_evidence.get(session_id, [])

evidence_store = EvidenceStore()
