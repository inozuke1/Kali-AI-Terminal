import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Terminal, 
  Shield, 
  Activity, 
  Target, 
  Zap, 
  Brain, 
  Network, 
  Lock,
  Eye,
  ChevronRight,
  Settings,
  User,
  Wifi,
  HardDrive,
  Cpu
} from 'lucide-react';
import TerminalComponent from './components/TerminalComponent';
import SidePanel from './components/SidePanel';
import HeaderBar from './components/HeaderBar';
import StatusBar from './components/StatusBar';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('terminal');
  const [isAIActive, setIsAIActive] = useState(true);
  const [systemStats, setSystemStats] = useState({
    cpu: 45,
    memory: 67,
    network: 89,
    threats: 3
  });

  const [targets, setTargets] = useState([
    { id: 1, ip: '192.168.1.100', status: 'scanning', risk: 'high' },
    { id: 2, ip: '10.0.0.50', status: 'vulnerable', risk: 'critical' },
    { id: 3, ip: '172.16.0.10', status: 'secure', risk: 'low' }
  ]);

  const [vulnerabilities, setVulnerabilities] = useState([
    { id: 1, type: 'SQL Injection', severity: 'Critical', target: '192.168.1.100' },
    { id: 2, type: 'XSS', severity: 'High', target: '10.0.0.50' },
    { id: 3, type: 'Open Port', severity: 'Medium', target: '172.16.0.10' }
  ]);

  useEffect(() => {
    // Simulate real-time system monitoring
    const interval = setInterval(() => {
      setSystemStats(prev => ({
        cpu: Math.max(20, Math.min(90, prev.cpu + (Math.random() - 0.5) * 10)),
        memory: Math.max(30, Math.min(95, prev.memory + (Math.random() - 0.5) * 8)),
        network: Math.max(40, Math.min(100, prev.network + (Math.random() - 0.5) * 15)),
        threats: Math.max(0, Math.min(10, prev.threats + Math.floor((Math.random() - 0.7) * 2)))
      }));
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  const glitchAnimation = {
    initial: { opacity: 0.8 },
    animate: { 
      opacity: [0.8, 1, 0.9, 1],
      textShadow: [
        '0 0 5px #00ff41',
        '2px 0 0 #ff0000, -2px 0 0 #00ff41',
        '0 0 5px #00ff41',
        '0 0 5px #00ff41'
      ]
    },
    transition: { 
      duration: 0.5, 
      repeat: Infinity, 
      repeatType: 'loop',
      ease: 'easeInOut'
    }
  };

  return (
    <div className="app-container">
      {/* Background Grid Effect */}
      <div className="grid-background"></div>
      
      {/* Matrix Rain Effect */}
      <div className="matrix-rain">
        {[...Array(20)].map((_, i) => (
          <div key={i} className="matrix-column" style={{ left: `${i * 5}%` }}>
            {[...Array(20)].map((_, j) => (
              <span key={j} className="matrix-char">
                {String.fromCharCode(0x30A0 + Math.random() * 96)}
              </span>
            ))}
          </div>
        ))}
      </div>

      {/* Main Application */}
      <div className="main-container">
        <HeaderBar 
          isAIActive={isAIActive}
          setIsAIActive={setIsAIActive}
          systemStats={systemStats}
        />

        <div className="content-area">
          <div className="terminal-section">
            <div className="terminal-header">
              <div className="terminal-title">
                <motion.div 
                  className="title-text"
                  {...glitchAnimation}
                >
                  <Terminal className="terminal-icon" />
                  <span>KALI AI TERMINAL</span>
                  <div className="ai-indicator">
                    {isAIActive && (
                      <motion.div
                        animate={{
                          boxShadow: [
                            '0 0 10px #00ff41',
                            '0 0 20px #00ff41',
                            '0 0 10px #00ff41'
                          ]
                        }}
                        transition={{ duration: 2, repeat: Infinity }}
                        className="ai-pulse"
                      >
                        <Brain size={16} />
                      </motion.div>
                    )}
                  </div>
                </motion.div>
              </div>
              
              <div className="terminal-controls">
                <div className="window-controls">
                  <span className="control minimize"></span>
                  <span className="control maximize"></span>
                  <span className="control close"></span>
                </div>
              </div>
            </div>

            <TerminalComponent isAIActive={isAIActive} />
          </div>

          <SidePanel 
            targets={targets}
            vulnerabilities={vulnerabilities}
            systemStats={systemStats}
            activeTab={activeTab}
            setActiveTab={setActiveTab}
          />
        </div>

        <StatusBar systemStats={systemStats} />
      </div>

      {/* Floating AI Assistant */}
      <AnimatePresence>
        {isAIActive && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8, x: 50 }}
            animate={{ opacity: 1, scale: 1, x: 0 }}
            exit={{ opacity: 0, scale: 0.8, x: 50 }}
            className="ai-assistant-float"
          >
            <div className="ai-avatar">
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
              >
                <Brain className="ai-brain" />
              </motion.div>
            </div>
            <div className="ai-status">
              <div className="ai-text">AI ACTIVE</div>
              <div className="ai-subtext">Analyzing...</div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Scan Lines Effect */}
      <div className="scan-lines"></div>
    </div>
  );
}

export default App;
