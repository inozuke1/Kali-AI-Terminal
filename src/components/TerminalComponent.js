import React, { useState, useEffect, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Send, 
  Brain, 
  Zap, 
  Terminal as TerminalIcon,
  Command,
  ChevronRight,
  Clock,
  CheckCircle,
  AlertTriangle,
  XCircle,
  Loader,
  Sparkles
} from 'lucide-react';

const TerminalComponent = ({ isAIActive }) => {
  const [currentCommand, setCurrentCommand] = useState('');
  const [commandHistory, setCommandHistory] = useState([]);
  const [output, setOutput] = useState([
    {
      type: 'system',
      content: 'Kali AI Terminal v1.0.0 - Initializing...',
      timestamp: new Date().toLocaleTimeString()
    },
    {
      type: 'success',
      content: 'AI Assistant: Ready for penetration testing commands',
      timestamp: new Date().toLocaleTimeString()
    },
    {
      type: 'info',
      content: 'Type "help" for available commands or use natural language',
      timestamp: new Date().toLocaleTimeString()
    }
  ]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [aiSuggestions, setAiSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [historyIndex, setHistoryIndex] = useState(-1);
  const [currentPath, setCurrentPath] = useState('~/kali');
  const [websocket, setWebsocket] = useState(null);

  const terminalRef = useRef(null);
  const inputRef = useRef(null);
  const outputRef = useRef(null);

  // Initialize WebSocket connection with retry logic
  useEffect(() => {
    let ws = null;
    let reconnectTimeout = null;
    let reconnectAttempts = 0;
    const maxReconnectAttempts = 5;
    const reconnectDelay = 3000; // 3 seconds

    const connectWebSocket = () => {
      try {
        ws = new WebSocket('ws://127.0.0.1:8000/ws');
        
        ws.onopen = () => {
          console.log('WebSocket connected');
          reconnectAttempts = 0; // Reset attempts on successful connection
          setWebsocket(ws); // Set websocket state only when connection is established
          setOutput(prev => [...prev, {
            type: 'success',
            content: 'Connected to Kali AI Backend',
            timestamp: new Date().toLocaleTimeString()
          }]);
        };

        ws.onmessage = (event) => {
          try {
            const message = JSON.parse(event.data);
            handleWebSocketMessage(message);
          } catch (e) {
            console.error('Failed to parse WebSocket message:', e);
          }
        };

        ws.onclose = (event) => {
          console.log('WebSocket disconnected', event.code, event.reason);
          
          if (reconnectAttempts < maxReconnectAttempts) {
            setOutput(prev => [...prev, {
              type: 'warning',
              content: `Connection lost. Reconnecting... (${reconnectAttempts + 1}/${maxReconnectAttempts})`,
              timestamp: new Date().toLocaleTimeString()
            }]);
            
            reconnectTimeout = setTimeout(() => {
              reconnectAttempts++;
              connectWebSocket();
            }, reconnectDelay);
          } else {
            setOutput(prev => [...prev, {
              type: 'error',
              content: 'Failed to connect to backend after multiple attempts. Using offline mode.',
              timestamp: new Date().toLocaleTimeString()
            }]);
          }
        };

        ws.onerror = (error) => {
          console.error('WebSocket error:', error);
          if (reconnectAttempts === 0) {
            setOutput(prev => [...prev, {
              type: 'error',
              content: 'Backend connection failed. Make sure the backend is running.',
              timestamp: new Date().toLocaleTimeString()
            }]);
          }
        };

        setWebsocket(ws);
      } catch (error) {
        console.error('Failed to create WebSocket connection:', error);
        setOutput(prev => [...prev, {
          type: 'error',
          content: 'Failed to initialize WebSocket connection',
          timestamp: new Date().toLocaleTimeString()
        }]);
      }
    };

    // Initial connection attempt with a small delay
    const initialTimeout = setTimeout(connectWebSocket, 1000);

    return () => {
      if (reconnectTimeout) clearTimeout(reconnectTimeout);
      if (initialTimeout) clearTimeout(initialTimeout);
      if (ws && ws.readyState !== WebSocket.CLOSED) {
        ws.close();
      }
    };
  }, []);

  // Handle WebSocket messages
  const handleWebSocketMessage = (message) => {
    switch (message.type) {
      case 'command_result':
        setOutput(prev => [...prev, {
          type: 'output',
          content: message.payload.output || message.payload.result || 'Command executed',
          timestamp: new Date().toLocaleTimeString()
        }]);
        setIsProcessing(false);
        break;
      case 'ai_response':
        setOutput(prev => [...prev, {
          type: 'ai',
          content: message.payload.response || message.payload.message,
          timestamp: new Date().toLocaleTimeString()
        }]);
        setIsProcessing(false);
        break;
      case 'scan_result':
        setOutput(prev => [...prev, {
          type: 'scan',
          content: `Scan Progress: ${message.payload.progress}% - ${message.payload.current_phase}`,
          timestamp: new Date().toLocaleTimeString()
        }]);
        break;
      case 'error':
        setOutput(prev => [...prev, {
          type: 'error',
          content: message.payload.message || 'An error occurred',
          timestamp: new Date().toLocaleTimeString()
        }]);
        setIsProcessing(false);
        break;
      default:
        console.log('Unknown message type:', message.type);
    }
  };

  // Auto-scroll to bottom
  useEffect(() => {
    if (outputRef.current) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight;
    }
  }, [output]);

  // Focus terminal input
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  // AI Command Suggestions
  const getAISuggestions = useCallback(async (input) => {
    if (!isAIActive || input.length < 2) {
      setAiSuggestions([]);
      setShowSuggestions(false);
      return;
    }

    const suggestions = [];
    
    // Security tool suggestions
    if (input.toLowerCase().includes('scan')) {
      suggestions.push('nmap -sS -O target_ip', 'masscan -p1-1000 target_ip', 'nmap -sV --script vuln target_ip');
    }
    if (input.toLowerCase().includes('exploit')) {
      suggestions.push('msfconsole', 'searchsploit keyword', 'use exploit/multi/handler');
    }
    if (input.toLowerCase().includes('brute')) {
      suggestions.push('hydra -l admin -P passwords.txt ssh://target_ip', 'john --wordlist=rockyou.txt hashes.txt');
    }
    if (input.toLowerCase().includes('web')) {
      suggestions.push('dirb http://target_ip', 'sqlmap -u "http://target_ip/page?id=1"', 'nikto -h target_ip');
    }

    // Natural language processing
    const naturalLanguageSuggestions = [
      'scan network for vulnerabilities',
      'enumerate open ports on target',
      'start metasploit framework',
      'brute force SSH credentials',
      'scan web application for SQL injection'
    ];

    if (input.length > 5) {
      suggestions.push(...naturalLanguageSuggestions.filter(s => 
        s.toLowerCase().includes(input.toLowerCase())
      ));
    }

    setAiSuggestions(suggestions.slice(0, 5));
    setShowSuggestions(suggestions.length > 0);
  }, [isAIActive]);

  // Handle command input
  const handleCommandChange = (e) => {
    const value = e.target.value;
    setCurrentCommand(value);
    
    if (isAIActive) {
      getAISuggestions(value);
    }
  };

  // Execute command
  const executeCommand = async () => {
    if (!currentCommand.trim()) return;

    const command = currentCommand.trim();
    
    // Add to history
    setCommandHistory(prev => [...prev, command]);
    setHistoryIndex(-1);

    // Add command to output
    setOutput(prev => [...prev, {
      type: 'command',
      content: `${currentPath}$ ${command}`,
      timestamp: new Date().toLocaleTimeString()
    }]);

    setCurrentCommand('');
    setShowSuggestions(false);
    setIsProcessing(true);

    // Handle built-in commands
    if (command.toLowerCase() === 'clear') {
      setOutput([]);
      setIsProcessing(false);
      return;
    }

    if (command.toLowerCase() === 'help') {
      setOutput(prev => [...prev, {
        type: 'info',
        content: `Available commands:
  • clear - Clear terminal
  • help - Show this help
  • scan <target> - Scan target for vulnerabilities
  • exploit <target> - Search for exploits
  • AI Commands: Use natural language like "scan network for open ports"
  
Security Tools:
  • nmap, masscan - Network scanning
  • metasploit, msfconsole - Exploitation
  • sqlmap - SQL injection testing
  • hydra, john - Password cracking
  • dirb, gobuster - Directory enumeration`,
        timestamp: new Date().toLocaleTimeString()
      }]);
      setIsProcessing(false);
      return;
    }

    // Send command to backend
    console.log('WebSocket check:', {
      websocket: !!websocket,
      readyState: websocket?.readyState,
      WebSocket_OPEN: WebSocket.OPEN,
      comparison: websocket?.readyState === WebSocket.OPEN
    });

    if (websocket && websocket.readyState === WebSocket.OPEN) {
      const message = {
        type: isNaturalLanguage(command) ? 'ai_query' : 'execute_command',
        payload: {
          [isNaturalLanguage(command) ? 'query' : 'command']: command,
          context: {
            currentPath,
            timestamp: new Date().toISOString()
          }
        }
      };
      
      console.log('Sending WebSocket message:', message);
      websocket.send(JSON.stringify(message));
    } else {
      console.log('Falling back to simulation mode - WebSocket not ready');
      // Simulate command execution
      setTimeout(() => {
        setOutput(prev => [...prev, {
          type: 'output',
          content: `Simulated output for: ${command}`,
          timestamp: new Date().toLocaleTimeString()
        }]);
        setIsProcessing(false);
      }, 1000);
    }
  };

  // Check if command is natural language
  const isNaturalLanguage = (command) => {
    const nlIndicators = ['scan', 'find', 'show', 'list', 'what', 'how', 'check', 'test'];
    return nlIndicators.some(indicator => 
      command.toLowerCase().includes(indicator) && command.split(' ').length > 2
    );
  };

  // Handle key presses
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      executeCommand();
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (historyIndex < commandHistory.length - 1) {
        const newIndex = historyIndex + 1;
        setHistoryIndex(newIndex);
        setCurrentCommand(commandHistory[commandHistory.length - 1 - newIndex]);
      }
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (historyIndex > 0) {
        const newIndex = historyIndex - 1;
        setHistoryIndex(newIndex);
        setCurrentCommand(commandHistory[commandHistory.length - 1 - newIndex]);
      } else if (historyIndex === 0) {
        setHistoryIndex(-1);
        setCurrentCommand('');
      }
    } else if (e.key === 'Tab') {
      e.preventDefault();
      if (aiSuggestions.length > 0) {
        setCurrentCommand(aiSuggestions[0]);
        setShowSuggestions(false);
      }
    }
  };

  // Get output icon
  const getOutputIcon = (type) => {
    switch (type) {
      case 'success': return <CheckCircle size={14} className="text-green-400" />;
      case 'error': return <XCircle size={14} className="text-red-400" />;
      case 'warning': return <AlertTriangle size={14} className="text-yellow-400" />;
      case 'ai': return <Brain size={14} className="text-purple-400" />;
      case 'scan': return <Zap size={14} className="text-blue-400" />;
      case 'command': return <ChevronRight size={14} className="text-green-400" />;
      default: return <TerminalIcon size={14} className="text-gray-400" />;
    }
  };

  return (
    <div className="terminal-component" ref={terminalRef}>
      {/* Terminal Output */}
      <div className="terminal-output" ref={outputRef}>
        <AnimatePresence>
          {output.map((line, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className={`output-line ${line.type}`}
            >
              <div className="output-content">
                <div className="output-icon">
                  {getOutputIcon(line.type)}
                </div>
                <div className="output-text">
                  <pre>{line.content}</pre>
                </div>
                <div className="output-timestamp">
                  <Clock size={12} />
                  {line.timestamp}
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {/* Processing indicator */}
        {isProcessing && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="processing-indicator"
          >
            <Loader className="animate-spin" size={14} />
            <span>Processing command...</span>
          </motion.div>
        )}
      </div>

      {/* AI Suggestions */}
      <AnimatePresence>
        {showSuggestions && aiSuggestions.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="ai-suggestions"
          >
            <div className="suggestions-header">
              <Sparkles size={14} />
              <span>AI Suggestions</span>
            </div>
            {aiSuggestions.map((suggestion, index) => (
              <div
                key={index}
                className="suggestion-item"
                onClick={() => {
                  setCurrentCommand(suggestion);
                  setShowSuggestions(false);
                  inputRef.current?.focus();
                }}
              >
                <ChevronRight size={12} />
                <span>{suggestion}</span>
              </div>
            ))}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Command Input */}
      <div className="terminal-input">
        <div className="input-prompt">
          <span className="path">{currentPath}</span>
          <ChevronRight size={16} className="prompt-icon" />
        </div>
        
        <div className="input-container">
          <input
            ref={inputRef}
            type="text"
            value={currentCommand}
            onChange={handleCommandChange}
            onKeyDown={handleKeyPress}
            placeholder={isAIActive ? "Enter command or describe what you want to do..." : "Enter command..."}
            className="command-input"
            disabled={isProcessing}
          />
          
          <div className="input-actions">
            {isAIActive && (
              <motion.div
                animate={{ rotate: isProcessing ? 360 : 0 }}
                transition={{ duration: 1, repeat: isProcessing ? Infinity : 0 }}
                className="ai-indicator-small"
              >
                <Brain size={16} />
              </motion.div>
            )}
            
            <button
              onClick={executeCommand}
              disabled={!currentCommand.trim() || isProcessing}
              className="execute-button"
            >
              <Send size={16} />
            </button>
          </div>
        </div>
      </div>

      {/* Terminal Stats */}
      <div className="terminal-stats">
        <div className="stat">
          <Command size={12} />
          <span>{commandHistory.length} commands</span>
        </div>
        <div className="stat">
          <TerminalIcon size={12} />
          <span>{output.length} lines</span>
        </div>
        {websocket && (
          <div className="stat">
            <div className={`connection-status ${websocket.readyState === WebSocket.OPEN ? 'connected' : 'disconnected'}`}>
              <div className="status-dot"></div>
              <span>{websocket.readyState === WebSocket.OPEN ? 'Connected' : 'Disconnected'}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TerminalComponent;
