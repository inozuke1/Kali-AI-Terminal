#!/usr/bin/env python3
"""
Test WebSocket connection using local backend URL
"""

import asyncio
import json
import websockets

WS_URL = "ws://localhost:8001/ws"

print(f"🔧 Local WebSocket URL: {WS_URL}")

async def test_local_websocket():
    try:
        print("🔌 Attempting local WebSocket connection...")
        async with websockets.connect(WS_URL, timeout=10) as websocket:
            print("✅ WebSocket connected successfully!")
            
            # Listen for initial connection message
            print("📡 Listening for connection message...")
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=5)
                print(f"📨 Connection message: {message}")
                
                parsed = json.loads(message)
                print(f"📋 Parsed JSON: {parsed}")
                
                if parsed.get("type") == "connection":
                    print("✅ Received proper connection message!")
                    
                    # Test system stats request
                    print("\n📤 Testing system stats request...")
                    stats_msg = {"type": "system_stats"}
                    await websocket.send(json.dumps(stats_msg))
                    
                    response = await asyncio.wait_for(websocket.recv(), timeout=5)
                    print(f"📨 Stats response: {response}")
                    
                    stats_data = json.loads(response)
                    if stats_data.get("type") == "system_stats":
                        print("✅ System stats working via WebSocket!")
                    
                    # Test AI query
                    print("\n📤 Testing AI query...")
                    ai_msg = {"type": "ai_query", "query": "help", "context": "test"}
                    await websocket.send(json.dumps(ai_msg))
                    
                    ai_response = await asyncio.wait_for(websocket.recv(), timeout=5)
                    print(f"📨 AI response: {ai_response}")
                    
                    ai_data = json.loads(ai_response)
                    if ai_data.get("type") == "ai_response":
                        print("✅ AI query working via WebSocket!")
                        
                else:
                    print(f"❌ Unexpected connection message type: {parsed.get('type')}")
                    
            except asyncio.TimeoutError:
                print("⏰ No connection message received (timeout)")
                
    except Exception as e:
        print(f"❌ Local WebSocket connection failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_local_websocket())