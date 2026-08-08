import json
from pathlib import Path
from app.models.candidate import Candidate, MissionRecord
from app.models.interview import CandidateProfile

class MissionState:
    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    NOT_ATTEMPTED = "NOT_ATTEMPTED"

class CandidateProfiler:
    def __init__(self, data_path: str = "data/candidates.json"):
        self.data_path = Path(data_path)
        self.candidates_data = self._load_data()
        self.candidates_map = {c.member.id: c for c in self.candidates_data}

    def _load_data(self) -> list[Candidate]:
        with open(self.data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Candidate(**c) for c in data.get("candidates", [])]

    def get_candidate(self, candidate_id: str) -> Candidate:
        return self.candidates_map.get(candidate_id)

    def determine_mission_state(self, mission: MissionRecord) -> str:
        if mission.skipped:
            return MissionState.SKIPPED
        if mission.passed is True:
            return MissionState.PASSED
        if mission.passed is False:
            return MissionState.FAILED
        return MissionState.NOT_ATTEMPTED

    def get_difficulty_badge(self, experience: int, signals: dict) -> str:
        if experience >= 8:
            return "SENIOR"
        elif experience >= 4:
            return "ADVANCED"
        elif experience >= 2:
            return "INTERMEDIATE"
        else:
            return "BEGINNER"

    def analyze_candidate(self, candidate: Candidate) -> dict:
        """
        Builds the deterministic profile.
        """
        strengths = []
        weaknesses = []
        skipped_topics = []
        
        for m in candidate.missions:
            state = self.determine_mission_state(m)
            if state == MissionState.PASSED:
                if m.attempts == 1:
                    strengths.append(m.day)
            elif state == MissionState.FAILED:
                weaknesses.append(m.day)
            elif state == MissionState.SKIPPED:
                skipped_topics.append(m.day)
                
            # If passed but took many attempts, it's an area needing probing
            if state == MissionState.PASSED and m.attempts and m.attempts >= 4:
                weaknesses.append(m.day)

        badge = self.get_difficulty_badge(candidate.member.yearsExperience, candidate.signals.model_dump())
        
        return {
            "candidate_id": candidate.member.id,
            "role": candidate.member.jobRole,
            "experience": candidate.member.yearsExperience,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "skipped": skipped_topics,
            "difficulty": badge
        }

    def get_candidate_profile(self, candidate_id: str) -> CandidateProfile:
        candidate = self.get_candidate(candidate_id)
        if not candidate:
            raise ValueError(f"Candidate {candidate_id} not found.")
            
        analysis = self.analyze_candidate(candidate)
        return CandidateProfile(
            role=analysis["role"],
            experience=analysis["experience"],
            strengths=[str(d) for d in analysis["strengths"]],
            gaps=[str(d) for d in analysis["weaknesses"]],
            difficulty=analysis["difficulty"]
        )

candidate_profiler = CandidateProfiler()
