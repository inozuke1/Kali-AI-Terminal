import React, { useState, useEffect } from 'react';

const SidePanel = ({ websocket, className }) => {
  const [activeTab, setActiveTab] = useState('targets');
  const [targets, setTargets] = useState([
    { id: 1, ip: '192.168.1.1', hostname: 'gateway.local', status: 'active', ports: '22,80,443' },
    { id: 2, ip: '192.168.1.100', hostname: 'workstation-01', status: 'scanning', ports: '135,139,445' },
  ]);
  const [vulnerabilities, setVulnerabilities] = useState([
    { id: 1, severity: 'high', target: '192.168.1.100', vuln: 'SMB Signing Disabled', cve: 'CVE-2020-1472' },
    { id: 2, severity: 'medium', target: '192.168.1.1', vuln: 'Weak SSH Configuration', cve: 'N/A' },
  ]);
  const [scanTarget, setScanTarget] = useState('');
  const [tools] = useState([
    { name: 'Nmap', description: 'Network Discovery', icon: '🔍', status: 'ready' },
    { name: 'SQLMap', description: 'SQL Injection', icon: '💉', status: 'ready' },
    { name: 'Metasploit', description: 'Exploitation', icon: '💥', status: 'ready' },
    { name: 'Gobuster', description: 'Directory Brute Force', icon: '📁', status: 'ready' },
    { name: 'Nikto', description: 'Web Scanner', icon: '🌐', status: 'ready' },
    { name: 'Hydra', description: 'Password Cracker', icon: '🔐', status: 'ready' },
  ]);

  const tabs = [
    { id: 'targets', name: 'Targets', icon: '🎯' },
    { id: 'vulns', name: 'Vulnerabilities', icon: '⚠️' },
    { id: 'tools', name: 'Tools', icon: '🛠️' },
    { id: 'ai', name: 'AI Assistant', icon: '🤖' },
  ];

  const startScan = () => {
    if (!scanTarget.trim()) return;
    
    if (websocket && websocket.readyState === WebSocket.OPEN) {
      websocket.send(JSON.stringify({
        type: 'scan_target',
        target: scanTarget,
        scan_type: 'comprehensive'
      }));
      
      // Add target to list with scanning status
      const newTarget = {
        id: Date.now(),
        ip: scanTarget,
        hostname: 'resolving...',
        status: 'scanning',
        ports: '...'
      };
      setTargets(prev => [...prev, newTarget]);
    }
    
    setScanTarget('');
  };

  const getSeverityColor = (severity) => {
    switch (severity.toLowerCase()) {
      case 'critical':
        return 'text-red-400 bg-red-900/20 border-red-500/30';
      case 'high':
        return 'text-orange-400 bg-orange-900/20 border-orange-500/30';
      case 'medium':
        return 'text-yellow-400 bg-yellow-900/20 border-yellow-500/30';
      case 'low':
        return 'text-green-400 bg-green-900/20 border-green-500/30';
      default:
        return 'text-gray-400 bg-gray-900/20 border-gray-500/30';
    }
  };

  const getStatusColor = (status) => {
    switch (status.toLowerCase()) {
      case 'active':
        return 'text-green-400';
      case 'scanning':
        return 'text-yellow-400 animate-pulse';
      case 'offline':
        return 'text-red-400';
      case 'ready':
        return 'text-cyan-400';
      default:
        return 'text-gray-400';
    }
  };

  const runTool = (toolName) => {
    if (websocket && websocket.readyState === WebSocket.OPEN) {
      const command = toolName.toLowerCase();
      websocket.send(JSON.stringify({
        type: 'execute_command',
        command: command,
        target: ''
      }));
    }
  };

  const renderTargetsTab = () => (
    <div className="space-y-4">
      {/* Add Target */}
      <div className="bg-gray-900 rounded-lg border border-green-500/30 p-3">
        <h3 className="text-sm font-bold text-green-400 mb-2">🎯 Add New Target</h3>
        <div className="flex space-x-2">
          <input
            type="text"
            value={scanTarget}
            onChange={(e) => setScanTarget(e.target.value)}
            placeholder="IP address or hostname"
            className="flex-1 bg-black border border-gray-600 rounded px-2 py-1 text-sm text-green-300 font-mono outline-none focus:border-green-500"
            onKeyPress={(e) => e.key === 'Enter' && startScan()}
          />
          <button
            onClick={startScan}
            className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-xs font-bold transition-colors"
          >
            SCAN
          </button>
        </div>
      </div>

      {/* Targets List */}
      <div className="space-y-2">
        {targets.map((target) => (
          <div key={target.id} className="bg-gray-900 rounded-lg border border-gray-600 p-3 hover:border-green-500/50 transition-colors">
            <div className="flex items-center justify-between mb-2">
              <span className="text-cyan-400 font-mono font-bold text-sm">{target.ip}</span>
              <span className={`text-xs font-bold ${getStatusColor(target.status)}`}>
                {target.status.toUpperCase()}
              </span>
            </div>
            <div className="text-xs text-gray-400 space-y-1">
              <div>📡 {target.hostname}</div>
              <div>🔌 Ports: {target.ports}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderVulnsTab = () => (
    <div className="space-y-3">
      {vulnerabilities.map((vuln) => (
        <div key={vuln.id} className={`rounded-lg border p-3 ${getSeverityColor(vuln.severity)}`}>
          <div className="flex items-center justify-between mb-2">
            <span className={`text-xs font-bold px-2 py-1 rounded border ${getSeverityColor(vuln.severity)}`}>
              {vuln.severity.toUpperCase()}
            </span>
            <span className="text-xs text-gray-400 font-mono">{vuln.target}</span>
          </div>
          <div className="text-sm font-medium mb-1">{vuln.vuln}</div>
          <div className="text-xs text-gray-400">
            {vuln.cve !== 'N/A' ? `CVE: ${vuln.cve}` : 'No CVE assigned'}
          </div>
        </div>
      ))}
    </div>
  );

  const renderToolsTab = () => (
    <div className="grid grid-cols-1 gap-3">
      {tools.map((tool, index) => (
        <div
          key={index}
          onClick={() => runTool(tool.name)}
          className="bg-gray-900 rounded-lg border border-gray-600 p-3 hover:border-cyan-500/50 cursor-pointer transition-all hover:scale-105"
        >
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center space-x-2">
              <span className="text-lg">{tool.icon}</span>
              <span className="text-sm font-bold text-cyan-400">{tool.name}</span>
            </div>
            <span className={`text-xs ${getStatusColor(tool.status)}`}>
              {tool.status.toUpperCase()}
            </span>
          </div>
          <div className="text-xs text-gray-400">{tool.description}</div>
        </div>
      ))}
    </div>
  );

  const renderAITab = () => (
    <div className="space-y-4">
      <div className="bg-purple-900/20 rounded-lg border border-purple-500/30 p-4">
        <h3 className="text-sm font-bold text-purple-400 mb-3">🤖 AI Quick Actions</h3>
        <div className="space-y-2">
          <button 
            onClick={() => websocket?.send(JSON.stringify({ type: 'ai_query', query: 'analyze current network topology' }))}
            className="w-full bg-purple-600 hover:bg-purple-700 text-white py-2 px-3 rounded text-xs font-bold transition-colors"
          >
            📊 Analyze Network
          </button>
          <button 
            onClick={() => websocket?.send(JSON.stringify({ type: 'ai_query', query: 'suggest next penetration testing steps' }))}
            className="w-full bg-purple-600 hover:bg-purple-700 text-white py-2 px-3 rounded text-xs font-bold transition-colors"
          >
            🎯 Suggest Next Steps
          </button>
          <button 
            onClick={() => websocket?.send(JSON.stringify({ type: 'ai_query', query: 'identify potential attack vectors' }))}
            className="w-full bg-purple-600 hover:bg-purple-700 text-white py-2 px-3 rounded text-xs font-bold transition-colors"
          >
            ⚡ Find Attack Vectors
          </button>
        </div>
      </div>

      <div className="bg-gray-900 rounded-lg border border-gray-600 p-4">
        <h4 className="text-sm font-bold text-gray-300 mb-3">💡 AI Tips</h4>
        <ul className="text-xs text-gray-400 space-y-2">
          <li>• Use "ai:" prefix in terminal for queries</li>
          <li>• Ask for exploit recommendations</li>
          <li>• Get vulnerability analysis</li>
          <li>• Request network topology insights</li>
        </ul>
      </div>
    </div>
  );

  const renderTabContent = () => {
    switch (activeTab) {
      case 'targets':
        return renderTargetsTab();
      case 'vulns':
        return renderVulnsTab();
      case 'tools':
        return renderToolsTab();
      case 'ai':
        return renderAITab();
      default:
        return null;
    }
  };

  return (
    <div className={`bg-black border-l border-green-500 ${className}`}>
      {/* Tab Headers */}
      <div className="bg-gray-900 border-b border-green-500 p-2">
        <div className="grid grid-cols-2 gap-1">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-2 py-1 rounded text-xs font-bold transition-all ${
                activeTab === tab.id
                  ? 'bg-green-600 text-white'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
            >
              {tab.icon} {tab.name}
            </button>
          ))}
        </div>
      </div>

      {/* Tab Content */}
      <div className="p-4 h-full overflow-y-auto scrollbar-thin scrollbar-track-gray-900 scrollbar-thumb-green-500">
        {renderTabContent()}
      </div>
    </div>
  );
};

export default SidePanel;