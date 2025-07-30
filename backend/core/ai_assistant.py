"""
KALI AI TERMINAL - AI Assistant Core Module
Advanced Security Terminal AI Intelligence Component
"""

"""
KALI AI TERMINAL - AI Assistant Core Module
Advanced Security Terminal AI Intelligence Component
"""

from .deepseek_agent import UnifiedAIAgent

class KaliAIAssistant:
    def __init__(self):
        """Initialize AI Assistant components"""
        self.agent = UnifiedAIAgent()
    
    async def process_query(self, query: str, context: dict, provider: str = None):
        """Process a generic query using the specified AI provider."""
        # Here, you can enrich the prompt with context if needed
        return await self.agent.process_query(query, provider)

    async def translate_command(self, nl_command: str, provider: str = None) -> str:
        """Translate a natural language command to a shell command."""
        return await self.agent.translate_command(nl_command, provider)

    def is_ready(self, provider: str = None):
        """Check if the AI Assistant is ready."""
        return self.agent.is_ready(provider)
