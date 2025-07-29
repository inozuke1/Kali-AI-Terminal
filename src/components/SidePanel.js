import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Target,
  Shield,
  AlertTriangle,
  Activity,
  Zap,
  Eye,
  Settings,
  Network,
  Lock,
  Unlock,
  Clock,
  TrendingUp,
  TrendingDown,
  Wifi,
  Server,
  Database,
  Globe,
  Search,
  Filter,
  RefreshCw,
  Play,
  Pause,
  MoreVertical,
  ChevronRight,
  ChevronDown,
  ExternalLink
} from 'lucide-react';

const SidePanel = ({ targets, vulnerabilities, systemStats, activeTab, setActiveTab }) => {
  const [expandedTarget, setExpandedTarget] = useState(null);
  const [expandedVuln, setExpandedVuln] = useState(null);
  const [isMonitoring, setIsMonitoring] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterSeverity, setFilterSeverity] = useState('all');

  const tabs = [
    { id: 'targets', label: 'Targets', icon: Target, count: targets.length },
    { id: 'vulnerabilities', label: 'Vulnerabilities', icon: Shield, count: vulnerabilities.length },
    { id: 'tools', label: 'Tools', icon: Settings, count: 8 },
    { id: 'monitor', label: 'Monitor', icon: Activity, count: null }
  ];

  // Filter vulnerabilities based on search and severity
  const filteredVulnerabilities = vulnerabilities.filter(vuln => {
    const matchesSearch = vuln.type.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         vuln.target.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesSeverity = filterSeverity === 'all' || 
                           vuln.severity.toLowerCase() === filterSeverity.toLowerCase();
    return matchesSearch && matchesSeverity;
  });

  // Get severity color
  const getSeverityColor = (severity) => {
    switch (severity.toLowerCase()) {
      case 'critical': return 'text-red-400 bg-red-400/10 border-red-400/20';
      case 'high': return 'text-orange-400 bg-orange-400/10 border-orange-400/20';
      case 'medium': return 'text-yellow-400 bg-yellow-400/10 border-yellow-400/20';
      case 'low': return 'text-blue-400 bg-blue-400/10 border-blue-400/20';
      default: return 'text-gray-400 bg-gray-400/10 border-gray-400/20';
    }
  };

  // Get risk color
  const getRiskColor = (risk) => {
    switch (risk.toLowerCase()) {
      case 'critical': return 'text-red-400';
      case 'high': return 'text-orange-400';
      case 'medium': return 'text-yellow-400';
      case 'low': return 'text-green-400';
      default: return 'text-gray-400';
    }
  };

  // Get status icon
  const getStatusIcon = (status) => {
    switch (status.toLowerCase()) {
      case 'scanning': return <Search className="animate-pulse" size={14} />;
      case 'vulnerable': return <Unlock className="text-red-400" size={14} />;
      case 'secure': return <Lock className="text-green-400" size={14} />;
      case 'offline': return <Wifi className="text-gray-400" size={14} />;
      default: return <Globe size={14} />;
    }
  };

  // Security tools data
  const securityTools = [
    { name: 'Nmap', description: 'Network Discovery', status: 'ready', category: 'scanner' },
    { name: 'Metasploit', description: 'Exploitation Framework', status: 'ready', category: 'exploit' },
    { name: 'Burp Suite', description: 'Web Security Testing', status: 'ready', category: 'web' },
    { name: 'Wireshark', description: 'Network Protocol Analyzer', status: 'ready', category: 'analysis' },
    { name: 'SQLMap', description: 'SQL Injection Tool', status: 'ready', category: 'web' },
    { name: 'Hydra', description: 'Password Cracking', status: 'ready', category: 'brute' },
    { name: 'John the Ripper', description: 'Password Hash Cracker', status: 'ready', category: 'brute' },
    { name: 'Dirb', description: 'Web Content Scanner', status: 'ready', category: 'web' }
  ];

  const renderTargetsTab = () => (
    <div className="tab-content">
      <div className="tab-header">
        <div className="tab-title">
          <Target size={16} />
          <span>Active Targets</span>
          <div className="count-badge">{targets.length}</div>
        </div>
        <button className="refresh-btn" onClick={() => window.location.reload()}>
          <RefreshCw size={14} />
        </button>
      </div>

      <div className="targets-list">
        {targets.map(target => (
          <motion.div
            key={target.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`target-item ${expandedTarget === target.id ? 'expanded' : ''}`}
          >
            <div 
              className="target-header"
              onClick={() => setExpandedTarget(expandedTarget === target.id ? null : target.id)}
            >
              <div className="target-info">
                <div className="target-ip">
                  {getStatusIcon(target.status)}
                  <span>{target.ip}</span>
                </div>
                <div className="target-meta">
                  <span className={`risk-level ${getRiskColor(target.risk)}`}>
                    {target.risk.toUpperCase()}
                  </span>
                  <span className="status">{target.status}</span>
                </div>
              </div>
              <ChevronRight 
                size={16} 
                className={`chevron ${expandedTarget === target.id ? 'rotated' : ''}`}
              />
            </div>

            <AnimatePresence>
              {expandedTarget === target.id && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  className="target-details"
                >
                  <div className="detail-row">
                    <span>Status:</span>
                    <span className="status-badge">{target.status}</span>
                  </div>
                  <div className="detail-row">
                    <span>Risk Level:</span>
                    <span className={getRiskColor(target.risk)}>{target.risk}</span>
                  </div>
                  <div className="detail-row">
                    <span>Last Scan:</span>
                    <span>2 minutes ago</span>
                  </div>
                  <div className="target-actions">
                    <button className="action-btn primary">
                      <Play size={12} />
                      Scan
                    </button>
                    <button className="action-btn">
                      <Eye size={12} />
                      Details
                    </button>
                    <button className="action-btn">
                      <ExternalLink size={12} />
                      Open
                    </button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        ))}
      </div>
    </div>
  );

  const renderVulnerabilitiesTab = () => (
    <div className="tab-content">
      <div className="tab-header">
        <div className="tab-title">
          <Shield size={16} />
          <span>Vulnerabilities</span>
          <div className="count-badge">{filteredVulnerabilities.length}</div>
        </div>
      </div>

      <div className="filters">
        <div className="search-box">
          <Search size={14} />
          <input
            type="text"
            placeholder="Search vulnerabilities..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <select 
          value={filterSeverity} 
          onChange={(e) => setFilterSeverity(e.target.value)}
          className="severity-filter"
        >
          <option value="all">All Severities</option>
          <option value="critical">Critical</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>
      </div>

      <div className="vulnerabilities-list">
        {filteredVulnerabilities.map(vuln => (
          <motion.div
            key={vuln.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`vulnerability-item ${expandedVuln === vuln.id ? 'expanded' : ''}`}
          >
            <div 
              className="vuln-header"
              onClick={() => setExpandedVuln(expandedVuln === vuln.id ? null : vuln.id)}
            >
              <div className="vuln-info">
                <div className="vuln-type">
                  <AlertTriangle size={14} />
                  <span>{vuln.type}</span>
                </div>
                <div className="vuln-meta">
                  <span className={`severity-badge ${getSeverityColor(vuln.severity)}`}>
                    {vuln.severity}
                  </span>
                  <span className="target-ip">{vuln.target}</span>
                </div>
              </div>
              <ChevronRight 
                size={16} 
                className={`chevron ${expandedVuln === vuln.id ? 'rotated' : ''}`}
              />
            </div>

            <AnimatePresence>
              {expandedVuln === vuln.id && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  className="vuln-details"
                >
                  <div className="detail-row">
                    <span>Type:</span>
                    <span>{vuln.type}</span>
                  </div>
                  <div className="detail-row">
                    <span>Target:</span>
                    <span>{vuln.target}</span>
                  </div>
                  <div className="detail-row">
                    <span>Severity:</span>
                    <span className={getSeverityColor(vuln.severity)}>{vuln.severity}</span>
                  </div>
                  <div className="detail-row">
                    <span>Discovered:</span>
                    <span>5 minutes ago</span>
                  </div>
                  <div className="vuln-actions">
                    <button className="action-btn primary">
                      <Zap size={12} />
                      Exploit
                    </button>
                    <button className="action-btn">
                      <Eye size={12} />
                      Details
                    </button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        ))}
      </div>
    </div>
  );

  const renderToolsTab = () => (
    <div className="tab-content">
      <div className="tab-header">
        <div className="tab-title">
          <Settings size={16} />
          <span>Security Tools</span>
          <div className="count-badge">{securityTools.length}</div>
        </div>
      </div>

      <div className="tools-grid">
        {securityTools.map((tool, index) => (
          <motion.div
            key={tool.name}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.1 }}
            className="tool-card"
          >
            <div className="tool-header">
              <div className="tool-icon">
                {tool.category === 'scanner' && <Search size={16} />}
                {tool.category === 'exploit' && <Zap size={16} />}
                {tool.category === 'web' && <Globe size={16} />}
                {tool.category === 'analysis' && <Activity size={16} />}
                {tool.category === 'brute' && <Lock size={16} />}
              </div>
              <div className="tool-info">
                <div className="tool-name">{tool.name}</div>
                <div className="tool-description">{tool.description}</div>
              </div>
              <div className={`tool-status ${tool.status}`}>
                <div className="status-dot"></div>
              </div>
            </div>
            <div className="tool-actions">
              <button className="action-btn primary">
                <Play size={12} />
                Launch
              </button>
              <button className="action-btn">
                <Settings size={12} />
                Config
              </button>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );

  const renderMonitorTab = () => (
    <div className="tab-content">
      <div className="tab-header">
        <div className="tab-title">
          <Activity size={16} />
          <span>System Monitor</span>
        </div>
        <button 
          className={`monitor-toggle ${isMonitoring ? 'active' : ''}`}
          onClick={() => setIsMonitoring(!isMonitoring)}
        >
          {isMonitoring ? <Pause size={14} /> : <Play size={14} />}
          {isMonitoring ? 'Pause' : 'Resume'}
        </button>
      </div>

      <div className="monitor-grid">
        <div className="metric-card">
          <div className="metric-header">
            <span>CPU Usage</span>
            <TrendingUp size={14} className="text-green-400" />
          </div>
          <div className="metric-value">
            {systemStats.cpu}%
          </div>
          <div className="metric-bar">
            <motion.div 
              className="metric-fill cpu"
              initial={{ width: 0 }}
              animate={{ width: `${systemStats.cpu}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-header">
            <span>Memory</span>
            <TrendingUp size={14} className="text-blue-400" />
          </div>
          <div className="metric-value">
            {systemStats.memory}%
          </div>
          <div className="metric-bar">
            <motion.div 
              className="metric-fill memory"
              initial={{ width: 0 }}
              animate={{ width: `${systemStats.memory}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-header">
            <span>Network</span>
            <TrendingUp size={14} className="text-purple-400" />
          </div>
          <div className="metric-value">
            {systemStats.network}%
          </div>
          <div className="metric-bar">
            <motion.div 
              className="metric-fill network"
              initial={{ width: 0 }}
              animate={{ width: `${systemStats.network}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
        </div>

        <div className="metric-card threats">
          <div className="metric-header">
            <span>Active Threats</span>
            <AlertTriangle size={14} className="text-red-400" />
          </div>
          <div className="metric-value">
            {systemStats.threats}
          </div>
          <div className="threats-indicator">
            {systemStats.threats > 0 ? (
              <span className="threat-status high">HIGH ALERT</span>
            ) : (
              <span className="threat-status safe">SECURE</span>
            )}
          </div>
        </div>
      </div>

      <div className="monitor-details">
        <div className="detail-section">
          <h4>Network Interfaces</h4>
          <div className="interface-list">
            <div className="interface-item">
              <Wifi size={14} />
              <span>eth0: 192.168.1.100</span>
              <div className="status-dot connected"></div>
            </div>
            <div className="interface-item">
              <Server size={14} />
              <span>wlan0: 10.0.0.50</span>
              <div className="status-dot connected"></div>
            </div>
          </div>
        </div>

        <div className="detail-section">
          <h4>Recent Activity</h4>
          <div className="activity-list">
            <div className="activity-item">
              <Clock size={12} />
              <span>Port scan detected on 192.168.1.100</span>
              <span className="time">2m ago</span>
            </div>
            <div className="activity-item">
              <Clock size={12} />
              <span>SQL injection attempt blocked</span>
              <span className="time">5m ago</span>
            </div>
            <div className="activity-item">
              <Clock size={12} />
              <span>New vulnerability discovered</span>
              <span className="time">8m ago</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <motion.div 
      initial={{ x: 300, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      className="side-panel"
    >
      {/* Tab Navigation */}
      <div className="tab-navigation">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
          >
            <tab.icon size={16} />
            <span>{tab.label}</span>
            {tab.count !== null && (
              <div className="tab-count">{tab.count}</div>
            )}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="tab-container">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.2 }}
          >
            {activeTab === 'targets' && renderTargetsTab()}
            {activeTab === 'vulnerabilities' && renderVulnerabilitiesTab()}
            {activeTab === 'tools' && renderToolsTab()}
            {activeTab === 'monitor' && renderMonitorTab()}
          </motion.div>
        </AnimatePresence>
      </div>
    </motion.div>
  );
};

export default SidePanel;
