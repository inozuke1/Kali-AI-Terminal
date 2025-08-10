"""
Simple WebSocket test script to debug the command execution issue
"""
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://127.0.0.1:8000/ws"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket!")
            
            # Test command
            test_command = {
                "type": "execute_command",
                "payload": {
                    "command": "echo Hello World",
                    "context": {}
                }
            }
            
            print(f"Sending: {test_command}")
            await websocket.send(json.dumps(test_command))
            
            # Wait for response
            response = await websocket.recv()
            response_data = json.loads(response)
            
            print(f"Received: {response_data}")
            
            # Check what's in the response
            if response_data.get("type") == "command_result":
                payload = response_data.get("payload", {})
                print(f"Payload keys: {list(payload.keys())}")
                print(f"Success: {payload.get('success')}")
                print(f"Output: '{payload.get('output')}'")
                print(f"Error: '{payload.get('error')}'")
                
    except Exception as e:
        print(f"WebSocket test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket())