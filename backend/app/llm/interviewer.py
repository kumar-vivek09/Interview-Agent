from app.llm.client import llm_client
from pydantic import BaseModel
import json

class InterviewResponse(BaseModel):
    reply: str

class InterviewerLLM:
    def __init__(self):
        with open("prompts/interviewer.txt", "r") as f:
            self.system_prompt = f.read()
            
    def generate_question(self, context: dict) -> str:
        prompt = f"Context:\\n{json.dumps(context, indent=2)}\\n\\nGenerate the next interviewer response."
        
        # We ask for structured output to ensure we just get the reply string cleanly
        res = llm_client.generate_structured(self.system_prompt, prompt, InterviewResponse)
        return res.reply

interviewer = InterviewerLLM()
