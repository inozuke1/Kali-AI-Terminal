"""
Firecrawl Tool Integration
Handles interactions with the Firecrawl API for security tasks.
"""

import logging
import os
import aiohttp
from typing import Dict, Any

logger = logging.getLogger(__name__)

class FirecrawlIntegration:
    """Firecrawl API integration for MCP tasks"""

    def __init__(self):
        self.api_key = os.getenv("FIRECRAWL_API_KEY")
        self.base_url = "https://api.firecrawl.com/v1"

    async def invoke_mcp_tool(self, task: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke MCP tool from Firecrawl API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "task": task,
            **config
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/mcp-tool", json=payload, headers=headers) as response:
                response.raise_for_status()
                return await response.json()

    def is_ready(self) -> bool:
        """Check if Firecrawl API is ready"""
        return bool(self.api_key)

