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

logger = logging.getLogger(__name__)

class SecurityValidator:
    """Validates command security"""
    
    DANGEROUS_COMMANDS = [
        'rm -rf /', 'del /f /s /q', 'format', 'fdisk', 'dd if=', 'shutdown', 'reboot',
        'powershell.exe', 'wget', 'curl', ':(){ :|: & };:','mkfs', 'curl | sh'
    ]
    
    ALLOWED_SECURITY_TOOLS = [
        'nmap', 'ncat', 'netstat', 'ss', 'ping', 'traceroute', 'dig', 'nslookup',
        'sqlmap', 'dirb', 'gobuster', 'nikto', 'hydra', 'john', 'hashcat',
        'metasploit', 'msfconsole', 'msfvenom', 'aircrack-ng', 'airodump-ng',
        'burpsuite', 'zaproxy', 'wireshark', 'tshark', 'tcpdump'
    ]
    
    def __init__(self):
        self.command_history = []
    
    async def validate_command(self, command: str) -> Dict:
        """Validate command for security risks"""
        danger_level = 0
        warnings = []
        is_allowed = True
        
        # Check for dangerous commands
        for dangerous in self.DANGEROUS_COMMANDS:
            if dangerous in command.lower():
                danger_level = 10
                warnings.append(f"Dangerous command detected: {dangerous}")
                is_allowed = False
                break
        
        # Check if it's a security tool
        command_parts = command.split()
        if command_parts:
            tool = command_parts[0]
            if tool in self.ALLOWED_SECURITY_TOOLS:
                danger_level = max(danger_level, 2)  # Security tools have minimal risk
                warnings.append(f"Security tool: {tool}")
            elif tool not in ['ls', 'cat', 'grep', 'ps', 'top', 'htop', 'history']:
                danger_level = max(danger_level, 5)  # Unknown commands have medium risk
                warnings.append(f"Unknown command: {tool}")
        
        return {
            'danger_level': danger_level,
            'warnings': warnings,
            'is_allowed': is_allowed,
            'timestamp': datetime.now().isoformat()
        }

class CommandPredictor:
    """Predicts likely next commands based on context"""
    
    COMMAND_PATTERNS = {
        'nmap': ['nmap -sV', 'nmap -sC', 'nmap -A', 'nmap -p-'],
        'scan': ['nmap', 'nikto', 'dirb', 'gobuster'],
        'exploit': ['msfconsole', 'sqlmap', 'hydra'],
        'network': ['netstat', 'ss', 'ping', 'traceroute'],
        'enumeration': ['enum4linux', 'smbclient', 'showmount']
    }
    
    def __init__(self):
        self.context_history = []
    
    async def predict_next_commands(self, current_command: str, context: Dict) -> List[str]:
        """Predict likely next commands"""
        predictions = []
        
        # Simple pattern matching
        for pattern, commands in self.COMMAND_PATTERNS.items():
            if pattern in current_command.lower():
                predictions.extend(commands[:3])  # Top 3 predictions
        
        # Remove duplicates and current command
        predictions = list(set(predictions))
        if current_command in predictions:
            predictions.remove(current_command)
        
        return predictions[:5]  # Return top 5 predictions

class OutputAnalyzer:
    """Analyzes command output for insights"""
    
    def __init__(self):
        self.analysis_patterns = {
            'open_ports': r'(\d+/tcp\s+open)',
            'vulnerabilities': r'(VULNERABLE|CVE-\d{4}-\d{4,})',
            'credentials': r'(password|username|login)',
            'network_info': r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        }
    
    async def analyze_output(self, output: str, command: str) -> Dict:
        """Analyze command output for security insights"""
        insights = {
            'findings': [],
            'recommendations': [],
            'risk_level': 'low',
            'metadata': {
                'command': command,
                'output_length': len(output),
                'timestamp': datetime.now().isoformat()
            }
        }
        
        # Simple analysis - look for common patterns
        if 'open' in output.lower() and 'port' in output.lower():
            insights['findings'].append('Open ports detected')
            insights['recommendations'].append('Investigate open services')
            insights['risk_level'] = 'medium'
        
        if 'vulnerable' in output.lower():
            insights['findings'].append('Potential vulnerabilities found')
            insights['recommendations'].append('Perform detailed vulnerability assessment')
            insights['risk_level'] = 'high'
        
        if len(output) > 10000:
            insights['findings'].append('Large output detected')
            insights['recommendations'].append('Consider filtering output')
        
        return insights

