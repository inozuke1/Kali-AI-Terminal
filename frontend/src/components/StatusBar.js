import React, { useState, useEffect } from 'react';

const StatusBar = ({ websocket, className }) => {
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const [lastActivity, setLastActivity] = useState(new Date());
  const [messageCount, setMessageCount] = useState(0);
  const [systemLoad, setSystemLoad] = useState({ cpu: 0, memory: 0, network: 0 });
  const [activeScans, setActiveScans] = useState(0);
  const [threatLevel, setThreatLevel] = useState('low');

  useEffect(() => {
    if (websocket) {
      websocket.onopen = () => {
        setConnectionStatus('connected');
        setLastActivity(new Date());
      };

      websocket.onclose = () => {
        setConnectionStatus('disconnected');
      };

      websocket.onerror = () => {
        setConnectionStatus('error');
      };

      const originalOnMessage = websocket.onmessage;
      websocket.onmessage = (event) => {
        const message = JSON.parse(event.data);
        setMessageCount(prev => prev + 1);
        setLastActivity(new Date());

        // Update system stats if received
        if (message.type === 'system_stats' && message.stats) {
          setSystemLoad({
            cpu: message.stats.cpu_percent || 0,
            memory: message.stats.memory_percent || 0,
            network: message.stats.network || 0
          });
        }

        // Track active scans
        if (message.type === 'scan_start') {
          setActiveScans(prev => prev + 1);
        } else if (message.type === 'scan_progress' && message.progress === 100) {
          setActiveScans(prev => Math.max(0, prev - 1));
        }

        if (originalOnMessage) {
          originalOnMessage(event);
        }
      };
    }

    // Update threat level based on system load
    const updateThreatLevel = () => {
      const avgLoad = (systemLoad.cpu + systemLoad.memory) / 2;
      if (avgLoad > 80) setThreatLevel('critical');
      else if (avgLoad > 60) setThreatLevel('high');
      else if (avgLoad > 30) setThreatLevel('medium');
      else setThreatLevel('low');
    };

    updateThreatLevel();
  }, [websocket, systemLoad]);

  const getConnectionStatusInfo = () => {
    switch (connectionStatus) {
      case 'connected':
        return {
          color: 'text-green-400',
          bgColor: 'bg-green-500',
          text: 'ONLINE',
          icon: '🟢'
        };
      case 'disconnected':
        return {
          color: 'text-red-400',
          bgColor: 'bg-red-500',
          text: 'OFFLINE',
          icon: '🔴'
        };
      case 'error':
        return {
          color: 'text-orange-400',
          bgColor: 'bg-orange-500',
          text: 'ERROR',
          icon: '🟡'
        };
      default:
        return {
          color: 'text-gray-400',
          bgColor: 'bg-gray-500',
          text: 'UNKNOWN',
          icon: '⚪'
        };
    }
  };

  const getThreatLevelInfo = () => {
    switch (threatLevel) {
      case 'critical':
        return {
          color: 'text-red-400',
          bgColor: 'bg-red-900/30',
          borderColor: 'border-red-500/50',
          text: 'CRITICAL',
          icon: '🚨'
        };
      case 'high':
        return {
          color: 'text-orange-400',
          bgColor: 'bg-orange-900/30',
          borderColor: 'border-orange-500/50',
          text: 'HIGH',
          icon: '⚠️'
        };
      case 'medium':
        return {
          color: 'text-yellow-400',
          bgColor: 'bg-yellow-900/30',
          borderColor: 'border-yellow-500/50',
          text: 'MEDIUM',
          icon: '⚡'
        };
      case 'low':
        return {
          color: 'text-green-400',
          bgColor: 'bg-green-900/30',
          borderColor: 'border-green-500/50',
          text: 'LOW',
          icon: '✅'
        };
      default:
        return {
          color: 'text-gray-400',
          bgColor: 'bg-gray-900/30',
          borderColor: 'border-gray-500/50',
          text: 'UNKNOWN',
          icon: '❓'
        };
    }
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString([], { hour12: false });
  };

  const getLoadColor = (value) => {
    if (value < 30) return 'text-green-400';
    if (value < 70) return 'text-yellow-400';
    return 'text-red-400';
  };

  const connectionInfo = getConnectionStatusInfo();
  const threatInfo = getThreatLevelInfo();

  return (
    <footer className={`bg-gray-900 border-t-2 border-green-500 shadow-lg ${className}`}>
      <div className="px-6 py-2">
        <div className="flex items-center justify-between">
          {/* Left Section - Connection Status */}
          <div className="flex items-center space-x-6">
            <div className="flex items-center space-x-2">
              <div className={`w-3 h-3 ${connectionInfo.bgColor} rounded-full animate-pulse`}></div>
              <span className={`text-sm font-bold font-mono ${connectionInfo.color}`}>
                {connectionInfo.text}
              </span>
            </div>

            <div className="flex items-center space-x-2 text-sm font-mono">
              <span className="text-gray-400">Last Activity:</span>
              <span className="text-cyan-400">{formatTime(lastActivity)}</span>
            </div>

            <div className="flex items-center space-x-2 text-sm font-mono">
              <span className="text-gray-400">Messages:</span>
              <span className="text-cyan-400">{messageCount}</span>
            </div>
          </div>

          {/* Center Section - System Load */}
          <div className="flex items-center space-x-6">
            <div className="flex items-center space-x-4">
              <div className="text-center">
                <div className="text-xs text-gray-400">CPU</div>
                <div className={`text-sm font-bold font-mono ${getLoadColor(systemLoad.cpu)}`}>
                  {systemLoad.cpu.toFixed(0)}%
                </div>
              </div>

              <div className="text-center">
                <div className="text-xs text-gray-400">RAM</div>
                <div className={`text-sm font-bold font-mono ${getLoadColor(systemLoad.memory)}`}>
                  {systemLoad.memory.toFixed(0)}%
                </div>
              </div>

              <div className="text-center">
                <div className="text-xs text-gray-400">NET</div>
                <div className="text-sm font-bold font-mono text-cyan-400">
                  {systemLoad.network}
                </div>
              </div>
            </div>

            {/* Active Scans */}
            <div className="flex items-center space-x-2">
              <div className={`w-2 h-2 rounded-full ${activeScans > 0 ? 'bg-yellow-500 animate-pulse' : 'bg-gray-500'}`}></div>
              <span className="text-sm font-mono text-gray-400">Scans:</span>
              <span className="text-sm font-bold font-mono text-yellow-400">{activeScans}</span>
            </div>
          </div>

          {/* Right Section - Threat Level */}
          <div className="flex items-center space-x-4">
            <div className={`flex items-center space-x-2 px-3 py-1 rounded border ${threatInfo.bgColor} ${threatInfo.borderColor}`}>
              <span>{threatInfo.icon}</span>
              <span className="text-xs text-gray-400">THREAT:</span>
              <span className={`text-sm font-bold font-mono ${threatInfo.color}`}>
                {threatInfo.text}
              </span>
            </div>

            <div className="text-right">
              <div className="text-xs text-gray-400 font-mono">KALI AI TERMINAL</div>
              <div className="text-xs text-green-400 font-mono">v2.1.0</div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default StatusBar;