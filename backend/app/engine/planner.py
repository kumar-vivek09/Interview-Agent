from app.models.interview import InterviewState
from app.engine.policy import InterviewPolicy
from app.engine.coverage import CoverageMatrix
from app.engine.question_engine import decision_engine
from app.engine.probes import QuestionType

class InterviewPlanner:
    def __init__(self):
        pass
        
    def determine_next_action(self, state: InterviewState) -> dict:
        """
        Evaluates current state against policy and decides the next structural step.
        Returns the action dict which includes whether we should finish or continue.
        """
        coverage = CoverageMatrix(state.required_days, state.covered_days)
        
        # Check completion conditions
        has_min_questions = state.question_count >= InterviewPolicy.MIN_QUESTIONS
        has_min_days = coverage.has_sufficient_coverage(InterviewPolicy.MIN_CURRICULUM_DAYS)
        hit_max_questions = state.question_count >= InterviewPolicy.MAX_QUESTIONS
        
        # In a real scenario we might ask LLM if natural conclusion reached, 
        # but here we'll use a deterministic check + max constraint.
        if (has_min_questions and has_min_days) or hit_max_questions:
            # We are eligible to finish. Let's finish for simplicity if we hit 10 questions or more, 
            # or if we have covered all required days.
            if state.question_count >= 10 or not coverage.get_remaining():
                return {"action": "FINISH", "reason": "Met completion criteria."}

        # Otherwise, we ask the decision engine what to do next
        decision = decision_engine.decide(state)
        
        return {
            "action": "CONTINUE",
            "decision": decision
        }

planner = InterviewPlanner()
