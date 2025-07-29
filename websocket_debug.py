#!/usr/bin/env python3
"""
Debug WebSocket connection to understand the issue
"""

import asyncio
import json
import websockets
import ssl

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
WS_URL = BACKEND_URL.replace('https://', 'wss://').replace('http://', 'ws://') + "/ws"

print(f"🔧 WebSocket URL: {WS_URL}")

async def debug_websocket():
    try:
        # Create SSL context that doesn't verify certificates (for testing)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        print("🔌 Attempting WebSocket connection...")
        async with websockets.connect(WS_URL, ssl=ssl_context, timeout=10) as websocket:
            print("✅ WebSocket connected successfully!")
            
            # Listen for initial messages
            print("📡 Listening for initial messages...")
            try:
                for i in range(3):  # Listen for up to 3 messages
                    message = await asyncio.wait_for(websocket.recv(), timeout=5)
                    print(f"📨 Message {i+1}: {message}")
                    
                    try:
                        parsed = json.loads(message)
                        print(f"📋 Parsed JSON: {parsed}")
                    except:
                        print(f"⚠️  Not valid JSON: {message}")
                        
            except asyncio.TimeoutError:
                print("⏰ No more messages received (timeout)")
            
            # Try sending a test message
            print("\n📤 Sending test message...")
            test_msg = {"type": "system_stats"}
            await websocket.send(json.dumps(test_msg))
            
            # Wait for response
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5)
                print(f"📨 Response: {response}")
                
                try:
                    parsed_response = json.loads(response)
                    print(f"📋 Parsed Response: {parsed_response}")
                except:
                    print(f"⚠️  Response not valid JSON: {response}")
                    
            except asyncio.TimeoutError:
                print("⏰ No response received (timeout)")
                
    except Exception as e:
        print(f"❌ WebSocket connection failed: {str(e)}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    asyncio.run(debug_websocket())