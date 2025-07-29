"""
KALI AI TERMINAL - Advanced Workflow Engine
Implements AI-driven thinking → planning → execution pipeline for security operations
"""

import asyncio
import json
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass, asdict

from .deepseek_agent import DeepSeekAgent
from .command_engine import IntelligentCommandEngine
from .security_tools import SecurityToolManager
from .vulnerability_scanner import VulnerabilityScanner
from .network_monitor import NetworkMonitor

logger = logging.getLogger(__name__)

class WorkflowState(Enum):
    IDLE = "idle"
    THINKING = "thinking" 
    PLANNING = "planning"
    EXECUTING = "executing"
    COMPLETED = "completed"
    ERROR = "error"

class OperationType(Enum):
    RECONNAISSANCE = "reconnaissance"
    VULNERABILITY_SCAN = "vulnerability_scan"
    EXPLOITATION = "exploitation"
    POST_EXPLOITATION = "post_exploitation"
    REPORTING = "reporting"
    NETWORK_ANALYSIS = "network_analysis"
    TOOL_EXECUTION = "tool_execution"

@dataclass
class WorkflowStep:
    id: str
    name: str
    operation_type: OperationType
    command: str
    parameters: Dict[str, Any]
    dependencies: List[str]
    estimated_duration: int  # seconds
    risk_level: str  # low, medium, high, critical
    description: str

@dataclass
class WorkflowPlan:
    id: str
    title: str
    description: str
    target: str
    steps: List[WorkflowStep]
    estimated_total_time: int
    risk_assessment: str
    created_at: str

@dataclass
class ExecutionResult:
    step_id: str
    success: bool  
    output: str
    error_message: Optional[str]
    execution_time: float
    artifacts: List[str]  # Files, reports generated

