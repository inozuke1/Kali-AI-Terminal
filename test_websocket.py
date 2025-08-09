#!/usr/bin/env python3
"""
WebSocket Test Client for Kali AI Terminal
"""
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://127.0.0.1:8000/ws"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("🔗 Connected to Kali AI Terminal WebSocket")
            
            # Test 1: System Status
            print("\n📊 Testing System Status...")
            message = {
                "type": "get_system_status",
                "payload": {}
            }
            await websocket.send(json.dumps(message))
            response = await websocket.recv()
            print("Response:", json.loads(response))
            
            # Test 2: Execute Command
            print("\n💻 Testing Command Execution...")
            message = {
                "type": "execute_command",
                "payload": {
                    "command": "whoami",
                    "context": {}
                }
            }
            await websocket.send(json.dumps(message))
            response = await websocket.recv()
            print("Response:", json.loads(response))
            
            # Test 3: Natural Language Request
            print("\n🧠 Testing Natural Language Processing...")
            message = {
                "type": "natural_language_request",
                "payload": {
                    "request": "scan the local network for open ports",
                    "context": {}
                }
            }
            await websocket.send(json.dumps(message))
            response = await websocket.recv()
            print("Response:", json.loads(response))
            
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")

if __name__ == "__main__":
    print("🚀 Starting Kali AI Terminal WebSocket Tests")
    asyncio.run(test_websocket())
