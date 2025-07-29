from fastapi import FastAPI, APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import uuid
from datetime import datetime
import json
import asyncio
import subprocess
import psutil
import platform


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        await self.send_personal_message({"type": "connection", "message": "Connected to Kali AI Terminal"}, websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_text(json.dumps(message))

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))

# AI Processing Handler
class AIHandler:
    def __init__(self):
        pass
    
    async def process_query(self, query: str, context: str = "") -> str:
        # Simulate AI processing for now - you can integrate DeepSeek later
        if "scan" in query.lower():
            return f"🔍 AI Analysis: Initiating network scan for target analysis..."
        elif "exploit" in query.lower():
            return f"⚠️  AI Suggestion: Potential vulnerabilities detected. Recommended approach: {query}"
        elif "help" in query.lower():
            return "🤖 AI Assistant: Available commands: scan, exploit, nmap, sqlmap, metasploit, status"
        else:
            return f"🧠 AI Response: Processing '{query}'. Analyzing security context..."

# Security Tools Handler
class SecurityToolsHandler:
    def __init__(self):
        self.tools = ["nmap", "sqlmap", "metasploit", "gobuster", "nikto", "hydra"]
    
    async def execute_command(self, command: str, target: str = "") -> dict:
        try:
            if command.startswith("nmap"):
                return {
                    "tool": "nmap",
                    "status": "running",
                    "output": f"Starting Nmap scan on {target or 'localhost'}...\n",
                    "progress": 10
                }
            elif command.startswith("sqlmap"):
                return {
                    "tool": "sqlmap",
                    "status": "running", 
                    "output": f"SQLMap injection testing on {target}...\n",
                    "progress": 15
                }
            else:
                return {
                    "tool": "terminal",
                    "status": "executed",
                    "output": f"$ {command}\nExecuted: {command}\n",
                    "progress": 100
                }
        except Exception as e:
            return {
                "tool": "error",
                "status": "failed",
                "output": f"Error: {str(e)}\n",
                "progress": 0
            }

# System Monitor
class SystemMonitor:
    @staticmethod
    def get_system_stats():
        try:
            return {
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent,
                "network": len(psutil.net_connections()),
                "processes": len(psutil.pids()),
                "platform": platform.system(),
                "uptime": "Running"
            }
        except:
            return {
                "cpu_percent": 0,
                "memory_percent": 0,
                "disk_percent": 0,
                "network": 0,
                "processes": 0,
                "platform": "Unknown",
                "uptime": "Unknown"
            }

# Initialize managers
manager = ConnectionManager()
ai_handler = AIHandler()
security_tools = SecurityToolsHandler()

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

class CommandRequest(BaseModel):
    command: str
    target: Optional[str] = ""

class AIQueryRequest(BaseModel):
    query: str
    context: Optional[str] = ""

class ScanRequest(BaseModel):
    target: str
    scan_type: str = "basic"

# WebSocket endpoint for real-time communication
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "execute_command":
                command = message.get("command", "")
                target = message.get("target", "")
                
                # Send acknowledgment
                await manager.send_personal_message({
                    "type": "command_start",
                    "command": command,
                    "timestamp": datetime.now().isoformat()
                }, websocket)
                
                # Execute command
                result = await security_tools.execute_command(command, target)
                
                # Send result
                await manager.send_personal_message({
                    "type": "command_result",
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                }, websocket)
                
            elif message["type"] == "ai_query":
                query = message.get("query", "")
                context = message.get("context", "")
                
                # Process AI query
                ai_response = await ai_handler.process_query(query, context)
                
                await manager.send_personal_message({
                    "type": "ai_response",
                    "query": query,
                    "response": ai_response,
                    "timestamp": datetime.now().isoformat()
                }, websocket)
                
            elif message["type"] == "system_stats":
                stats = SystemMonitor.get_system_stats()
                await manager.send_personal_message({
                    "type": "system_stats",
                    "stats": stats,
                    "timestamp": datetime.now().isoformat()
                }, websocket)
                
            elif message["type"] == "scan_target":
                target = message.get("target", "")
                scan_type = message.get("scan_type", "basic")
                
                await manager.send_personal_message({
                    "type": "scan_start",
                    "target": target,
                    "scan_type": scan_type,
                    "timestamp": datetime.now().isoformat()
                }, websocket)
                
                # Simulate scan progress
                for progress in [20, 40, 60, 80, 100]:
                    await asyncio.sleep(1)
                    await manager.send_personal_message({
                        "type": "scan_progress",
                        "target": target,
                        "progress": progress,
                        "details": f"Scanning... {progress}% complete",
                        "timestamp": datetime.now().isoformat()
                    }, websocket)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# API Routes for the penetration testing terminal
@api_router.get("/")
async def root():
    return {"message": "Kali AI Terminal Backend Online", "status": "operational"}

@api_router.get("/system/stats")
async def get_system_stats():
    return SystemMonitor.get_system_stats()

@api_router.post("/command/execute", response_model=Dict)
async def execute_command(request: CommandRequest):
    result = await security_tools.execute_command(request.command, request.target)
    return {"status": "success", "result": result}

@api_router.post("/ai/query", response_model=Dict)
async def ai_query(request: AIQueryRequest):
    response = await ai_handler.process_query(request.query, request.context)
    return {"status": "success", "response": response}

@api_router.post("/scan/target", response_model=Dict)
async def scan_target(request: ScanRequest):
    # This would integrate with actual scanning tools
    return {
        "status": "initiated",
        "target": request.target,
        "scan_type": request.scan_type,
        "scan_id": str(uuid.uuid4())
    }

@api_router.get("/tools/available")
async def get_available_tools():
    return {
        "tools": security_tools.tools,
        "ai_enabled": True,
        "websocket_status": "active"
    }

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
