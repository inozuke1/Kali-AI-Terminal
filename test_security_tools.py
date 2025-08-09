#!/usr/bin/env python3
"""
Security Tools Test for Kali AI Terminal
"""
import asyncio
import websockets
import json

async def test_security_features():
    uri = "ws://127.0.0.1:8000/ws"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("🔗 Connected to Kali AI Terminal")
            
            # Test: Tool Operation
            print("\n🛠️ Testing Security Tools...")
            message = {
                "type": "tool_operation",
                "payload": {
                    "tool": "port_scanner",
                    "target": "127.0.0.1",
                    "options": {
                        "ports": "22,80,443,3000,8000",
                        "timeout": 5
                    }
                }
            }
            await websocket.send(json.dumps(message))
            response = await websocket.recv()
            print("Port Scan Response:", json.loads(response))
            
            # Test: Network Scan
            print("\n🌐 Testing Network Scanner...")
            message = {
                "type": "scan_target",
                "payload": {
                    "target": "192.168.217.1",
                    "scan_type": "quick",
                    "options": {}
                }
            }
            await websocket.send(json.dumps(message))
            response = await websocket.recv()
            print("Network Scan Response:", json.loads(response))
            
    except Exception as e:
        print(f"❌ Security tools test failed: {e}")

if __name__ == "__main__":
    print("🚀 Testing Kali AI Terminal Security Features")
    asyncio.run(test_security_features())
