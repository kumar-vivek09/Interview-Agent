from app.models.evaluation import Evaluation, Evidence
from app.models.interview import InterviewState
import uuid

class EvidenceBuilder:
    def build_from_evaluation(self, eval_data: Evaluation, state: InterviewState) -> list[Evidence]:
        """
        Converts the evaluation from the LLM into final evidence objects.
        """
        # Currently the LLM returns the Evidence array directly inside Evaluation.
        # This builder just ensures they have IDs and are properly formatted.
        results = []
        for ev in eval_data.evidence:
            ev.evidenceId = f"EV-{uuid.uuid4().hex[:8]}"
            if not ev.questionId:
                ev.questionId = state.current_question_id or "UNKNOWN"
            if not ev.day and state.current_topic:
                ev.day = state.current_topic.day
            results.append(ev)
        return results

evidence_builder = EvidenceBuilder()
