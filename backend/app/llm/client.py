import os
import json
import re
from pydantic import BaseModel
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        api_key = os.getenv("HF_TOKEN")
        self.client = InferenceClient(api_key=api_key)
        self.model = "meta-llama/Llama-3.3-70B-Instruct"

    def _extract_json(self, text: str) -> dict:
        """Robustly extracts JSON from LLM output, handling markdown blocks."""
        # Try to find a JSON block
        match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
        if match:
            text = match.group(1)
        
        # Clean up any remaining whitespace/newlines
        text = text.strip()
        
        # Find first { and last }
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            text = text[start:end+1]
            
        return json.loads(text)

    def generate_structured(self, system_instruction: str, prompt: str, response_schema: type[BaseModel]) -> BaseModel:
        # Ask explicitly for JSON matching the schema
        schema_json = json.dumps(response_schema.model_json_schema(), indent=2)
        system_with_schema = (
            f"{system_instruction}\n\n"
            f"IMPORTANT: You must respond ONLY with a valid JSON object. "
            f"The JSON object must perfectly match this JSON Schema:\n{schema_json}"
        )
        
        messages = [
            {"role": "system", "content": system_with_schema},
            {"role": "user", "content": prompt}
        ]
        
        response = self.client.chat_completion(
            model=self.model,
            messages=messages,
            max_tokens=2048,
            temperature=0.7,
        )
        
        content = response.choices[0].message.content
        parsed_dict = self._extract_json(content)
        return response_schema.model_validate(parsed_dict)

    def generate_text(self, system_instruction: str, prompt: str) -> str:
        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ]
        
        response = self.client.chat_completion(
            model=self.model,
            messages=messages,
            max_tokens=2048,
            temperature=0.7
        )
        
        return response.choices[0].message.content

llm_client = LLMClient()
