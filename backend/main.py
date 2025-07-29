async def handle_natural_language_request(websocket: WebSocket, payload: Dict):
    """Handle natural language requests for workflows"""
    try:
        request_text = payload.get("request", "")
        context = payload.get("context", {})

        logger.info(f"Processing natural language request: {request_text}")

        # Process through workflow engine
        response = await workflow_engine.process_natural_language_request(request_text, context)

        await connection_manager.send_message(websocket, {
            "type": "workflow_response",
            "payload": response
        })

    except Exception as e:
        logger.error(f"Natural language processing error: {str(e)}")
        await connection_manager.send_message(websocket, {
            "type": "error",
            "payload": {"message": f"Workflow processing failed: {str(e)}"}
        })

async def handle_workflow_status(websocket: WebSocket, payload: Dict):
    """Handle workflow status requests"""
    try:
        status = workflow_engine.get_workflow_status()

        await connection_manager.send_message(websocket, {
            "type": "workflow_status",
            "payload": status
        })

    except Exception as e:
        logger.error(f"Workflow status error: {str(e)}")
        await connection_manager.send_message(websocket, {
            "type": "error",
            "payload": {"message": f"Workflow status request failed: {str(e)}"}
        })

"""
KALI AI TERMINAL - Main FastAPI Application
Advanced Security Terminal with AI Intelligence
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import json
from datetime import datetime
from typing import Dict, List, Optional

from core.ai_assistant import KaliAIAssistant
from core.command_engine import IntelligentCommandEngine
from core.security_tools import SecurityToolManager
from core.vulnerability_scanner import VulnerabilityScanner
from core.network_monitor import NetworkMonitor
from core.workflow_engine import AdvancedWorkflowEngine
from utils.websocket_manager import ConnectionManager
from utils.logger import setup_logger

# Setup logging
logger = setup_logger(__name__)

# Global instances
ai_assistant = None
command_engine = None
security_tools = None
vulnerability_scanner = None
network_monitor = None
workflow_engine = None
connection_manager = ConnectionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global ai_assistant, command_engine, security_tools, vulnerability_scanner, network_monitor, workflow_engine
    
    logger.info("Starting Kali AI Terminal Backend...")
    
    # Initialize core components
    ai_assistant = KaliAIAssistant()
    command_engine = IntelligentCommandEngine()
    security_tools = SecurityToolManager()
    vulnerability_scanner = VulnerabilityScanner()
    network_monitor = NetworkMonitor()
    workflow_engine = AdvancedWorkflowEngine()
    
    # Start background tasks
    asyncio.create_task(network_monitor.start_monitoring())
    asyncio.create_task(vulnerability_scanner.start_continuous_scan())
    
    logger.info("All systems initialized successfully")
    
    yield
    
    logger.info("Shutting down Kali AI Terminal Backend...")
    # Cleanup resources
    await network_monitor.stop_monitoring()
    await vulnerability_scanner.stop_scan()

# Create FastAPI app
app = FastAPI(
    title="Kali AI Terminal Backend",
    description="Advanced AI-powered security terminal backend",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Kali AI Terminal Backend",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "components": {
            "ai_assistant": ai_assistant.is_ready() if ai_assistant else False,
            "command_engine": command_engine.is_ready() if command_engine else False,
            "security_tools": security_tools.is_ready() if security_tools else False,
            "vulnerability_scanner": vulnerability_scanner.is_ready() if vulnerability_scanner else False,
            "network_monitor": network_monitor.is_ready() if network_monitor else False,
            "workflow_engine": workflow_engine.is_ready() if workflow_engine else False
        },
        "timestamp": datetime.now().isoformat()
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Main WebSocket endpoint for real-time communication"""
    await connection_manager.connect(websocket)
    logger.info("New WebSocket connection established")
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            message_type = message.get("type")
            payload = message.get("payload", {})
            
            logger.info(f"Received message: {message_type}")
            
            # Route message to appropriate handler
            if message_type == "execute_command":
                await handle_command_execution(websocket, payload)
            elif message_type == "ai_query":
                await handle_ai_query(websocket, payload)
            elif message_type == "scan_target":
                await handle_target_scan(websocket, payload)
            elif message_type == "get_system_status":
                await handle_system_status(websocket, payload)
            elif message_type == "tool_operation":
                await handle_tool_operation(websocket, payload)
            elif message_type == "natural_language_request":
                await handle_natural_language_request(websocket, payload)
            elif message_type == "workflow_status":
                await handle_workflow_status(websocket, payload)
            else:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "payload": {"message": f"Unknown message type: {message_type}"}
                }))
                
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        logger.info("WebSocket connection closed")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await connection_manager.send_message(websocket, {
            "type": "error",
            "payload": {"message": str(e)}
        })

