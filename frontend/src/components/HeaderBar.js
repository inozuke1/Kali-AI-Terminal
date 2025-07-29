import React, { useState, useEffect } from 'react';

const HeaderBar = ({ websocket, onAIToggle, aiEnabled = true }) => {
  const [systemStats, setSystemStats] = useState({
    cpu_percent: 0,
    memory_percent: 0,
    network: 0,
    uptime: 'Loading...'
  });
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    // Update time every second
    const timeInterval = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    // Request system stats every 5 seconds
    const statsInterval = setInterval(() => {
      if (websocket && websocket.readyState === WebSocket.OPEN) {
        websocket.send(JSON.stringify({ type: 'system_stats' }));
      }
    }, 5000);

    // WebSocket message handler for system stats
    if (websocket) {
      const originalOnMessage = websocket.onmessage;
      websocket.onmessage = (event) => {
        const message = JSON.parse(event.data);
        if (message.type === 'system_stats') {
          setSystemStats(message.stats);
        }
        if (originalOnMessage) {
          originalOnMessage(event);
        }
      };
    }

    return () => {
      clearInterval(timeInterval);
      clearInterval(statsInterval);
    };
  }, [websocket]);

  const getStatColor = (value, type = 'percent') => {
    if (type === 'percent') {
      if (value < 30) return 'text-green-400';
      if (value < 70) return 'text-yellow-400';
      return 'text-red-400';
    }
    return 'text-cyan-400';
  };

  const getStatBar = (value) => {
    return (
      <div className="w-16 h-2 bg-gray-700 rounded-full overflow-hidden">
        <div 
          className={`h-full transition-all duration-500 ${
            value < 30 ? 'bg-green-500' : value < 70 ? 'bg-yellow-500' : 'bg-red-500'
          }`}
          style={{ width: `${Math.min(value, 100)}%` }}
        ></div>
      </div>
    );
  };

  return (
    <header className="bg-gray-900 border-b-2 border-green-500 shadow-lg shadow-green-500/10">
      <div className="px-6 py-4">
        {/* Top Row */}
        <div className="flex items-center justify-between mb-3">
          {/* Logo and Title */}
          <div className="flex items-center space-x-4">
            <div className="relative">
              <div className="w-10 h-10 bg-green-500 rounded-lg flex items-center justify-center shadow-lg shadow-green-500/50">
                <span className="text-black font-bold text-lg">K</span>
                <div className="absolute -inset-1 bg-green-500 rounded-lg opacity-30 animate-pulse"></div>
              </div>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white tracking-wide">
                KALI <span className="text-green-400">AI</span> TERMINAL
              </h1>
              <p className="text-sm text-gray-400">AI-Powered Penetration Testing Environment</p>
            </div>
          </div>

          {/* AI Controls */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2 bg-gray-800 px-4 py-2 rounded-lg border border-purple-500/30">
              <div className={`w-3 h-3 rounded-full ${aiEnabled ? 'bg-purple-500 animate-pulse' : 'bg-gray-500'}`}></div>
              <span className="text-purple-400 font-mono text-sm">AI ENGINE</span>
              <button
                onClick={onAIToggle}
                className={`px-3 py-1 rounded text-xs font-bold transition-all ${
                  aiEnabled 
                    ? 'bg-purple-600 text-white hover:bg-purple-700' 
                    : 'bg-gray-600 text-gray-300 hover:bg-gray-500'
                }`}
              >
                {aiEnabled ? 'ON' : 'OFF'}
              </button>
            </div>

            {/* Time Display */}
            <div className="text-right">
              <div className="text-green-400 font-mono text-lg font-bold">
                {currentTime.toLocaleTimeString()}
              </div>
              <div className="text-gray-400 font-mono text-xs">
                {currentTime.toLocaleDateString()}
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Row - System Stats */}
        <div className="flex items-center justify-between">
          {/* System Metrics */}
          <div className="flex items-center space-x-8">
            {/* CPU */}
            <div className="flex items-center space-x-3">
              <div className="text-center">
                <div className="text-xs text-gray-400 font-mono">CPU</div>
                <div className={`text-sm font-bold font-mono ${getStatColor(systemStats.cpu_percent)}`}>
                  {systemStats.cpu_percent.toFixed(1)}%
                </div>
              </div>
              {getStatBar(systemStats.cpu_percent)}
            </div>

            {/* Memory */}
            <div className="flex items-center space-x-3">
              <div className="text-center">
                <div className="text-xs text-gray-400 font-mono">RAM</div>
                <div className={`text-sm font-bold font-mono ${getStatColor(systemStats.memory_percent)}`}>
                  {systemStats.memory_percent.toFixed(1)}%
                </div>
              </div>
              {getStatBar(systemStats.memory_percent)}
            </div>

            {/* Network */}
            <div className="flex items-center space-x-3">
              <div className="text-center">
                <div className="text-xs text-gray-400 font-mono">NET</div>
                <div className="text-sm font-bold font-mono text-cyan-400">
                  {systemStats.network}
                </div>
              </div>
              <div className="w-3 h-3 bg-cyan-500 rounded-full animate-pulse"></div>
            </div>
          </div>

          {/* Status Indicators */}
          <div className="flex items-center space-x-4">
            {/* Connection Status */}
            <div className="flex items-center space-x-2 bg-gray-800 px-3 py-1 rounded border border-green-500/30">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-green-400 font-mono text-xs">ONLINE</span>
            </div>

            {/* Security Level */}
            <div className="flex items-center space-x-2 bg-gray-800 px-3 py-1 rounded border border-red-500/30">
              <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
              <span className="text-red-400 font-mono text-xs">HIGH ALERT</span>
            </div>

            {/* Uptime */}
            <div className="text-right">
              <div className="text-xs text-gray-400 font-mono">UPTIME</div>
              <div className="text-sm font-bold font-mono text-blue-400">
                {systemStats.uptime}
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default HeaderBar;