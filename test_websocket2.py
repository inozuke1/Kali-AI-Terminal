"""
Test Windows commands through WebSocket
"""
import asyncio
import websockets
import json

async def test_commands():
    uri = "ws://127.0.0.1:8000/ws"
    
    commands = [
        "dir",
        "whoami", 
        "ipconfig"
    ]
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket!")
            
            for cmd in commands:
                print(f"\n--- Testing command: {cmd} ---")
                
                test_command = {
                    "type": "execute_command",
                    "payload": {
                        "command": cmd,
                        "context": {}
                    }
                }
                
                await websocket.send(json.dumps(test_command))
                response = await websocket.recv()
                response_data = json.loads(response)
                
                if response_data.get("type") == "command_result":
                    payload = response_data.get("payload", {})
                    print(f"Success: {payload.get('success')}")
                    print(f"Output length: {len(payload.get('output', ''))}")
                    print(f"Output preview: {repr(payload.get('output', '')[:100])}")
                    if payload.get('error'):
                        print(f"Error: {payload.get('error')}")
                
    except Exception as e:
        print(f"WebSocket test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_commands())