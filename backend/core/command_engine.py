"""
KALI AI TERMINAL - Intelligent Command Engine
Advanced command processing with AI enhancement
"""

import asyncio
import subprocess
import os
import json
from datetime import datetime
from typing import Dict, List, Optional, AsyncGenerator
import psutil
import logging
import re

from .ai_assistant import KaliAIAssistant
from .security_tools import SecurityToolManager

logger = logging.getLogger(__name__)

class SecurityValidator:
    """Validates command security"""
    
    DANGEROUS_PATTERNS = [
        r'rm\s+-rf\s+/',
        r'dd\s+if=/dev/zero',
        r':\(\)\{\s*:.*\|.*:&\s*\};:',
        r'mkfs\.',
        r'shutdown\s+-h\s+now',
    ]
    
    def __init__(self):
        self.command_history = []
    
    async def validate_command(self, command: str) -> Dict:
        """Validate command for security risks"""
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, command):
                return {
                    'is_allowed': False,
                    'warning': f"Dangerous command pattern detected: {pattern}"
                }
        return {'is_allowed': True, 'warning': None}

class CommandPredictor:
    """Predicts likely next commands based on context"""
    
    COMMAND_CHAINS = {
        'nmap': ['gobuster', 'nikto', 'msfconsole'],
        'gobuster': ['nmap', 'whatweb'],
    }
    
    def __init__(self, ai_assistant: KaliAIAssistant):
        self.ai_assistant = ai_assistant
    
    async def predict_next_commands(self, current_command: str, context: Dict) -> List[str]:
        """Predict likely next commands"""
        base_predictions = self.COMMAND_CHAINS.get(current_command.split()[0], [])
        
        ai_prompt = f"Given the last command ''{current_command}'' and the context, suggest the next most likely pentesting commands."
        ai_response = await self.ai_assistant.process_query(ai_prompt, context)
        
        ai_predictions = ai_response.get('response', [])
        
        return list(set(base_predictions + ai_predictions))[:5]

class OutputAnalyzer:
    """Analyzes command output for insights"""
    
    def __init__(self, ai_assistant: KaliAIAssistant):
        self.ai_assistant = ai_assistant

    async def analyze_output(self, output: str, command: str) -> Dict:
        """Analyze command output for security insights"""
        ai_prompt = f"Analyze the output of the command ''{command}'' and provide a summary of findings and recommendations."
        return await self.ai_assistant.process_query(ai_prompt, {"command_output": output})

class IntelligentCommandEngine:
    """AI-enhanced command processing engine"""
    
    def __init__(self, ai_assistant: KaliAIAssistant, security_tools: SecurityToolManager):
        self.ai_assistant = ai_assistant
        self.security_tools = security_tools
        self.security_validator = SecurityValidator()
        self.command_predictor = CommandPredictor(ai_assistant)
        self.output_analyzer = OutputAnalyzer(ai_assistant)
        self.command_history = []
    
    def is_ready(self) -> bool:
        """Check if command engine is ready"""
        return True
    
    async def process_command(self, command: str, context: Dict = None) -> Dict:
        """Process command with AI enhancement"""
        if context is None:
            context = {}
        
        logger.info(f"Processing command: {command}")
        
        security_check = await self.security_validator.validate_command(command)
        if not security_check['is_allowed']:
            return {'success': False, 'error': security_check['warning']}

        is_tool_command = command.split()[0] in self.security_tools.tools
        if is_tool_command:
            # Simplified for brevity, assuming operation maps to method name
            tool_name, operation, *args = command.split()
            params = self._parse_args(args)
            result = await self.security_tools.execute_tool_operation(tool_name, operation, params)
        else:
            result = await self._execute_shell_command(command)
        
        insights = await self.output_analyzer.analyze_output(result['output'], command)
        predictions = await self.command_predictor.predict_next_commands(command, context)
        
        self.command_history.append({
            'command': command,
            'timestamp': datetime.now().isoformat(),
            'success': result['success'],
        })
        
        return {
            **result,
            'insights': insights,
            'predictions': predictions
        }

    async def process_natural_language_command(self, nl_command: str, context: dict) -> Dict:
        """Translate and execute a natural language command."""
        prompt = f"Translate the following natural language command for a Kali Linux terminal into a precise shell command: ''{nl_command}''." 
        response = await self.ai_assistant.process_query(prompt, context)
        
        shell_command = response.get('response', '').strip()
        if not shell_command:
            return {'success': False, 'error': 'AI could not translate the command.'}
            
        return await self.process_command(shell_command, context)

    def _parse_args(self, args: list) -> dict:
        """A simple parser for command line arguments into a dictionary."""
        params = {}
        for arg in args:
            if '=' in arg:
                key, value = arg.split('=', 1)
                params[key.strip('--')] = value
        return params

    async def _execute_shell_command(self, command: str) -> Dict:
        """Execute a generic shell command"""
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            return {
                'success': process.returncode == 0,
                'output': stdout.decode(),
                'error': stderr.decode()
            }
        except Exception as e:
            return {'success': False, 'error': str(e), 'output': ''}
