import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Brain,
  Terminal,
  Shield,
  Activity,
  Settings,
  Power,
  User,
  Bell,
  Search,
  Menu,
  X,
  Maximize,
  Minimize,
  Minus,
  ChevronDown,
  Wifi,
  WifiOff,
  Zap,
  AlertTriangle,
  CheckCircle,
  Clock,
  HardDrive,
  Cpu,
  MemoryStick
} from 'lucide-react';

const HeaderBar = ({ isAIActive, setIsAIActive, systemStats }) => {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState('connected');
  const [notifications, setNotifications] = useState([
    {
      id: 1,
      type: 'success',
      title: 'Scan Complete',
      message: 'Network scan completed successfully',
      time: '2 min ago',
      read: false
    },
    {
      id: 2,
      type: 'warning',
      title: 'High CPU Usage',
      message: 'CPU usage is above 80%',
      time: '5 min ago',
      read: false
    },
    {
      id: 3,
      type: 'info',
      title: 'New Target Added',
      message: '192.168.1.100 added to targets',
      time: '10 min ago',
      read: true
    }
  ]);

  // Update time every second
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  // Simulate connection status monitoring
  useEffect(() => {
    const checkConnection = () => {
      // Simple connection check simulation
      const isConnected = Math.random() > 0.1; // 90% chance connected
      setConnectionStatus(isConnected ? 'connected' : 'disconnected');
    };

    const interval = setInterval(checkConnection, 5000);
    return () => clearInterval(interval);
  }, []);

  // Get notification icon
  const getNotificationIcon = (type) => {
    switch (type) {
      case 'success': return <CheckCircle size={14} className="text-green-400" />;
      case 'warning': return <AlertTriangle size={14} className="text-yellow-400" />;
      case 'error': return <X size={14} className="text-red-400" />;
      case 'info': return <Bell size={14} className="text-blue-400" />;
      default: return <Bell size={14} className="text-gray-400" />;
    }
  };

  // Toggle fullscreen
  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen();
      setIsFullscreen(true);
    } else {
      document.exitFullscreen();
      setIsFullscreen(false);
    }
  };

  // Get system health status
  const getSystemHealth = () => {
    const avgUsage = (systemStats.cpu + systemStats.memory + systemStats.network) / 3;
    if (avgUsage > 80) return { status: 'critical', color: 'text-red-400', label: 'Critical' };
    if (avgUsage > 60) return { status: 'warning', color: 'text-yellow-400', label: 'Warning' };
    if (avgUsage > 40) return { status: 'good', color: 'text-green-400', label: 'Good' };
    return { status: 'optimal', color: 'text-blue-400', label: 'Optimal' };
  };

  const systemHealth = getSystemHealth();
  const unreadNotifications = notifications.filter(n => !n.read).length;

  return (
    <motion.div 
      initial={{ y: -50, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="header-bar"
    >
      {/* Left Section - Logo & Navigation */}
      <div className="header-left">
        <div className="logo-section">
          <motion.div
            animate={{ 
              textShadow: [
                '0 0 5px #00ff41',
                '0 0 10px #00ff41',
                '0 0 5px #00ff41'
              ]
            }}
            transition={{ duration: 2, repeat: Infinity }}
            className="logo"
          >
            <Terminal size={24} />
            <span className="logo-text">KALI AI</span>
          </motion.div>
        </div>

        <div className="nav-section">
          <nav className="main-nav">
            <button className="nav-item active">
              <Terminal size={16} />
              <span>Terminal</span>
            </button>
            <button className="nav-item">
              <Shield size={16} />
              <span>Security</span>
            </button>
            <button className="nav-item">
              <Activity size={16} />
              <span>Monitor</span>
            </button>
            <button className="nav-item">
              <Settings size={16} />
              <span>Tools</span>
            </button>
          </nav>
        </div>
      </div>

      {/* Center Section - AI Controls & Status */}
      <div className="header-center">
        <div className="ai-control-panel">
          <div className="ai-status">
            <motion.div
              animate={isAIActive ? {
                boxShadow: [
                  '0 0 10px rgba(0, 255, 65, 0.5)',
                  '0 0 20px rgba(0, 255, 65, 0.8)',
                  '0 0 10px rgba(0, 255, 65, 0.5)'
                ]
              } : {}}
              transition={{ duration: 2, repeat: Infinity }}
              className={`ai-indicator ${isAIActive ? 'active' : 'inactive'}`}
            >
              <Brain size={20} />
              <div className="ai-info">
                <span className="ai-label">AI Assistant</span>
                <span className="ai-state">
                  {isAIActive ? 'ACTIVE' : 'STANDBY'}
                </span>
              </div>
            </motion.div>

            <button
              onClick={() => setIsAIActive(!isAIActive)}
              className={`ai-toggle ${isAIActive ? 'active' : 'inactive'}`}
            >
              <Power size={16} />
              {isAIActive ? 'Disable' : 'Enable'}
            </button>
          </div>
        </div>

        {/* System Health Indicator */}
        <div className="system-health">
          <div className={`health-indicator ${systemHealth.status}`}>
            <Activity size={16} className={systemHealth.color} />
            <span className={systemHealth.color}>{systemHealth.label}</span>
          </div>
        </div>
      </div>

      {/* Right Section - System Stats & Controls */}
      <div className="header-right">
        {/* Quick Stats */}
        <div className="quick-stats">
          <div className="stat-item">
            <Cpu size={14} />
            <span>{systemStats.cpu}%</span>
            <div className="stat-bar">
              <motion.div 
                className="stat-fill cpu"
                initial={{ width: 0 }}
                animate={{ width: `${systemStats.cpu}%` }}
                transition={{ duration: 0.5 }}
              />
            </div>
          </div>

          <div className="stat-item">
            <MemoryStick size={14} />
            <span>{systemStats.memory}%</span>
            <div className="stat-bar">
              <motion.div 
                className="stat-fill memory"
                initial={{ width: 0 }}
                animate={{ width: `${systemStats.memory}%` }}
                transition={{ duration: 0.5 }}
              />
            </div>
          </div>

          <div className="stat-item">
            <Wifi size={14} />
            <span>{systemStats.network}%</span>
            <div className="stat-bar">
              <motion.div 
                className="stat-fill network"
                initial={{ width: 0 }}
                animate={{ width: `${systemStats.network}%` }}
                transition={{ duration: 0.5 }}
              />
            </div>
          </div>
        </div>

        {/* Connection Status */}
        <div className="connection-status">
          <div className={`connection-indicator ${connectionStatus}`}>
            {connectionStatus === 'connected' ? (
              <Wifi size={16} className="text-green-400" />
            ) : (
              <WifiOff size={16} className="text-red-400" />
            )}
            <span className={connectionStatus === 'connected' ? 'text-green-400' : 'text-red-400'}>
              {connectionStatus === 'connected' ? 'Online' : 'Offline'}
            </span>
          </div>
        </div>

        {/* Notifications */}
        <div className="notifications-section">
          <button
            onClick={() => setShowNotifications(!showNotifications)}
            className="notification-btn"
          >
            <Bell size={16} />
            {unreadNotifications > 0 && (
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                className="notification-badge"
              >
                {unreadNotifications}
              </motion.div>
            )}
          </button>

          <AnimatePresence>
            {showNotifications && (
              <motion.div
                initial={{ opacity: 0, y: -10, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: -10, scale: 0.95 }}
                className="notifications-dropdown"
              >
                <div className="notifications-header">
                  <span>Notifications</span>
                  <button 
                    onClick={() => setShowNotifications(false)}
                    className="close-btn"
                  >
                    <X size={14} />
                  </button>
                </div>
                <div className="notifications-list">
                  {notifications.map(notification => (
                    <div
                      key={notification.id}
                      className={`notification-item ${notification.read ? 'read' : 'unread'}`}
                    >
                      <div className="notification-icon">
                        {getNotificationIcon(notification.type)}
                      </div>
                      <div className="notification-content">
                        <div className="notification-title">{notification.title}</div>
                        <div className="notification-message">{notification.message}</div>
                        <div className="notification-time">
                          <Clock size={10} />
                          {notification.time}
                        </div>
                      </div>
                      {!notification.read && (
                        <div className="unread-indicator"></div>
                      )}
                    </div>
                  ))}
                </div>
                <div className="notifications-footer">
                  <button className="clear-all-btn">
                    Clear All
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Time Display */}
        <div className="time-display">
          <div className="time">
            {currentTime.toLocaleTimeString('en-US', {
              hour12: false,
              hour: '2-digit',
              minute: '2-digit',
              second: '2-digit'
            })}
          </div>
          <div className="date">
            {currentTime.toLocaleDateString('en-US', {
              month: 'short',
              day: 'numeric'
            })}
          </div>
        </div>

        {/* Profile Menu */}
        <div className="profile-section">
          <button
            onClick={() => setShowProfileMenu(!showProfileMenu)}
            className="profile-btn"
          >
            <User size={16} />
            <span>Admin</span>
            <ChevronDown size={12} className={showProfileMenu ? 'rotated' : ''} />
          </button>

          <AnimatePresence>
            {showProfileMenu && (
              <motion.div
                initial={{ opacity: 0, y: -10, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: -10, scale: 0.95 }}
                className="profile-dropdown"
              >
                <div className="profile-info">
                  <div className="profile-avatar">
                    <User size={20} />
                  </div>
                  <div className="profile-details">
                    <span className="profile-name">Administrator</span>
                    <span className="profile-email">admin@kali.local</span>
                  </div>
                </div>
                <div className="profile-menu">
                  <button className="menu-item">
                    <Settings size={14} />
                    <span>Settings</span>
                  </button>
                  <button className="menu-item">
                    <Shield size={14} />
                    <span>Security</span>
                  </button>
                  <button className="menu-item">
                    <Activity size={14} />
                    <span>Activity Log</span>
                  </button>
                  <div className="menu-divider"></div>
                  <button className="menu-item logout">
                    <Power size={14} />
                    <span>Logout</span>
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Window Controls */}
        <div className="window-controls">
          <button className="control-btn minimize">
            <Minus size={12} />
          </button>
          <button 
            className="control-btn maximize"
            onClick={toggleFullscreen}
          >
            <Maximize size={12} />
          </button>
          <button className="control-btn close">
            <X size={12} />
          </button>
        </div>
      </div>
    </motion.div>
  );
};

export default HeaderBar;
