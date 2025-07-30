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

class ToolController:
    """Base class for tool controllers"""
    
    def __init__(self, tool_name: str):
        self.tool_name = tool_name
        self.active_processes = {}

    async def run_command(self, command: str) -> Dict:
        """Run a shell command and return the output"""
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            return {
                "success": process.returncode == 0,
                "output": stdout.decode('utf-8', errors='ignore'),
                "error": stderr.decode('utf-8', errors='ignore'),
                "command": command
            }
            
        except Exception as e:
            logger.error(f"Error executing command for {self.tool_name}: {command} - {str(e)}")
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "command": command,
            }

class NmapController(ToolController):
    """Nmap network scanner controller"""
    
    def __init__(self):
        super().__init__("nmap")
    
    async def port_scan(self, target: str, scan_type: str = "basic") -> Dict:
        """Execute port scan"""
        scan_commands = {
            "basic": f"nmap {target}",
            "service": f"nmap -sV {target}",
            "aggressive": f"nmap -A {target}",
            "stealth": f"nmap -sS {target}",
            "all_ports": f"nmap -p- {target}"
        }
        command = scan_commands.get(scan_type, scan_commands["basic"])
        return await self.run_command(command)

class MetasploitController(ToolController):
    """Metasploit framework controller"""
    
    def __init__(self):
        super().__init__("metasploit")
    
    async def search_exploits(self, query: str) -> Dict:
        """Search for exploits"""
        command = f"msfconsole -q -x 'search {query}; exit'"
        return await self.run_command(command)
    
    async def use_exploit(self, exploit_path: str, target: str, port: int) -> Dict:
        """Use an exploit module"""
        commands = [
            f"use {exploit_path}",
            f"set RHOSTS {target}",
            f"set RPORT {port}",
            "show options",
            "exploit"
        ]
        command_str = "; ".join(commands)
        full_command = f"msfconsole -q -x '{command_str}; exit'"
        return await self.run_command(full_command)

class SQLMapController(ToolController):
    """SQLMap SQL injection tool controller"""
    
    def __init__(self):
        super().__init__("sqlmap")
    
    async def test_sql_injection(self, url: str, params: str = None) -> Dict:
        """Test for SQL injection vulnerabilities"""
        command = f"sqlmap -u '{url}'"
        if params:
            command += f" --data '{params}'"
        command += " --batch --level=1 --risk=1"
        return await self.run_command(command)

class HydraController(ToolController):
    """Hydra password cracker controller"""
    
    def __init__(self):
        super().__init__("hydra")
    
    async def brute_force_login(self, target: str, service: str, username_list: str, password_list: str) -> Dict:
        """Execute brute force attack"""
        command = f"hydra -L {username_list} -P {password_list} {target} {service}"
        return await self.run_command(command)

class DirBController(ToolController):
    """DirB directory brute forcer controller"""
    
    def __init__(self):
        super().__init__("dirb")
    
    async def directory_scan(self, url: str, wordlist: str = None) -> Dict:
        """Execute directory brute force scan"""
        command = f"dirb {url}"
        if wordlist:
            command += f" {wordlist}"
        return await self.run_command(command)

class SecurityToolManager:
    """Main security tools integration manager"""
    
    def __init__(self):
        self.tools = {
            'nmap': NmapController(),
            'metasploit': MetasploitController(),
            'sqlmap': SQLMapController(),
            'hydra': HydraController(),
            'dirb': DirBController()
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
                text=True,
                check=True
            )
            return result.returncode == 0
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _get_tool_version(self, tool_name: str) -> str:
        """Get tool version"""
        version_commands = {
            'nmap': 'nmap --version',
            'metasploit': 'msfconsole --version',
            'sqlmap': 'sqlmap --version',
            'hydra': 'hydra -h',
            'dirb': 'dirb'
        }
        
        command = version_commands.get(tool_name)
        if not command:
            return "Unknown"
            
        try:
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                timeout=5,
                check=True
            )
            return result.stdout.split('\n')[0]
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
            logger.warning(f"Could not get version for {tool_name}: {e}")
            return "Unknown"
    
    def is_ready(self) -> bool:
        """Check if security tools manager is ready"""
        return True
    
    async def get_available_tools(self) -> Dict:
        """Get list of available tools"""
        return {
            'tools': self.tool_status,
            'timestamp': datetime.now().isoformat()
        }
    
    async def execute_tool_operation(self, tool_name: str, operation: str, params: Dict) -> Dict:
        """Execute a tool operation"""
        if tool_name not in self.tools:
            return {
                'success': False,
                'error': f'Tool {tool_name} not available',
                'tool': tool_name,
                'operation': operation
            }
        
        tool = self.tools[tool_name]
        
        try:
            self.tool_status[tool_name]['last_used'] = datetime.now().isoformat()
            
            operation_method = getattr(tool, operation, None)
            if operation_method and callable(operation_method):
                return await operation_method(**params)

            return {
                'success': False,
                'error': f'Operation {operation} not supported for {tool_name}',
                'tool': tool_name,
                'operation': operation
            }
            
        except Exception as e:
            logger.error(f"Tool operation error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'tool': tool_name,
                'operation': operation
            }
    
    async def get_tool_help(self, tool_name: str) -> Dict:
        """Get help information for a tool"""
        help_info = {
            'nmap': {
                'description': 'Network discovery and security auditing',
                'operations': ['port_scan'],
                'examples': [
                    {'operation': 'port_scan', 'params': {'target': '192.168.1.1', 'scan_type': 'basic'}}
                ]
            },
            'metasploit': {
                'description': 'Penetration testing framework',
                'operations': ['search_exploits', 'use_exploit'],
                'examples': [
                    {'operation': 'search_exploits', 'params': {'query': 'windows smb'}},
                    {'operation': 'use_exploit', 'params': {'exploit_path': 'windows/smb/ms08_067_netapi', 'target': '192.168.1.100', 'port': 445}}
                ]
            },
            'sqlmap': {
                'description': 'Automatic SQL injection tool',
                'operations': ['test_injection'],
                'examples': [
                    {'operation': 'test_injection', 'params': {'url': 'http://example.com/login.php', 'params': 'username=admin&password=test'}}
                ]
            },
            'hydra': {
                'description': 'Password cracking tool',
                'operations': ['brute_force'],
                'examples': [
                    {'operation': 'brute_force', 'params': {'target': '192.168.1.100', 'service': 'ssh', 'username_list': '/usr/share/wordlists/usernames.txt', 'password_list': '/usr/share/wordlists/passwords.txt'}}
                ]
            },
            'dirb': {
                'description': 'Web directory brute forcer',
                'operations': ['directory_scan'],
                'examples': [
                    {'operation': 'directory_scan', 'params': {'url': 'http://example.com', 'wordlist': '/usr/share/dirb/wordlists/common.txt'}}
                ]
            }
        }
        
        if tool_name in help_info:
            return {
                'success': True,
                'tool': tool_name,
                'help': help_info[tool_name]
            }
        
        return {
            'success': False,
            'error': f'No help available for {tool_name}'
        }
