from app.llm.client import llm_client
from app.models.evaluation import Evaluation
import json

class EvaluatorLLM:
    def __init__(self):
        with open("prompts/evaluator.txt", "r") as f:
            self.system_prompt = f.read()
            
    def evaluate(self, answer: str, context: dict) -> Evaluation:
        prompt = f"Context:\\n{json.dumps(context, indent=2)}\\n\\nCandidate Answer:\\n{answer}\\n\\nEvaluate the answer and provide structured evidence."
        return llm_client.generate_structured(self.system_prompt, prompt, Evaluation)

evaluator = EvaluatorLLM()
