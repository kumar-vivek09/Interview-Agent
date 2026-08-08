from typing import List

class CoverageMatrix:
    def __init__(self, required_days: List[int], covered_days: List[int] = None):
        self.required_days = set(required_days)
        self.covered_days = set(covered_days) if covered_days else set()

    def mark_covered(self, day: int):
        self.covered_days.add(day)

    def get_remaining(self) -> List[int]:
        return list(self.required_days - self.covered_days)

    def has_sufficient_coverage(self, min_days: int) -> bool:
        return len(self.covered_days) >= min_days

    def to_dict(self):
        return {
            "requiredDays": list(self.required_days),
            "coveredDays": list(self.covered_days),
            "remaining": self.get_remaining()
        }
