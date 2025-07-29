"""
KALI AI TERMINAL - Backend Test Runner
Comprehensive testing of natural language workflows and backend functionality
"""

import asyncio
import aiohttp
import json
import logging
import websocket
import time
from datetime import datetime
from typing import Dict, List

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BackendTester:
    """
    Comprehensive backend testing class
    Tests all components including workflow engine, AI assistant, and security tools
    """
    
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.ws_url = "ws://127.0.0.1:8000/ws"
        self.test_results = []
        
    async def test_health_endpoint(self):
        """Test the health check endpoint"""
        logger.info("Testing health endpoint...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/health") as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"Health check passed: {data}")
                        
                        # Check all components
                        components = data.get('components', {})
                        all_healthy = all(components.values())
                        
                        self.test_results.append({
                            "test": "health_check",
                            "passed": all_healthy,
                            "details": components,
                            "timestamp": datetime.now().isoformat()
                        })
                        
                        return all_healthy
                    else:
                        logger.error(f"Health check failed: {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"Health check error: {e}")
            return False

    async def test_natural_language_workflows(self):
        """Test natural language workflow processing"""
        logger.info("Testing natural language workflows...")
        
        test_scenarios = [
            {
                "name": "port_scan_reconnaissance",
                "request": "Scan ports on localhost",
                "expected_intent": "reconnaissance",
                "expected_target": "127.0.0.1"
            },
            {
                "name": "vulnerability_assessment",
                "request": "Check for vulnerabilities on 192.168.1.1",
                "expected_intent": "vulnerability_scan",
                "expected_target": "192.168.1.1"
            },
            {
                "name": "network_analysis",
                "request": "Analyze the local network topology",
                "expected_intent": "network_analysis",
                "expected_target": "unknown"
            },
            {
                "name": "service_enumeration",
                "request": "Enumerate services on example.com",
                "expected_intent": "reconnaissance",
                "expected_target": "example.com"
            },
            {
                "name": "exploit_attempt",
                "request": "Exploit SQL injection on testsite.com",
                "expected_intent": "exploitation",
                "expected_target": "testsite.com"
            }
        ]
        
        results = []
        
        for scenario in test_scenarios:
            logger.info(f"Testing scenario: {scenario['name']}")
            
            try:
                # Import and test the workflow engine directly
                from core.workflow_engine import AdvancedWorkflowEngine
                
                workflow_engine = AdvancedWorkflowEngine()
                context = {"test_mode": True}
                
                result = await workflow_engine.process_natural_language_request(
                    scenario['request'], context
                )
                
                # Validate results
                thinking = result.get('thinking', {})
                planning = result.get('planning', {})
                execution = result.get('execution', {})
                
                intent_match = thinking.get('extracted_intent') == scenario['expected_intent']
                target_match = thinking.get('extracted_target') == scenario['expected_target']
                
                test_passed = intent_match and target_match and result.get('status') == 'success'
                
                scenario_result = {
                    "scenario": scenario['name'],
                    "request": scenario['request'],
                    "passed": test_passed,
                    "extracted_intent": thinking.get('extracted_intent'),
                    "expected_intent": scenario['expected_intent'],
                    "extracted_target": thinking.get('extracted_target'),
                    "expected_target": scenario['expected_target'],
                    "workflow_steps": len(planning.get('workflow_plan', {}).get('steps', [])),
                    "execution_success_rate": execution.get('success_rate', 0),
                    "timestamp": datetime.now().isoformat()
                }
                
                results.append(scenario_result)
                
                logger.info(f"Scenario {scenario['name']}: {'PASSED' if test_passed else 'FAILED'}")
                if not test_passed:
                    logger.warning(f"Expected intent: {scenario['expected_intent']}, Got: {thinking.get('extracted_intent')}")
                    logger.warning(f"Expected target: {scenario['expected_target']}, Got: {thinking.get('extracted_target')}")
                
            except Exception as e:
                logger.error(f"Scenario {scenario['name']} failed with error: {e}")
                results.append({
                    "scenario": scenario['name'],
                    "passed": False,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
        
        self.test_results.extend(results)
        return results

    async def test_command_execution(self):
        """Test command execution through the command engine"""
        logger.info("Testing command execution...")
        
        test_commands = [
            {
                "command": "echo 'Hello from Kali AI Terminal'",
                "should_pass": True,
                "expected_in_output": "Hello from Kali AI Terminal"
            },
            {
                "command": "dir" if __import__('os').name == 'nt' else "ls",
                "should_pass": True,
                "expected_in_output": ""  # Just check it runs
            },
            {
                "command": "nmap --version",
                "should_pass": True,
                "expected_in_output": "Nmap"
            },
            {
                "command": "rm -rf /",  # Dangerous command
                "should_pass": False,
                "expected_in_output": "blocked"
            }
        ]
        
        results = []
        
        try:
            from core.command_engine import IntelligentCommandEngine
            
            command_engine = IntelligentCommandEngine()
            
            for test_cmd in test_commands:
                logger.info(f"Testing command: {test_cmd['command']}")
                
                try:
                    result = await command_engine.process_command(test_cmd['command'])
                    
                    passed = (
                        (test_cmd['should_pass'] and result['success']) or
                        (not test_cmd['should_pass'] and not result['success'])
                    )
                    
                    if test_cmd['expected_in_output'] and passed:
                        passed = test_cmd['expected_in_output'].lower() in result['output'].lower()
                    
                    cmd_result = {
                        "command": test_cmd['command'],
                        "passed": passed,
                        "expected_pass": test_cmd['should_pass'],
                        "actual_success": result['success'],
                        "output_length": len(result['output']),
                        "has_predictions": len(result.get('predictions', [])) > 0,
                        "has_insights": bool(result.get('insights', {})),
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    results.append(cmd_result)
                    logger.info(f"Command test: {'PASSED' if passed else 'FAILED'}")
                    
                except Exception as e:
                    logger.error(f"Command execution error: {e}")
                    results.append({
                        "command": test_cmd['command'],
                        "passed": False,
                        "error": str(e),
                        "timestamp": datetime.now().isoformat()
                    })
            
        except Exception as e:
            logger.error(f"Command engine test setup failed: {e}")
        
        self.test_results.extend(results)
        return results

    async def test_security_tools_integration(self):
        """Test security tools integration"""
        logger.info("Testing security tools integration...")
        
        results = []
        
        try:
            from core.security_tools import SecurityToolsManager
            
            tools_manager = SecurityToolsManager()
            
            # Test tool availability
            available_tools = await tools_manager.get_available_tools()
            
            tools_test = {
                "test": "tools_availability",
                "passed": len(available_tools) > 0,
                "available_tools": len(available_tools),
                "tools_list": list(available_tools.keys()) if isinstance(available_tools, dict) else [],
                "timestamp": datetime.now().isoformat()
            }
            
            results.append(tools_test)
            logger.info(f"Tools availability: {'PASSED' if tools_test['passed'] else 'FAILED'}")
            
            # Test basic nmap functionality (safe command)
            try:
                nmap_result = await tools_manager.run_nmap_scan("127.0.0.1", "basic")
                
                nmap_test = {
                    "test": "nmap_basic_scan",
                    "passed": nmap_result.get('success', False),
                    "has_output": len(nmap_result.get('output', '')) > 0,
                    "timestamp": datetime.now().isoformat()
                }
                
                results.append(nmap_test)
                logger.info(f"Nmap test: {'PASSED' if nmap_test['passed'] else 'FAILED'}")
                
            except Exception as e:
                logger.warning(f"Nmap test failed (tool may not be installed): {e}")
                results.append({
                    "test": "nmap_basic_scan",
                    "passed": False,
                    "error": "Tool not available or failed",
                    "timestamp": datetime.now().isoformat()
                })
            
        except Exception as e:
            logger.error(f"Security tools test failed: {e}")
            results.append({
                "test": "security_tools_integration",
                "passed": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
        
        self.test_results.extend(results)
        return results

    async def test_vulnerability_scanner(self):
        """Test vulnerability scanner functionality"""
        logger.info("Testing vulnerability scanner...")
        
        results = []
        
        try:
            from core.vulnerability_scanner import VulnerabilityScanner
            
            vuln_scanner = VulnerabilityScanner()
            
            # Test scanner readiness
            scanner_ready = vuln_scanner.is_ready()
            
            ready_test = {
                "test": "vulnerability_scanner_ready",
                "passed": scanner_ready,
                "timestamp": datetime.now().isoformat()
            }
            
            results.append(ready_test)
            logger.info(f"Scanner readiness: {'PASSED' if scanner_ready else 'FAILED'}")
            
            # Test basic scan
            try:
                scan_result = await vuln_scanner.scan_target("127.0.0.1")
                
                scan_test = {
                    "test": "basic_vulnerability_scan",
                    "passed": scan_result.get('success', False),
                    "findings_count": len(scan_result.get('vulnerabilities', [])),
                    "ports_scanned": len(scan_result.get('open_ports', [])),
                    "timestamp": datetime.now().isoformat()
                }
                
                results.append(scan_test)
                logger.info(f"Basic scan: {'PASSED' if scan_test['passed'] else 'FAILED'}")
                
            except Exception as e:
                logger.warning(f"Vulnerability scan test failed: {e}")
                results.append({
                    "test": "basic_vulnerability_scan",
                    "passed": False,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
        
        except Exception as e:
            logger.error(f"Vulnerability scanner test failed: {e}")
            results.append({
                "test": "vulnerability_scanner",
                "passed": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
        
        self.test_results.extend(results)
        return results

    async def run_all_tests(self):
        """Run all tests and generate comprehensive report"""
        logger.info("🚀 Starting comprehensive backend testing...")
        
        test_start_time = datetime.now()
        
        # Run all test suites
        await self.test_health_endpoint()
        await self.test_natural_language_workflows()
        await self.test_command_execution()
        await self.test_security_tools_integration()
        await self.test_vulnerability_scanner()
        
        test_end_time = datetime.now()
        total_duration = (test_end_time - test_start_time).total_seconds()
        
        # Generate summary report
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result.get('passed', False))
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        summary_report = {
            "test_summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "success_rate": f"{success_rate:.1f}%",
                "duration_seconds": total_duration,
                "start_time": test_start_time.isoformat(),
                "end_time": test_end_time.isoformat()
            },
            "detailed_results": self.test_results
        }
        
        # Print summary
        print("\n" + "="*80)
        print("🎯 KALI AI TERMINAL - BACKEND TEST RESULTS")
        print("="*80)
        print(f"📊 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        print(f"⏱️  Duration: {total_duration:.2f} seconds")
        print("="*80)
        
        # Print failed tests details
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result.get('passed', False):
                    test_name = result.get('test', result.get('scenario', result.get('command', 'Unknown')))
                    error = result.get('error', 'Test conditions not met')
                    print(f"  • {test_name}: {error}")
        
        print("\n✨ Test completed successfully!")
        
        # Save detailed report
        with open('backend/test_results.json', 'w') as f:
            json.dump(summary_report, f, indent=2)
        
        logger.info("Test results saved to backend/test_results.json")
        
        return summary_report

async def main():
    """Main test runner"""
    print("🔧 Kali AI Terminal Backend Test Suite")
    print("=====================================")
    
    tester = BackendTester()
    
    try:
        # Check if backend is running
        logger.info("Checking if backend server is running...")
        
        import aiohttp
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get("http://127.0.0.1:8000/") as response:
                    if response.status == 200:
                        logger.info("✅ Backend server is running")
                    else:
                        logger.warning("⚠️  Backend server responded with non-200 status")
            except Exception as e:
                logger.warning(f"⚠️  Backend server may not be running: {e}")
                logger.info("You can start it with: python backend/main.py")
        
        # Run all tests
        await tester.run_all_tests()
        
    except KeyboardInterrupt:
        logger.info("Test interrupted by user")
    except Exception as e:
        logger.error(f"Test runner failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
