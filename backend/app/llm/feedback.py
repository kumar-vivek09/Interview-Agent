from app.llm.client import llm_client
from app.models.feedback import Feedback
import json

class FeedbackLLM:
    def __init__(self):
        with open("prompts/feedback.txt", "r") as f:
            self.system_prompt = f.read()
            
    def generate_feedback(self, state: dict, evidence: list) -> Feedback:
        prompt = f"Candidate Profile:\\n{json.dumps(state.get('candidate_profile'), indent=2)}\\n\\nEvidence Collected:\\n{json.dumps([e.model_dump() for e in evidence], indent=2)}\\n\\nGenerate the final scorecard."
        return llm_client.generate_structured(self.system_prompt, prompt, Feedback)

feedback_generator = FeedbackLLM()
