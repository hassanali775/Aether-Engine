import json
import httpx
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class LocalLLMService:
    """
    On-Premise Inference Engine.
    Handles communication with local Ollama runtimes to generate strictly structured task trees.
    """
    def __init__(self, ollama_url: str = "http://127.0.0.1:11434", model_name: str = "phi3"):
        self.client = httpx.AsyncClient(base_url=ollama_url, timeout=45.0)
        self.model_name = model_name

    async def decompose_instruction(self, raw_instruction: str, available_tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Forces the local SLM to parse an abstract human request into a strict JSON execution schema.
        """
        prompt = f"""
        You are the core routing brain of an autonomous multi-agent mesh. Your job is to translate a raw human instruction into a structured task execution payload.
        You must choose from the following list of available system tools:
        {json.dumps(available_tools, indent=2)}

        Target Human Instruction: "{raw_instruction}"

        You must respond strictly with a single valid JSON object matching this schema, with no markdown code block wrappers, conversational text, or explanations:
        {{
          "tool_to_use": "NAME_OF_TOOL",
          "args": {{"parameter_name": "extracted_value"}},
          "confidence_score": 1.0
        }}
        """

        try:
            response = await self.client.post("/api/generate", json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.0  # Eradicate random hallucinations
                }
            })
            
            raw_output = response.json().get("response", "").strip()
            
            # Clean off any unexpected markdown artifacts
            if raw_output.startswith("```json"):
                raw_output = raw_output.split("```json")[1].split("```")[0].strip()
            elif raw_output.startswith("```"):
                raw_output = raw_output.split("```")[1].split("```")[0].strip()

            return json.loads(raw_output)

        except Exception as e:
            logger.error(f"[LLM ENGINE ERROR] Local inference task parsing failed: {str(e)}")
            # Fail-safe gracefully back to system baseline instead of throwing an unhandled exception
            return {"tool_to_use": "FALLBACK_DIAGNOSTIC", "args": {"raw_input": raw_instruction}, "confidence_score": 0.0}