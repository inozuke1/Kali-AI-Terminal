import React, { useState, useEffect, useRef } from "react";
import "./App.css";
import TerminalComponent from "./components/TerminalComponent";
import HeaderBar from "./components/HeaderBar";
import SidePanel from "./components/SidePanel";
import StatusBar from "./components/StatusBar";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function App() {
  const [websocket, setWebsocket] = useState(null);
  const [aiEnabled, setAIEnabled] = useState(true);
  const [isConnecting, setIsConnecting] = useState(false);
  const reconnectTimeoutRef = useRef(null);

  const connectWebSocket = () => {
    if (isConnecting) return;
    
    setIsConnecting(true);
    const wsUrl = BACKEND_URL.replace('https://', 'wss://').replace('http://', 'ws://') + '/ws';
    
    try {
      const ws = new WebSocket(wsUrl);
      
      ws.onopen = () => {
        console.log('✅ Connected to Kali AI Terminal');
        setWebsocket(ws);
        setIsConnecting(false);
        
        // Clear any existing reconnection timeout
        if (reconnectTimeoutRef.current) {
          clearTimeout(reconnectTimeoutRef.current);
          reconnectTimeoutRef.current = null;
        }
      };
      
      ws.onclose = (event) => {
        console.log('❌ WebSocket connection closed', event.code, event.reason);
        setWebsocket(null);
        setIsConnecting(false);
        
        // Attempt to reconnect after 3 seconds
        if (!reconnectTimeoutRef.current) {
          reconnectTimeoutRef.current = setTimeout(() => {
            console.log('🔄 Attempting to reconnect...');
            connectWebSocket();
          }, 3000);
        }
      };
      
      ws.onerror = (error) => {
        console.error('❌ WebSocket error:', error);
        setIsConnecting(false);
      };
      
    } catch (error) {
      console.error('❌ Failed to create WebSocket connection:', error);
      setIsConnecting(false);
    }
  };

  useEffect(() => {
    connectWebSocket();
    
    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (websocket) {
        websocket.close();
      }
    };
  }, []);

  const handleAIToggle = () => {
    setAIEnabled(!aiEnabled);
  };

  return (
    <div className="App h-screen bg-black text-green-400 font-mono overflow-hidden">
      {/* Cyberpunk Background Effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-black via-gray-900 to-black">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 left-0 w-full h-full bg-green-900/5 animate-pulse"></div>
        </div>
        
        {/* Matrix-style rain effect (CSS animation) */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="matrix-rain"></div>
        </div>
      </div>

      {/* Main Interface */}
      <div className="relative z-10 flex flex-col h-full">
        {/* Header */}
        <HeaderBar 
          websocket={websocket} 
          onAIToggle={handleAIToggle}
          aiEnabled={aiEnabled}
        />
        
        {/* Main Content */}
        <div className="flex-1 flex overflow-hidden">
          {/* Terminal Section */}
          <div className="flex-1 p-4">
            <TerminalComponent 
              websocket={websocket}
              aiEnabled={aiEnabled}
            />
          </div>
          
          {/* Side Panel */}
          <SidePanel 
            websocket={websocket}
            className="w-80 flex-shrink-0"
          />
        </div>
        
        {/* Status Bar */}
        <StatusBar 
          websocket={websocket}
          className="flex-shrink-0"
        />
      </div>

      {/* Connection Loading Overlay */}
      {isConnecting && (
        <div className="absolute inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-green-500 mb-4"></div>
            <p className="text-green-400 text-lg font-bold">Connecting to Kali AI Terminal...</p>
            <p className="text-gray-400 text-sm mt-2">Establishing secure WebSocket connection</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;