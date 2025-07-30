"""
KALI AI TERMINAL - Unified AI Interface
Provides a flexible interface to multiple AI providers for natural language processing.
"""

import aiohttp
import os
import logging
from typing import Dict, Any, Protocol

logger = logging.getLogger(__name__)

class AIProvider(Protocol):
    """Interface for AI providers"""
    async def process_query(self, prompt: str, config: Dict[str, Any]) -> Dict[str, Any]:
        ...

class DeepSeekProvider:
    """AI provider for DeepSeek API"""
    async def process_query(self, prompt: str, config: Dict[str, Any]) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {config['api_key']}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": config.get('model', 'deepseek-chat'),
            "messages": [
                {"role": "system", "content": "You are a helpful assistant in a cybersecurity terminal."},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{config.get('base_url', 'https://api.deepseek.com/v1')}/chat/completions", json=payload, headers=headers) as response:
                response.raise_for_status()
                return await response.json()

class PromptEngine:
    """Generates tailored prompts for different tasks."""
    def get_command_translation_prompt(self, nl_command: str) -> str:
        return f"Translate this natural language command to a Kali Linux shell command: '{nl_command}'. Only respond with the command, no explanations."

    def get_output_analysis_prompt(self, command: str, output: str) -> str:
        return f"Analyze the output of the command '{command}' for security insights. Extract key findings like open ports, vulnerabilities, or services. Output should be in JSON format with keys: findings, recommendations, risk_level. Output: {output}"

class UnifiedAIAgent:
    """A unified agent to interact with various AI models."""
    def __init__(self):
        self.providers = {
            "deepseek": DeepSeekProvider(),
        }
        self.prompt_engine = PromptEngine()
        self.default_provider = os.getenv("DEFAULT_AI_PROVIDER", "deepseek")
        self.configs = {
            "deepseek": {
                "api_key": os.getenv("DEEPSEEK_API_KEY"),
                "base_url": os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
                "model": os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
            }
        }
        logger.info("Unified AI Agent initialized")

    def is_ready(self, provider: str = None) -> bool:
        provider = provider or self.default_provider
        return bool(self.configs.get(provider, {}).get('api_key'))

    async def process_query(self, prompt: str, provider: str = None) -> Dict[str, Any]:
        provider = provider or self.default_provider
        if not self.is_ready(provider):
            return {"error": f"{provider.capitalize()} API key not configured."}
        
        try:
            return await self.providers[provider].process_query(prompt, self.configs[provider])
        except Exception as e:
            logger.error(f"Error with {provider} API: {e}")
            return {"error": str(e)}

    async def translate_command(self, nl_command: str, provider: str = None) -> str:
        prompt = self.prompt_engine.get_command_translation_prompt(nl_command)
        response = await self.process_query(prompt, provider)
        # Extract the command from the response
        if 'choices' in response and response['choices']:
            return response['choices'][0].get('message', {}).get('content', '').strip()
        elif 'error' in response:
            return f"Error: {response['error']}"
        return "Unable to translate command"

    async def analyze_output(self, command: str, output: str, provider: str = None) -> Dict[str, Any]:
        prompt = self.prompt_engine.get_output_analysis_prompt(command, output)
        response = await self.process_query(prompt, provider)
        # Extract analysis from the response
        if 'choices' in response and response['choices']:
            content = response['choices'][0].get('message', {}).get('content', '')
            try:
                import json
                return json.loads(content)
            except:
                return {"analysis": content, "findings": [], "recommendations": [], "risk_level": "unknown"}
        return {"error": "Unable to analyze output"}