class IntelligentCommandEngine:
    """AI-enhanced command processing engine"""
    
    def __init__(self):
        self.security_validator = SecurityValidator()
        self.command_predictor = CommandPredictor()
        self.output_analyzer = OutputAnalyzer()
        self.active_processes = {}
        self.command_history = []
    
    def is_ready(self) -> bool:
        """Check if command engine is ready"""
        return True
    
    async def process_command(self, command: str, context: Dict = None) -> Dict:
        """Process command with AI enhancement"""
        if context is None:
            context = {}
        
        logger.info(f"Processing command: {command}")
        
        try:
            # Validate security
            security_check = await self.security_validator.validate_command(command)
            
            if not security_check['is_allowed']:
                return {
                    'success': False,
                    'output': f"Command blocked for security: {', '.join(security_check['warnings'])}",
                    'error': 'Security violation',
                    'security_check': security_check,
                    'predictions': [],
                    'insights': {}
                }
            
            # Execute command
            result = await self._execute_command_async(command)
            
            # Predict next commands
            predictions = await self.command_predictor.predict_next_commands(command, context)
            
            # Analyze output
            insights = await self.output_analyzer.analyze_output(result['output'], command)
            
            # Store in history
            self.command_history.append({
                'command': command,
                'timestamp': datetime.now().isoformat(),
                'success': result['success'],
                'context': context
            })
            
            return {
                'success': result['success'],
                'output': result['output'],
                'error': result.get('error', ''),
                'security_check': security_check,
                'predictions': predictions,
                'insights': insights,
                'execution_time': result.get('execution_time', 0)
            }
            
        except Exception as e:
            logger.error(f"Command processing error: {str(e)}")
            return {
                'success': False,
                'output': '',
                'error': str(e),
                'security_check': {'danger_level': 0, 'warnings': [], 'is_allowed': True},
                'predictions': [],
                'insights': {}
            }
    
    async def _execute_command_async(self, command: str) -> Dict:
        """Execute command asynchronously"""
        start_time = datetime.now()
        
        try:
            # Handle Windows vs Linux commands
            if os.name == 'nt':  # Windows
                shell_cmd = ['cmd', '/c', command]
            else:  # Linux/Unix
                shell_cmd = ['bash', '-c', command]
            
            # Execute with timeout
            process = await asyncio.create_subprocess_exec(
                *shell_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                limit=1024*1024  # 1MB limit
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), 
                    timeout=30.0  # 30 second timeout
                )
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                output = stdout.decode('utf-8', errors='ignore')
                error = stderr.decode('utf-8', errors='ignore')
                
                return {
                    'success': process.returncode == 0,
                    'output': output,
                    'error': error,
                    'return_code': process.returncode,
                    'execution_time': execution_time
                }
                
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                return {
                    'success': False,
                    'output': '',
                    'error': 'Command timed out after 30 seconds',
                    'return_code': -1,
                    'execution_time': 30.0
                }
                
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return {
                'success': False,
                'output': '',
                'error': str(e),
                'return_code': -1,
                'execution_time': execution_time
            }
    
    async def get_command_history(self, limit: int = 100) -> List[Dict]:
        """Get command history"""
        return self.command_history[-limit:]
    
    async def get_active_processes(self) -> List[Dict]:
        """Get list of active processes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                proc_info = proc.info
                proc_info['cpu_percent'] = proc.cpu_percent()
                processes.append(proc_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:20]
    
    async def kill_process(self, pid: int) -> bool:
        """Kill a process by PID"""
        try:
            process = psutil.Process(pid)
            process.terminate()
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False