async def handle_command_execution(websocket: WebSocket, payload: Dict):
    """Handle command execution requests"""
    try:
        command = payload.get("command", "")
        context = payload.get("context", {})
        
        logger.info(f"Executing command: {command}")
        
        # Process command through AI engine
        result = await command_engine.process_command(command, context)
        
        # Send result back to client
        await connection_manager.send_message(websocket, {
            "type": "command_result",
            "payload": result
        })
        
    except Exception as e:
        logger.error(f"Command execution error: {str(e)}")
        await connection_manager.send_message(websocket, {
            "type": "error",
            "payload": {"message": f"Command execution failed: {str(e)}"}
        })

async def handle_ai_query(websocket: WebSocket, payload: Dict):
    """Handle AI assistant queries"""
    try:
        query = payload.get("query", "")
        context = payload.get("context", {})
        
        logger.info(f"AI query: {query}")
        
        # Process through AI assistant
        response = await ai_assistant.process_query(query, context)
        
        await connection_manager.send_message(websocket, {
            "type": "ai_response",
            "payload": response
        })
        
    except Exception as e:
        logger.error(f"AI query error: {str(e)}")
        await connection_manager.send_message(websocket, {
            "type": "error",
            "payload": {"message": f"AI query failed: {str(e)}"}
        })

async def handle_target_scan(websocket: WebSocket, payload: Dict):
    """Handle target scanning requests"""
    try:
        target = payload.get("target", "")
        scan_type = payload.get("scan_type", "basic")
        
        logger.info(f"Scanning target: {target}")
        
        # Start vulnerability scan
        scan_id = await vulnerability_scanner.start_scan(target, scan_type)
        
        await connection_manager.send_message(websocket, {
            "type": "scan_started",
            "payload": {"scan_id": scan_id, "target": target}
        })
        
        # Stream scan results
        async for result in vulnerability_scanner.get_scan_results(scan_id):
            await connection_manager.send_message(websocket, {
                "type": "scan_result",
                "payload": result
            })
            
    except Exception as e:
        logger.error(f"Target scan error: {str(e)}")
        await connection_manager.send_message(websocket, {
            "type": "error",
            "payload": {"message": f"Target scan failed: {str(e)}"}
        })

async def handle_system_status(websocket: WebSocket, payload: Dict):
    """Handle system status requests"""
    try:
        status = await network_monitor.get_system_status()
        
        await connection_manager.send_message(websocket, {
            "type": "system_status",
            "payload": status
        })
        
    except Exception as e:
        logger.error(f"System status error: {str(e)}")
        await connection_manager.send_message(websocket, {
            "type": "error",
            "payload": {"message": f"System status failed: {str(e)}"}
        })

async def handle_tool_operation(websocket: WebSocket, payload: Dict):
    """Handle security tool operations"""
    try:
        tool_name = payload.get("tool", "")
        operation = payload.get("operation", "")
        params = payload.get("params", {})
        
        logger.info(f"Tool operation: {tool_name} - {operation}")
        
        result = await security_tools.execute_tool_operation(tool_name, operation, params)
        
        await connection_manager.send_message(websocket, {
            "type": "tool_result",
            "payload": result
        })
        
    except Exception as e:
        logger.error(f"Tool operation error: {str(e)}")
        await connection_manager.send_message(websocket, {
            "type": "error",
            "payload": {"message": f"Tool operation failed: {str(e)}"}
        })

@app.get("/api/targets")
async def get_targets():
    """Get list of targets"""
    return await vulnerability_scanner.get_targets()

@app.get("/api/vulnerabilities")
async def get_vulnerabilities():
    """Get list of vulnerabilities"""
    return await vulnerability_scanner.get_vulnerabilities()

@app.get("/api/tools")
async def get_available_tools():
    """Get list of available security tools"""
    return await security_tools.get_available_tools()

@app.get("/api/system/stats")
async def get_system_stats():
    """Get system statistics"""
    return await network_monitor.get_system_stats()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
