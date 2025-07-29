#!/usr/bin/env python3
"""
Kali AI Terminal Backend Testing Suite
Tests WebSocket connections, API endpoints, and security tool integrations
"""

import asyncio
import json
import requests
import websockets
import time
from datetime import datetime
import sys
import os

# Get backend URL from frontend .env file
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=')[1].strip()
    except:
        pass
    return "https://ad08de15-5c9e-4861-93ed-bb75b27e86e7.preview.emergentagent.com"

BACKEND_URL = get_backend_url()
API_BASE = f"{BACKEND_URL}/api"
WS_URL = BACKEND_URL.replace('https://', 'wss://').replace('http://', 'ws://') + "/ws"

print(f"🔧 Testing Backend URL: {BACKEND_URL}")
print(f"🔧 API Base: {API_BASE}")
print(f"🔧 WebSocket URL: {WS_URL}")

class KaliTerminalTester:
    def __init__(self):
        self.test_results = {}
        self.failed_tests = []
        self.passed_tests = []
        
    def log_test(self, test_name, status, message=""):
        """Log test results"""
        self.test_results[test_name] = {"status": status, "message": message}
        if status == "PASS":
            self.passed_tests.append(test_name)
            print(f"✅ {test_name}: {message}")
        else:
            self.failed_tests.append(test_name)
            print(f"❌ {test_name}: {message}")
    
    def test_api_root(self):
        """Test the root API endpoint"""
        try:
            response = requests.get(f"{API_BASE}/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "Kali AI Terminal Backend Online" in data.get("message", ""):
                    self.log_test("API Root Endpoint", "PASS", "Backend is online and responding")
                    return True
                else:
                    self.log_test("API Root Endpoint", "FAIL", f"Unexpected response: {data}")
            else:
                self.log_test("API Root Endpoint", "FAIL", f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("API Root Endpoint", "FAIL", f"Connection error: {str(e)}")
        return False
    
    def test_system_stats_api(self):
        """Test system monitoring API"""
        try:
            response = requests.get(f"{API_BASE}/system/stats", timeout=10)
            if response.status_code == 200:
                stats = response.json()
                required_fields = ["cpu_percent", "memory_percent", "disk_percent", "network", "processes", "platform"]
                
                missing_fields = [field for field in required_fields if field not in stats]
                if not missing_fields:
                    # Validate data types and ranges
                    if (isinstance(stats["cpu_percent"], (int, float)) and 0 <= stats["cpu_percent"] <= 100 and
                        isinstance(stats["memory_percent"], (int, float)) and 0 <= stats["memory_percent"] <= 100):
                        self.log_test("System Stats API", "PASS", f"All system metrics available: CPU {stats['cpu_percent']}%, Memory {stats['memory_percent']}%")
                        return True
                    else:
                        self.log_test("System Stats API", "FAIL", "Invalid data ranges or types")
                else:
                    self.log_test("System Stats API", "FAIL", f"Missing fields: {missing_fields}")
            else:
                self.log_test("System Stats API", "FAIL", f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("System Stats API", "FAIL", f"Error: {str(e)}")
        return False
    
    def test_ai_query_api(self):
        """Test AI query processing"""
        test_queries = [
            {"query": "help", "expected_keyword": "AI Assistant"},
            {"query": "scan target 192.168.1.1", "expected_keyword": "AI Analysis"},
            {"query": "exploit vulnerability", "expected_keyword": "AI Suggestion"}
        ]
        
        all_passed = True
        for test_query in test_queries:
            try:
                payload = {"query": test_query["query"], "context": "penetration testing"}
                response = requests.post(f"{API_BASE}/ai/query", json=payload, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "success" and test_query["expected_keyword"] in data.get("response", ""):
                        self.log_test(f"AI Query - {test_query['query'][:20]}...", "PASS", f"AI responded correctly")
                    else:
                        self.log_test(f"AI Query - {test_query['query'][:20]}...", "FAIL", f"Unexpected AI response: {data}")
                        all_passed = False
                else:
                    self.log_test(f"AI Query - {test_query['query'][:20]}...", "FAIL", f"HTTP {response.status_code}")
                    all_passed = False
            except Exception as e:
                self.log_test(f"AI Query - {test_query['query'][:20]}...", "FAIL", f"Error: {str(e)}")
                all_passed = False
        
        return all_passed
    
    def test_security_tools_api(self):
        """Test security tools command execution"""
        test_commands = [
            {"command": "nmap -sS 192.168.1.1", "target": "192.168.1.1", "expected_tool": "nmap"},
            {"command": "sqlmap -u http://example.com", "target": "http://example.com", "expected_tool": "sqlmap"},
            {"command": "ls -la", "target": "", "expected_tool": "terminal"}
        ]
        
        all_passed = True
        for test_cmd in test_commands:
            try:
                payload = {"command": test_cmd["command"], "target": test_cmd["target"]}
                response = requests.post(f"{API_BASE}/command/execute", json=payload, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if (data.get("status") == "success" and 
                        data.get("result", {}).get("tool") == test_cmd["expected_tool"]):
                        self.log_test(f"Security Tool - {test_cmd['expected_tool']}", "PASS", f"Command executed successfully")
                    else:
                        self.log_test(f"Security Tool - {test_cmd['expected_tool']}", "FAIL", f"Unexpected response: {data}")
                        all_passed = False
                else:
                    self.log_test(f"Security Tool - {test_cmd['expected_tool']}", "FAIL", f"HTTP {response.status_code}")
                    all_passed = False
            except Exception as e:
                self.log_test(f"Security Tool - {test_cmd['expected_tool']}", "FAIL", f"Error: {str(e)}")
                all_passed = False
        
        return all_passed
    
    def test_target_scanning_api(self):
        """Test target scanning functionality"""
        try:
            payload = {"target": "192.168.1.100", "scan_type": "comprehensive"}
            response = requests.post(f"{API_BASE}/scan/target", json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if (data.get("status") == "initiated" and 
                    data.get("target") == "192.168.1.100" and
                    "scan_id" in data):
                    self.log_test("Target Scanning API", "PASS", f"Scan initiated with ID: {data['scan_id'][:8]}...")
                    return True
                else:
                    self.log_test("Target Scanning API", "FAIL", f"Unexpected response: {data}")
            else:
                self.log_test("Target Scanning API", "FAIL", f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Target Scanning API", "FAIL", f"Error: {str(e)}")
        return False
    
    def test_available_tools_api(self):
        """Test available tools endpoint"""
        try:
            response = requests.get(f"{API_BASE}/tools/available", timeout=10)
            if response.status_code == 200:
                data = response.json()
                expected_tools = ["nmap", "sqlmap", "metasploit"]
                available_tools = data.get("tools", [])
                
                if all(tool in available_tools for tool in expected_tools):
                    self.log_test("Available Tools API", "PASS", f"All security tools available: {len(available_tools)} tools")
                    return True
                else:
                    self.log_test("Available Tools API", "FAIL", f"Missing tools. Available: {available_tools}")
            else:
                self.log_test("Available Tools API", "FAIL", f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Available Tools API", "FAIL", f"Error: {str(e)}")
        return False
    
    async def test_websocket_connection(self):
        """Test WebSocket connection and message handling"""
        try:
            async with websockets.connect(WS_URL, timeout=10) as websocket:
                # Test connection message
                connection_msg = await asyncio.wait_for(websocket.recv(), timeout=5)
                connection_data = json.loads(connection_msg)
                
                if connection_data.get("type") == "connection":
                    self.log_test("WebSocket Connection", "PASS", "Connected successfully")
                    
                    # Test command execution via WebSocket
                    await self.test_websocket_command_execution(websocket)
                    
                    # Test AI query via WebSocket
                    await self.test_websocket_ai_query(websocket)
                    
                    # Test system stats via WebSocket
                    await self.test_websocket_system_stats(websocket)
                    
                    # Test target scanning via WebSocket
                    await self.test_websocket_target_scan(websocket)
                    
                    return True
                else:
                    self.log_test("WebSocket Connection", "FAIL", f"Unexpected connection message: {connection_data}")
        except Exception as e:
            self.log_test("WebSocket Connection", "FAIL", f"Connection error: {str(e)}")
        return False
    
    async def test_websocket_command_execution(self, websocket):
        """Test command execution through WebSocket"""
        try:
            command_msg = {
                "type": "execute_command",
                "command": "nmap -sS 192.168.1.1",
                "target": "192.168.1.1"
            }
            
            await websocket.send(json.dumps(command_msg))
            
            # Wait for command start acknowledgment
            start_msg = await asyncio.wait_for(websocket.recv(), timeout=5)
            start_data = json.loads(start_msg)
            
            # Wait for command result
            result_msg = await asyncio.wait_for(websocket.recv(), timeout=5)
            result_data = json.loads(result_msg)
            
            if (start_data.get("type") == "command_start" and 
                result_data.get("type") == "command_result" and
                result_data.get("result", {}).get("tool") == "nmap"):
                self.log_test("WebSocket Command Execution", "PASS", "Command executed via WebSocket")
            else:
                self.log_test("WebSocket Command Execution", "FAIL", f"Unexpected response sequence")
        except Exception as e:
            self.log_test("WebSocket Command Execution", "FAIL", f"Error: {str(e)}")
    
    async def test_websocket_ai_query(self, websocket):
        """Test AI query through WebSocket"""
        try:
            ai_msg = {
                "type": "ai_query",
                "query": "help with penetration testing",
                "context": "security assessment"
            }
            
            await websocket.send(json.dumps(ai_msg))
            
            # Wait for AI response
            response_msg = await asyncio.wait_for(websocket.recv(), timeout=5)
            response_data = json.loads(response_msg)
            
            if (response_data.get("type") == "ai_response" and 
                "AI Assistant" in response_data.get("response", "")):
                self.log_test("WebSocket AI Query", "PASS", "AI query processed via WebSocket")
            else:
                self.log_test("WebSocket AI Query", "FAIL", f"Unexpected AI response: {response_data}")
        except Exception as e:
            self.log_test("WebSocket AI Query", "FAIL", f"Error: {str(e)}")
    
    async def test_websocket_system_stats(self, websocket):
        """Test system stats through WebSocket"""
        try:
            stats_msg = {"type": "system_stats"}
            await websocket.send(json.dumps(stats_msg))
            
            # Wait for stats response
            response_msg = await asyncio.wait_for(websocket.recv(), timeout=5)
            response_data = json.loads(response_msg)
            
            if (response_data.get("type") == "system_stats" and 
                "cpu_percent" in response_data.get("stats", {})):
                self.log_test("WebSocket System Stats", "PASS", "System stats received via WebSocket")
            else:
                self.log_test("WebSocket System Stats", "FAIL", f"Unexpected stats response: {response_data}")
        except Exception as e:
            self.log_test("WebSocket System Stats", "FAIL", f"Error: {str(e)}")
    
    async def test_websocket_target_scan(self, websocket):
        """Test target scanning through WebSocket"""
        try:
            scan_msg = {
                "type": "scan_target",
                "target": "192.168.1.50",
                "scan_type": "basic"
            }
            
            await websocket.send(json.dumps(scan_msg))
            
            # Wait for scan start
            start_msg = await asyncio.wait_for(websocket.recv(), timeout=5)
            start_data = json.loads(start_msg)
            
            # Wait for at least one progress update
            progress_msg = await asyncio.wait_for(websocket.recv(), timeout=5)
            progress_data = json.loads(progress_msg)
            
            if (start_data.get("type") == "scan_start" and 
                progress_data.get("type") == "scan_progress" and
                progress_data.get("progress", 0) > 0):
                self.log_test("WebSocket Target Scan", "PASS", "Target scan initiated via WebSocket")
            else:
                self.log_test("WebSocket Target Scan", "FAIL", f"Unexpected scan response sequence")
        except Exception as e:
            self.log_test("WebSocket Target Scan", "FAIL", f"Error: {str(e)}")
    
    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting Kali AI Terminal Backend Tests")
        print("=" * 60)
        
        # Test API endpoints first
        self.test_api_root()
        self.test_system_stats_api()
        self.test_ai_query_api()
        self.test_security_tools_api()
        self.test_target_scanning_api()
        self.test_available_tools_api()
        
        # Test WebSocket functionality
        print("\n🔌 Testing WebSocket Functionality...")
        asyncio.run(self.test_websocket_connection())
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_count = len(self.passed_tests)
        failed_count = len(self.failed_tests)
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_count}")
        print(f"❌ Failed: {failed_count}")
        print(f"Success Rate: {(passed_count/total_tests)*100:.1f}%")
        
        if self.failed_tests:
            print("\n🔍 FAILED TESTS:")
            for test_name in self.failed_tests:
                result = self.test_results[test_name]
                print(f"  • {test_name}: {result['message']}")
        
        print("\n🎯 CRITICAL FUNCTIONALITY STATUS:")
        critical_tests = [
            "API Root Endpoint",
            "WebSocket Connection", 
            "System Stats API",
            "WebSocket AI Query",
            "WebSocket Command Execution"
        ]
        
        for test in critical_tests:
            if test in self.test_results:
                status = "✅" if self.test_results[test]["status"] == "PASS" else "❌"
                print(f"  {status} {test}")

if __name__ == "__main__":
    tester = KaliTerminalTester()
    tester.run_all_tests()