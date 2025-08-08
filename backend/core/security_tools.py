"""
KALI AI TERMINAL - Security Tools Manager
Integration hub for penetration testing tools
"""

import asyncio
import subprocess
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, AsyncGenerator
import logging

logger = logging.getLogger(__name__)

class InteractiveSessionManager:
    """Manages long-running interactive tool sessions"""
    def __init__(self, command: List[str]):
        self.command = command
        self.process = None

    async def start_session(self):
        """Start an interactive session"""
        self.process = await asyncio.create_subprocess_shell(
            " ".join(self.command),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

    async def send_command(self, command: str):
        """Send a command to the interactive session"""
        if self.process and self.process.stdin:
            self.process.stdin.write(f"{command}\n".encode())
            await self.process.stdin.drain()

    async def read_output(self, timeout: int = 5) -> str:
        """Read output from the interactive session"""
        if self.process and self.process.stdout:
            try:
                return await asyncio.wait_for(self.process.stdout.readline(), timeout)
            except asyncio.TimeoutError:
                return ""
        return ""

    async def close_session(self):
        """Close the interactive session"""
        if self.process:
            self.process.terminate()
            await self.process.wait()


class MetasploitController:
    """Metasploit framework controller"""
    
    def __init__(self):
        self.session = None

    async def start_interactive_session(self):
        """Start an interactive msfconsole session"""
        self.session = InteractiveSessionManager(["msfconsole", "-q"])
        await self.session.start_session()

    async def run_command_in_session(self, command: str) -> str:
        """Run a command in the interactive session"""
        if self.session:
            await self.session.send_command(command)
            return await self.session.read_output()
        return "Error: Session not started"

    async def close_session(self):
        """Close the interactive session"""
        if self.session:
            await self.session.close_session()


class SecurityToolManager:
    """Main security tools integration manager"""
    
    def __init__(self):
        self.tools = {
            'metasploit': MetasploitController(),
            # Other tools can be added here
        }
        self.tool_status = {}
        self._initialize_tools()
    
    def _initialize_tools(self):
        """Initialize tool status"""
        for tool_name in self.tools.keys():
            self.tool_status[tool_name] = {
                'available': self._check_tool_availability(tool_name),
                'version': self._get_tool_version(tool_name),
                'last_used': None
            }
    
    def _check_tool_availability(self, tool_name: str) -> bool:
        """Check if a tool is available on the system"""
        try:
            result = subprocess.run(
                ['which', tool_name] if os.name != 'nt' else ['where', tool_name],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except:
            return False
    
    def _get_tool_version(self, tool_name: str) -> str:
        """Get tool version"""
        # Placeholder for version checking logic
        return "unknown"

    def is_ready(self) -> bool:
        """Check if security tools manager is ready"""
        return True

    async def start_interactive_session(self, tool_name: str):
        """Start an interactive session with a tool"""
        if tool_name in self.tools and hasattr(self.tools[tool_name], "start_interactive_session"):
            await self.tools[tool_name].start_interactive_session()

    async def run_command_in_session(self, tool_name: str, command: str) -> str:
        """Run a command in an interactive session"""
        if tool_name in self.tools and hasattr(self.tools[tool_name], "run_command_in_session"):
            return await self.tools[tool_name].run_command_in_session(command)
        return f"Error: Interactive session for {tool_name} not supported"

    async def close_interactive_session(self, tool_name: str):
        """Close an interactive session"""
        if tool_name in self.tools and hasattr(self.tools[tool_name], "close_session"):
            await self.tools[tool_name].close_session()
    
    # Legacy compatibility methods for workflow engine
    async def run_nmap_scan(self, target: str, scan_type: str = "basic") -> Dict:
        """Run nmap scan (legacy compatibility)"""
        try:
            command_map = {
                "basic": f"nmap {target}",
                "syn": f"nmap -sS {target}",
                "service": f"nmap -sV -sC {target}"
            }
            command = command_map.get(scan_type, command_map["basic"])
            
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            return {
                "success": process.returncode == 0,
                "output": stdout.decode('utf-8', errors='ignore'),
                "error": stderr.decode('utf-8', errors='ignore')
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e)
            }
    
    async def run_dirb_scan(self, target: str) -> Dict:
        """Run dirb scan (legacy compatibility)"""
        try:
            command = f"dirb {target}"
            
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            return {
                "success": process.returncode == 0,
                "output": stdout.decode('utf-8', errors='ignore'),
                "error": stderr.decode('utf-8', errors='ignore')
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e)
            }
    
    async def run_metasploit_command(self, command: str) -> Dict:
        """Run metasploit command (legacy compatibility)"""
        try:
            full_command = f"msfconsole -q -x '{command}; exit'"
            
            process = await asyncio.create_subprocess_shell(
                full_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            return {
                "success": process.returncode == 0,
                "output": stdout.decode('utf-8', errors='ignore'),
                "error": stderr.decode('utf-8', errors='ignore')
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e)
            }
    
    async def run_sqlmap_scan(self, target: str) -> Dict:
        """Run sqlmap scan (legacy compatibility)"""
        try:
            command = f"sqlmap -u '{target}' --batch --level=1 --risk=1"
            
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            return {
                "success": process.returncode == 0,
                "output": stdout.decode('utf-8', errors='ignore'),
                "error": stderr.decode('utf-8', errors='ignore')
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e)
            }
    
    async def run_hydra_attack(self, target: str, service: str) -> Dict:
        """Run hydra attack (legacy compatibility)"""
        try:
            command = f"hydra -l admin -p admin {target} {service}"
            
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            return {
                "success": process.returncode == 0,
                "output": stdout.decode('utf-8', errors='ignore'),
                "error": stderr.decode('utf-8', errors='ignore')
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e)
            }
    
    async def get_available_tools(self) -> Dict:
        """Get available tools"""
        return self.tool_status
