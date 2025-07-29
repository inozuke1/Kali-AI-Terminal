import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Activity,
  Zap,
  Shield,
  AlertTriangle,
  CheckCircle,
  Clock,
  Wifi,
  Server,
  Database,
  Terminal,
  Brain,
  Target,
  Eye,
  Loader,
  TrendingUp,
  TrendingDown,
  Cpu,
  MemoryStick,
  HardDrive,
  Network,
  Globe,
  Lock,
  Unlock
} from 'lucide-react';

const StatusBar = ({ systemStats }) => {
  const [activeScans, setActiveScans] = useState(2);
  const [vulnerabilitiesFound, setVulnerabilitiesFound] = useState(5);
  const [connectedTargets, setConnectedTargets] = useState(3);
  const [uptime, setUptime] = useState('02:34:56');
  const [networkTraffic, setNetworkTraffic] = useState({ up: 1.2, down: 5.8 });
  const [recentActivity, setRecentActivity] = useState([
    { type: 'scan', message: 'Port scan completed on 192.168.1.100', time: Date.now() - 120000 },
    { type: 'vuln', message: 'SQL injection detected', time: Date.now() - 300000 },
    { type: 'success', message: 'Target secured successfully', time: Date.now() - 450000 }
  ]);
  const [showActivityLog, setShowActivityLog] = useState(false);

  // Update uptime every second
  useEffect(() => {
    const timer = setInterval(() => {
      const now = new Date();
      const startTime = new Date().setHours(now.getHours() - 2, now.getMinutes() - 34, now.getSeconds() - 56);
      const diff = now - startTime;
      const hours = Math.floor(diff / (1000 * 60 * 60));
      const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((diff % (1000 * 60)) / 1000);
      setUptime(`${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`);
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  // Simulate network traffic updates
  useEffect(() => {
    const interval = setInterval(() => {
      setNetworkTraffic({
        up: (Math.random() * 10).toFixed(1),
        down: (Math.random() * 20).toFixed(1)
      });
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  // Get activity icon
  const getActivityIcon = (type) => {
    switch (type) {
      case 'scan': return <Eye size={12} className="text-blue-400" />;
      case 'vuln': return <AlertTriangle size={12} className="text-red-400" />;
      case 'success': return <CheckCircle size={12} className="text-green-400" />;
      case 'error': return <AlertTriangle size={12} className="text-red-400" />;
      default: return <Activity size={12} className="text-gray-400" />;
    }
  };

  // Format time ago
  const formatTimeAgo = (timestamp) => {
    const now = Date.now();
    const diff = now - timestamp;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(minutes / 60);
    
    if (hours > 0) return `${hours}h ago`;
    if (minutes > 0) return `${minutes}m ago`;
    return 'Just now';
  };

  // Get system status color
  const getSystemStatusColor = () => {
    const avgUsage = (systemStats.cpu + systemStats.memory + systemStats.network) / 3;
    if (avgUsage > 80) return 'text-red-400';
    if (avgUsage > 60) return 'text-yellow-400';
    if (avgUsage > 40) return 'text-green-400';
    return 'text-blue-400';
  };

  // Get security status
  const getSecurityStatus = () => {
    if (systemStats.threats > 5) return { status: 'critical', color: 'text-red-400', label: 'CRITICAL' };
    if (systemStats.threats > 2) return { status: 'warning', color: 'text-yellow-400', label: 'WARNING' };
    if (systemStats.threats > 0) return { status: 'alert', color: 'text-orange-400', label: 'ALERT' };
    return { status: 'secure', color: 'text-green-400', label: 'SECURE' };
  };

  const securityStatus = getSecurityStatus();

  return (
    <motion.div 
      initial={{ y: 50, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="status-bar"
    >
      {/* Left Section - System Metrics */}
      <div className="status-left">
        <div className="metric-group">
          <div className="metric-item">
            <Cpu size={14} />
            <span className="metric-label">CPU</span>
            <span className={`metric-value ${systemStats.cpu > 80 ? 'text-red-400' : systemStats.cpu > 60 ? 'text-yellow-400' : 'text-green-400'}`}>
              {systemStats.cpu}%
            </span>
            <div className="metric-trend">
              {systemStats.cpu > 50 ? <TrendingUp size={10} /> : <TrendingDown size={10} />}
            </div>
          </div>

          <div className="metric-item">
            <MemoryStick size={14} />
            <span className="metric-label">RAM</span>
            <span className={`metric-value ${systemStats.memory > 80 ? 'text-red-400' : systemStats.memory > 60 ? 'text-yellow-400' : 'text-green-400'}`}>
              {systemStats.memory}%
            </span>
            <div className="metric-trend">
              {systemStats.memory > 50 ? <TrendingUp size={10} /> : <TrendingDown size={10} />}
            </div>
          </div>

          <div className="metric-item">
            <Network size={14} />
            <span className="metric-label">NET</span>
            <span className={`metric-value ${systemStats.network > 80 ? 'text-red-400' : systemStats.network > 60 ? 'text-yellow-400' : 'text-green-400'}`}>
              {systemStats.network}%
            </span>
            <div className="metric-trend">
              {systemStats.network > 50 ? <TrendingUp size={10} /> : <TrendingDown size={10} />}
            </div>
          </div>

          <div className="metric-separator"></div>

          <div className="metric-item">
            <Globe size={14} />
            <span className="metric-label">Traffic</span>
            <div className="traffic-info">
              <span className="traffic-up">↑{networkTraffic.up} MB/s</span>
              <span className="traffic-down">↓{networkTraffic.down} MB/s</span>
            </div>
          </div>
        </div>
      </div>

      {/* Center Section - Security & Activity Status */}
      <div className="status-center">
        <div className="security-status">
          <div className={`security-indicator ${securityStatus.status}`}>
            <Shield size={16} className={securityStatus.color} />
            <span className={securityStatus.color}>{securityStatus.label}</span>
            {systemStats.threats > 0 && (
              <motion.div
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 1, repeat: Infinity }}
                className="threat-count"
              >
                {systemStats.threats}
              </motion.div>
            )}
          </div>
        </div>

        <div className="activity-summary">
          <div className="activity-item">
            <Eye size={14} className="text-blue-400" />
            <span>{activeScans} Active Scans</span>
          </div>
          <div className="activity-item">
            <AlertTriangle size={14} className="text-red-400" />
            <span>{vulnerabilitiesFound} Vulnerabilities</span>
          </div>
          <div className="activity-item">
            <Target size={14} className="text-green-400" />
            <span>{connectedTargets} Targets</span>
          </div>
        </div>

        <button
          onClick={() => setShowActivityLog(!showActivityLog)}
          className="activity-toggle"
        >
          <Activity size={14} />
          <span>Activity Log</span>
          {recentActivity.length > 0 && (
            <motion.div
              animate={{ scale: [1, 1.1, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
              className="activity-badge"
            >
              {recentActivity.length}
            </motion.div>
          )}
        </button>
      </div>

      {/* Right Section - System Info & Time */}
      <div className="status-right">
        <div className="system-info">
          <div className="info-item">
            <Clock size={14} />
            <span className="info-label">Uptime</span>
            <span className="info-value">{uptime}</span>
          </div>

          <div className="info-item">
            <Terminal size={14} />
            <span className="info-label">Session</span>
            <span className="info-value">admin@kali</span>
          </div>

          <div className="info-item">
            <Server size={14} />
            <span className="info-label">Status</span>
            <div className="connection-indicator">
              <div className="status-dot connected"></div>
              <span className="text-green-400">Online</span>
            </div>
          </div>
        </div>

        <div className="ai-status-mini">
          <Brain size={14} className="text-purple-400" />
          <span className="ai-label">AI</span>
          <motion.div
            animate={{ opacity: [0.5, 1, 0.5] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="ai-pulse-dot"
          ></motion.div>
        </div>
      </div>

      {/* Activity Log Overlay */}
      <AnimatePresence>
        {showActivityLog && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="activity-log-overlay"
          >
            <div className="activity-log-header">
              <div className="log-title">
                <Activity size={16} />
                <span>Recent Activity</span>
              </div>
              <button
                onClick={() => setShowActivityLog(false)}
                className="close-log-btn"
              >
                ×
              </button>
            </div>
            <div className="activity-log-content">
              {recentActivity.map((activity, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="activity-log-item"
                >
                  <div className="activity-icon">
                    {getActivityIcon(activity.type)}
                  </div>
                  <div className="activity-content">
                    <span className="activity-message">{activity.message}</span>
                    <span className="activity-time">{formatTimeAgo(activity.time)}</span>
                  </div>
                </motion.div>
              ))}
            </div>
            <div className="activity-log-footer">
              <button className="view-all-btn">
                View All Activity
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

export default StatusBar;
