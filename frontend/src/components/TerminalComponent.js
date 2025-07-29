import React, { useState, useEffect, useRef } from 'react';

const TerminalComponent = ({ websocket, aiEnabled = true }) => {
  const [history, setHistory] = useState([]);
  const [currentCommand, setCurrentCommand] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const terminalRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    if (websocket) {
      websocket.onopen = () => {
        setIsConnected(true);
        addToHistory('🔗 Connected to Kali AI Terminal', 'system');
        addToHistory('🤖 AI Assistant Ready. Type "help" for commands or "ai:<query>" for AI assistance', 'info');
      };

      websocket.onmessage = (event) => {
        const message = JSON.parse(event.data);
        handleWebSocketMessage(message);
      };

      websocket.onclose = () => {
        setIsConnected(false);
        addToHistory('❌ Disconnected from terminal', 'error');
      };
    }
  }, [websocket]);

  const handleWebSocketMessage = (message) => {
    switch (message.type) {
      case 'connection':
        addToHistory(message.message, 'system');
        break;
      case 'command_result':
        addToHistory(message.result.output, 'output');
        break;
      case 'ai_response':
        addToHistory(`AI: ${message.response}`, 'ai');
        break;
      case 'scan_progress':
        addToHistory(`[${message.progress}%] ${message.details}`, 'progress');
        break;
      default:
        console.log('Unknown message type:', message.type);
    }
  };

  const addToHistory = (text, type = 'output') => {
    const timestamp = new Date().toLocaleTimeString();
    setHistory(prev => [...prev, { text, type, timestamp, id: Date.now() }]);
  };

  const executeCommand = () => {
    if (!currentCommand.trim()) return;

    const cmd = currentCommand.trim();
    addToHistory(`$ ${cmd}`, 'command');

    if (cmd.startsWith('ai:')) {
      // AI query
      const query = cmd.substring(3).trim();
      if (websocket && websocket.readyState === WebSocket.OPEN) {
        websocket.send(JSON.stringify({
          type: 'ai_query',
          query: query,
          context: 'terminal'
        }));
      }
    } else if (cmd === 'clear') {
      setHistory([]);
    } else if (cmd === 'help') {
      addToHistory(`
Available Commands:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Security Tools:
  nmap <target>          - Network discovery and security auditing
  sqlmap <url>           - SQL injection testing
  gobuster <target>      - Directory/file brute-forcing
  nikto <target>         - Web server scanner
  
🤖 AI Commands:
  ai:<query>             - Ask AI assistant anything
  ai:scan <target>       - AI-powered scan analysis
  ai:exploit <info>      - Get AI exploit recommendations
  
📊 System Commands:
  status                 - Show system information
  clear                  - Clear terminal
  help                   - Show this help message
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`, 'info');
    } else if (cmd === 'status') {
      if (websocket && websocket.readyState === WebSocket.OPEN) {
        websocket.send(JSON.stringify({ type: 'system_stats' }));
      }
    } else {
      // Regular command execution
      if (websocket && websocket.readyState === WebSocket.OPEN) {
        websocket.send(JSON.stringify({
          type: 'execute_command',
          command: cmd,
          target: ''
        }));
      } else {
        addToHistory('❌ Not connected to server', 'error');
      }
    }

    setCurrentCommand('');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      executeCommand();
    } else if (e.key === 'ArrowUp') {
      // TODO: Command history navigation
      e.preventDefault();
    }
  };

  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [history]);

  const getTypeClass = (type) => {
    switch (type) {
      case 'command':
        return 'text-cyan-400 font-bold';
      case 'output':
        return 'text-green-300';
      case 'error':
        return 'text-red-400';
      case 'system':
        return 'text-blue-400';
      case 'ai':
        return 'text-purple-400 font-medium';
      case 'info':
        return 'text-yellow-300';
      case 'progress':
        return 'text-orange-400';
      default:
        return 'text-gray-300';
    }
  };

  return (
    <div className="flex flex-col h-full bg-black border border-green-500 rounded-lg shadow-lg shadow-green-500/20">
      {/* Terminal Header */}
      <div className="flex items-center justify-between px-4 py-2 bg-gray-900 border-b border-green-500 rounded-t-lg">
        <div className="flex items-center space-x-2">
          <div className="flex space-x-2">
            <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
            <div className="w-3 h-3 bg-yellow-500 rounded-full animate-pulse delay-75"></div>
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse delay-150"></div>
          </div>
          <span className="text-green-400 font-mono text-sm font-bold">KALI AI TERMINAL</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></div>
          <span className="text-xs text-gray-400 font-mono">
            {isConnected ? 'CONNECTED' : 'DISCONNECTED'}
          </span>
          {aiEnabled && (
            <span className="text-xs text-purple-400 font-mono bg-purple-900/30 px-2 py-1 rounded border border-purple-500/30">
              🤖 AI ENABLED
            </span>
          )}
        </div>
      </div>

      {/* Terminal Output */}
      <div 
        ref={terminalRef}
        className="flex-1 p-4 overflow-y-auto bg-black font-mono text-sm leading-relaxed scrollbar-thin scrollbar-track-gray-900 scrollbar-thumb-green-500"
        style={{ minHeight: '400px' }}
      >
        {history.length === 0 && (
          <div className="text-green-400 animate-pulse">
            <pre className="text-xs">
{`
 ██╗  ██╗ █████╗ ██╗     ██╗     █████╗ ██╗    ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗     
 ██║ ██╔╝██╔══██╗██║     ██║    ██╔══██╗██║    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║     
 █████╔╝ ███████║██║     ██║    ███████║██║       ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║     
 ██╔═██╗ ██╔══██║██║     ██║    ██╔══██║██║       ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║     
 ██║  ██╗██║  ██║███████╗██║    ██║  ██║██║       ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗
 ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝    ╚═╝  ╚═╝╚═╝       ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝
                                                                                                                     
`}
            </pre>
            <p className="mt-4 text-center text-green-300">Welcome to Kali AI Terminal - Your AI-Powered Penetration Testing Environment</p>
            <p className="mt-2 text-center text-gray-400">Type 'help' to get started</p>
          </div>
        )}
        
        {history.map((entry) => (
          <div key={entry.id} className={`mb-1 ${getTypeClass(entry.type)}`}>
            <span className="text-gray-500 text-xs mr-2">[{entry.timestamp}]</span>
            <pre className="whitespace-pre-wrap break-words">{entry.text}</pre>
          </div>
        ))}
      </div>

      {/* Command Input */}
      <div className="flex items-center p-3 bg-gray-900 border-t border-green-500 rounded-b-lg">
        <span className="text-green-400 font-mono mr-2">root@kali:~$</span>
        <input
          ref={inputRef}
          type="text"
          value={currentCommand}
          onChange={(e) => setCurrentCommand(e.target.value)}
          onKeyDown={handleKeyPress}
          className="flex-1 bg-transparent text-green-300 font-mono outline-none placeholder-gray-500"
          placeholder="Enter command or 'ai:<query>' for AI assistance..."
          autoFocus
        />
        <div className="ml-2">
          <div className="w-3 h-5 bg-green-400 animate-pulse"></div>
        </div>
      </div>
    </div>
  );
};

export default TerminalComponent;