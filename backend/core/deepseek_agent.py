"""
DeepSeek Communication Module
Integrates with DeepSeek API to perform natural language understanding and decision making.
"""

import aiohttp
import os
import logging

logger = logging.getLogger(__name__)

class DeepSeekAgent:
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
    DEEPSEEK_BASE_URL = os.getenv('DEEPSEEK_BASE_URL')
    DEEPSEEK_MODEL = os.getenv('DEEPSEEK_MODEL')

    def __init__(self):
        logger.info("DeepSeek agent initialized")

    async def process_natural_language(self, text: str, context: dict) -> dict:
        """Process text command using DeepSeek AI"""
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": self.DEEPSEEK_MODEL,
                "input": text,
                "context": context
            }
            headers = {
                "Authorization": f"Bearer {self.DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            }
            async with session.post(f"{self.DEEPSEEK_BASE_URL}/completions", json=payload, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info("DeepSeek AI response received")
                    return result
                else:
                    error_message = await response.text()
                    logger.error(f"DeepSeek error: {response.status} - {error_message}")
                    raise Exception(f"DeepSeek error: {response.status} - {error_message}")

    def is_ready(self) -> bool:
        """Check if DeepSeek agent is ready"""
        return bool(self.DEEPSEEK_API_KEY and self.DEEPSEEK_BASE_URL)
