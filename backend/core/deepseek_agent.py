"""
DeepSeek Communication Module
Integrates with DeepSeek API to perform natural language understanding and decision making.
"""

import aiohttp
import os
import logging

logger = logging.getLogger(__name__)

class DeepSeekAgent:
    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        self.base_url = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com/v1')
        self.model = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')
        logger.info("DeepSeek agent initialized")

    async def process_natural_language(self, text: str, context: dict) -> dict:
        """Process text command using DeepSeek AI"""
        if not self.is_ready():
            return {"error": "DeepSeek API key not configured"}
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant in a cybersecurity terminal."},
                {"role": "user", "content": text}
            ],
            "stream": False
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(f"{self.base_url}/chat/completions", json=payload, headers=headers) as response:
                    response.raise_for_status()
                    result = await response.json()
                    logger.info("DeepSeek AI response received")
                    return result
            except aiohttp.ClientError as e:
                logger.error(f"DeepSeek API request failed: {e}")
                return {"error": f"API request failed: {e}"}

    def is_ready(self) -> bool:
        """Check if DeepSeek agent is ready"""
        return bool(self.api_key)