class AdvancedWorkflowEngine:
    """
    Advanced AI-powered workflow engine for penetration testing operations
    Implements thinking → planning → execution pipeline
    """
    
    def __init__(self):
        self.deepseek_agent = DeepSeekAgent()
        self.command_engine = IntelligentCommandEngine()
        self.security_tools = SecurityToolManager()
        self.vuln_scanner = VulnerabilityScanner()
        self.network_monitor = NetworkMonitor()
        
        self.state = WorkflowState.IDLE
        self.current_workflow: Optional[WorkflowPlan] = None
        self.execution_results: List[ExecutionResult] = []
        self.workflow_history: List[WorkflowPlan] = []
        
        # Knowledge base for security operations
        self.security_knowledge_base = self._initialize_knowledge_base()
        
        logger.info("Advanced Workflow Engine initialized")

    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        """Initialize security operations knowledge base"""
        return {
            "reconnaissance_techniques": [
                {"name": "Port Scanning", "tool": "nmap", "command": "nmap -sS -O {target}"},
                {"name": "Service Detection", "tool": "nmap", "command": "nmap -sV -sC {target}"},
                {"name": "Directory Enumeration", "tool": "dirb", "command": "dirb http://{target}"},
                {"name": "DNS Enumeration", "tool": "dnsrecon", "command": "dnsrecon -d {target}"},
                {"name": "Subdomain Discovery", "tool": "sublist3r", "command": "sublist3r -d {target}"}
            ],
            "vulnerability_scanning": [
                {"name": "Web App Scan", "tool": "nikto", "command": "nikto -h {target}"},
                {"name": "SSL/TLS Analysis", "tool": "sslscan", "command": "sslscan {target}"},
                {"name": "SQL Injection Test", "tool": "sqlmap", "command": "sqlmap -u {target} --batch"}
            ],
            "exploitation_frameworks": [
                {"name": "Metasploit", "command": "msfconsole -r {script}"},
                {"name": "Manual Exploit", "command": "{custom_command}"}
            ],
            "common_ports": {
                "21": "FTP", "22": "SSH", "23": "Telnet", "25": "SMTP",
                "53": "DNS", "80": "HTTP", "110": "POP3", "143": "IMAP",
                "443": "HTTPS", "993": "IMAPS", "995": "POP3S"
            }
        }

    async def process_natural_language_request(self, request: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for processing natural language security requests
        Implements the thinking → planning → execution pipeline
        """
        try:
            self.state = WorkflowState.THINKING
            logger.info(f"Processing natural language request: {request}")
            
            # Step 1: THINKING - Understand the request
            thinking_result = await self._thinking_phase(request, context)
            
            # Step 2: PLANNING - Create execution plan
            self.state = WorkflowState.PLANNING
            planning_result = await self._planning_phase(thinking_result, context)
            
            # Step 3: EXECUTION - Execute the plan
            self.state = WorkflowState.EXECUTING
            execution_result = await self._execution_phase(planning_result)
            
            self.state = WorkflowState.COMPLETED
            
            return {
                "status": "success",
                "thinking": thinking_result,
                "planning": planning_result,
                "execution": execution_result,
                "workflow_id": self.current_workflow.id if self.current_workflow else None
            }
            
        except Exception as e:
            self.state = WorkflowState.ERROR
            logger.error(f"Workflow engine error: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "state": self.state.value
            }

    async def _thinking_phase(self, request: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        THINKING PHASE: Analyze and understand the security request
        """
        logger.info("Entering thinking phase...")
        
        # Analyze the request using AI
        thinking_prompt = f"""
        Analyze this penetration testing request and provide structured analysis:
        
        REQUEST: {request}
        CONTEXT: {json.dumps(context, indent=2)}
        
        Please analyze and respond with:
        1. Intent classification (reconnaissance, vulnerability_scan, exploitation, etc.)
        2. Target identification (IP, domain, service)
        3. Risk assessment (low, medium, high, critical)
        4. Required tools and techniques
        5. Potential security concerns
        6. Success criteria
        
        Respond in JSON format.
        """
        
        try:
            ai_response = await self.deepseek_agent.process_natural_language(thinking_prompt, context)
            
            # Extract intent from request using pattern matching as fallback
            intent = self._extract_intent(request)
            target = self._extract_target(request)
            
            thinking_result = {
                "original_request": request,
                "ai_analysis": ai_response,
                "extracted_intent": intent,
                "extracted_target": target,
                "risk_level": self._assess_risk(request),
                "required_capabilities": self._identify_required_capabilities(request),
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Thinking phase completed: {intent} operation on {target}")
            return thinking_result
            
        except Exception as e:
            logger.warning(f"AI thinking failed, using fallback analysis: {e}")
            return self._fallback_thinking_analysis(request, context)

    async def _planning_phase(self, thinking_result: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        PLANNING PHASE: Create detailed execution plan
        """
        logger.info("Entering planning phase...")
        
        intent = thinking_result.get("extracted_intent", "reconnaissance")
        target = thinking_result.get("extracted_target", "unknown")
        risk_level = thinking_result.get("risk_level", "medium")
        
        # Generate workflow plan based on intent
        workflow_steps = await self._generate_workflow_steps(intent, target, context)
        
        # Create workflow plan
        workflow_plan = WorkflowPlan(
            id=f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            title=f"{intent.title()} Operation on {target}",
            description=f"Automated {intent} workflow targeting {target}",
            target=target,
            steps=workflow_steps,
            estimated_total_time=sum(step.estimated_duration for step in workflow_steps),
            risk_assessment=risk_level,
            created_at=datetime.now().isoformat()
        )
        
        self.current_workflow = workflow_plan
        
        planning_result = {
            "workflow_plan": asdict(workflow_plan),
            "step_count": len(workflow_steps),
            "estimated_duration": workflow_plan.estimated_total_time,
            "risk_assessment": risk_level,
            "requires_approval": risk_level in ["high", "critical"]
        }
        
        logger.info(f"Planning phase completed: {len(workflow_steps)} steps planned")
        return planning_result

    async def _execution_phase(self, planning_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        EXECUTION PHASE: Execute the planned workflow
        """
        logger.info("Entering execution phase...")
        
        if not self.current_workflow:
            raise Exception("No workflow plan available for execution")
        
        execution_results = []
        total_steps = len(self.current_workflow.steps)
        
        for i, step in enumerate(self.current_workflow.steps):
            logger.info(f"Executing step {i+1}/{total_steps}: {step.name}")
            
            try:
                start_time = datetime.now()
                
                # Execute the step
                result = await self._execute_workflow_step(step)
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                exec_result = ExecutionResult(
                    step_id=step.id,
                    success=result.get("success", False),
                    output=result.get("output", ""),
                    error_message=result.get("error"),
                    execution_time=execution_time,
                    artifacts=result.get("artifacts", [])
                )
                
                execution_results.append(exec_result)
                self.execution_results.append(exec_result)
                
                # Stop on failure if step is critical
                if not exec_result.success and step.risk_level == "critical":
                    logger.error(f"Critical step failed: {step.name}")
                    break
                    
            except Exception as e:
                logger.error(f"Step execution failed: {step.name} - {e}")
                exec_result = ExecutionResult(
                    step_id=step.id,
                    success=False,
                    output="",
                    error_message=str(e),
                    execution_time=0,
                    artifacts=[]
                )
                execution_results.append(exec_result)
        
        # Generate summary report
        success_count = sum(1 for r in execution_results if r.success)
        total_time = sum(r.execution_time for r in execution_results)
        
        execution_summary = {
            "total_steps": total_steps,
            "successful_steps": success_count,
            "failed_steps": total_steps - success_count,
            "total_execution_time": total_time,
            "success_rate": (success_count / total_steps) * 100 if total_steps > 0 else 0,
            "results": [asdict(r) for r in execution_results],
            "artifacts_generated": sum(len(r.artifacts) for r in execution_results)
        }
        
        logger.info(f"Execution completed: {success_count}/{total_steps} steps successful")
        return execution_summary

    async def _execute_workflow_step(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute a single workflow step"""
        try:
            if step.operation_type == OperationType.RECONNAISSANCE:
                return await self._execute_reconnaissance_step(step)
            elif step.operation_type == OperationType.VULNERABILITY_SCAN:
                return await self._execute_vulnerability_step(step)
            elif step.operation_type == OperationType.TOOL_EXECUTION:
                return await self._execute_tool_step(step)
            elif step.operation_type == OperationType.NETWORK_ANALYSIS:
                return await self._execute_network_analysis_step(step)
            else:
                return await self._execute_generic_step(step)
                
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "artifacts": []
            }

    async def _execute_reconnaissance_step(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute reconnaissance operations"""
        if "nmap" in step.command:
            result = await self.security_tools.run_nmap_scan(
                step.parameters.get("target", "127.0.0.1"),
                step.parameters.get("scan_type", "basic")
            )
        elif "dirb" in step.command:
            result = await self.security_tools.run_dirb_scan(
                step.parameters.get("target", "http://127.0.0.1")
            )
        else:
            result = await self.command_engine.execute_command(step.command)
        
        return {
            "success": result.get("success", False),
            "output": result.get("output", ""),
            "artifacts": [f"recon_result_{step.id}.txt"]
        }

    async def _execute_vulnerability_step(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute vulnerability scanning operations"""
        scan_id = await self.vuln_scanner.start_scan(
            step.parameters.get("target", "127.0.0.1")
        )
        
        # Wait a moment for scan to initialize and get some results
        await asyncio.sleep(2)
        
        return {
            "success": True,
            "output": f"Vulnerability scan started with ID: {scan_id}\nTarget: {step.parameters.get('target', '127.0.0.1')}",
            "artifacts": [f"vuln_scan_{step.id}.json"]
        }

    async def _execute_tool_step(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute security tool operations"""
        tool_name = step.parameters.get("tool")
        
        if tool_name == "metasploit":
            result = await self.security_tools.run_metasploit_command(
                step.parameters.get("command", "version")
            )
        elif tool_name == "sqlmap":
            result = await self.security_tools.run_sqlmap_scan(
                step.parameters.get("target", "http://127.0.0.1")
            )
        elif tool_name == "hydra":
            result = await self.security_tools.run_hydra_attack(
                step.parameters.get("target", "127.0.0.1"),
                step.parameters.get("service", "ssh")
            )
        else:
            result = await self.command_engine.execute_command(step.command)
        
        return {
            "success": result.get("success", False),
            "output": result.get("output", ""),
            "artifacts": [f"tool_output_{step.id}.txt"]
        }

    async def _execute_network_analysis_step(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute network analysis operations"""
        network_info = await self.network_monitor.get_network_info()
        
        return {
            "success": True,
            "output": json.dumps(network_info, indent=2),
            "artifacts": [f"network_analysis_{step.id}.json"]
        }

    async def _execute_generic_step(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute generic command step"""
        result = await self.command_engine.execute_command(step.command)
        
        return {
            "success": result.get("success", False),
            "output": result.get("output", ""),
            "artifacts": []
        }

    async def _generate_workflow_steps(self, intent: str, target: str, context: Dict[str, Any]) -> List[WorkflowStep]:
        """Generate workflow steps based on intent and target"""
        steps = []
        step_counter = 1
        
        if intent == "reconnaissance":
            steps.extend([
                WorkflowStep(
                    id=f"step_{step_counter}",
                    name="Port Scan",
                    operation_type=OperationType.RECONNAISSANCE,
                    command=f"nmap -sS {target}",
                    parameters={"target": target, "scan_type": "syn"},
                    dependencies=[],
                    estimated_duration=60,
                    risk_level="low",
                    description=f"Perform SYN scan on {target}"
                ),
                WorkflowStep(
                    id=f"step_{step_counter + 1}",
                    name="Service Detection",
                    operation_type=OperationType.RECONNAISSANCE,
                    command=f"nmap -sV -sC {target}",
                    parameters={"target": target, "scan_type": "service"},
                    dependencies=[f"step_{step_counter}"],
                    estimated_duration=120,
                    risk_level="low",
                    description=f"Detect services and versions on {target}"
                )
            ])
        
        elif intent == "vulnerability_scan":
            steps.append(
                WorkflowStep(
                    id=f"step_{step_counter}",
                    name="Vulnerability Scan",
                    operation_type=OperationType.VULNERABILITY_SCAN,
                    command=f"scan_target {target}",
                    parameters={"target": target},
                    dependencies=[],
                    estimated_duration=180,
                    risk_level="medium",
                    description=f"Comprehensive vulnerability scan of {target}"
                )
            )
        
        elif intent == "network_analysis":
            steps.append(
                WorkflowStep(
                    id=f"step_{step_counter}",
                    name="Network Analysis",
                    operation_type=OperationType.NETWORK_ANALYSIS,
                    command="analyze_network",
                    parameters={"target": target},
                    dependencies=[],
                    estimated_duration=30,
                    risk_level="low",
                    description="Analyze network topology and connectivity"
                )
            )
        
        return steps

    def _extract_intent(self, request: str) -> str:
        """Extract operation intent from natural language request"""
        request_lower = request.lower()
        
        if any(word in request_lower for word in ["scan", "nmap", "port", "enumerate"]):
            return "reconnaissance"
        elif any(word in request_lower for word in ["vulnerability", "vuln", "security", "weakness"]):
            return "vulnerability_scan"
        elif any(word in request_lower for word in ["exploit", "attack", "penetrate"]):
            return "exploitation"
        elif any(word in request_lower for word in ["network", "topology", "routing"]):
            return "network_analysis"
        elif any(word in request_lower for word in ["report", "summary", "analysis"]):
            return "reporting"
        else:
            return "reconnaissance"  # Default

    def _extract_target(self, request: str) -> str:
        """Extract target from natural language request"""
        # Look for IP addresses
        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        ip_match = re.search(ip_pattern, request)
        if ip_match:
            return ip_match.group()
        
        # Look for domain names
        domain_pattern = r'\b[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}\b'
        domain_match = re.search(domain_pattern, request)
        if domain_match:
            return domain_match.group()
        
        # Look for localhost variants
        if any(word in request.lower() for word in ["localhost", "local", "127.0.0.1"]):
            return "127.0.0.1"
        
        return "unknown"

    def _assess_risk(self, request: str) -> str:
        """Assess risk level of the request"""
        request_lower = request.lower()
        
        if any(word in request_lower for word in ["exploit", "attack", "penetrate", "hack"]):
            return "high"
        elif any(word in request_lower for word in ["vulnerability", "scan", "probe"]):
            return "medium"
        else:
            return "low"

    def _identify_required_capabilities(self, request: str) -> List[str]:
        """Identify required capabilities for the request"""
        capabilities = []
        request_lower = request.lower()
        
        if "nmap" in request_lower or "scan" in request_lower:
            capabilities.append("port_scanning")
        if "vulnerability" in request_lower:
            capabilities.append("vulnerability_assessment")
        if "metasploit" in request_lower:
            capabilities.append("exploitation_framework")
        if "network" in request_lower:
            capabilities.append("network_analysis")
        
        return capabilities

    def _fallback_thinking_analysis(self, request: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback analysis when AI is unavailable"""
        return {
            "original_request": request,
            "ai_analysis": "AI analysis unavailable - using fallback",
            "extracted_intent": self._extract_intent(request),
            "extracted_target": self._extract_target(request),
            "risk_level": self._assess_risk(request),
            "required_capabilities": self._identify_required_capabilities(request),
            "timestamp": datetime.now().isoformat()
        }

    def get_workflow_status(self) -> Dict[str, Any]:
        """Get current workflow status"""
        return {
            "state": self.state.value,
            "current_workflow": asdict(self.current_workflow) if self.current_workflow else None,
            "execution_results_count": len(self.execution_results),
            "workflow_history_count": len(self.workflow_history)
        }

    def is_ready(self) -> bool:
        """Check if workflow engine is ready"""
        return (
            self.command_engine.is_ready() and
            self.security_tools.is_ready() and
            self.state != WorkflowState.ERROR
        )
