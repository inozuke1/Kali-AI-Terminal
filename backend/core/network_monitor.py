"""
NETWORK MONITOR - Real-time System & Network Monitoring
Advanced monitoring and analytics for security operations
"""

import asyncio
import psutil
import json
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import socket
import subprocess
import platform
from utils.logger import setup_logger

logger = setup_logger(__name__)

@dataclass
class NetworkInterface:
    name: str
    ip_address: str
    mac_address: str
    status: str
    bytes_sent: int
    bytes_recv: int
    packets_sent: int
    packets_recv: int

@dataclass
class SystemMetrics:
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    memory_available: int
    memory_total: int
    disk_usage_percent: float
    disk_free: int
    disk_total: int
    network_io: Dict[str, Dict]
    active_connections: int
    running_processes: int

@dataclass
class NetworkConnection:
    local_address: str
    local_port: int
    remote_address: str
    remote_port: int
    status: str
    pid: Optional[int]
    process_name: Optional[str]

class NetworkMonitor:
    def __init__(self):
        self._running = False
        self._monitor_task = None
        self.metrics_history: List[SystemMetrics] = []
        self.active_connections: List[NetworkConnection] = []
        self.network_interfaces: List[NetworkInterface] = []
        self._last_network_io = None
        
        logger.info("Network Monitor initialized")

    def is_ready(self) -> bool:
        """Check if monitor is ready"""
        return True

    async def start_monitoring(self):
        """Start real-time monitoring"""
        self._running = True
        self._monitor_task = asyncio.create_task(self._monitoring_loop())
        logger.info("Started real-time network monitoring")

    async def _monitoring_loop(self):
        """Main monitoring loop"""
        while self._running:
            try:
                # Collect system metrics
                metrics = await self._collect_system_metrics()
                self.metrics_history.append(metrics)
                
                # Keep only last hour of metrics (assuming 5 second intervals)
                if len(self.metrics_history) > 720:  # 720 * 5 seconds = 1 hour
                    self.metrics_history.pop(0)
                
                # Update network interfaces
                await self._update_network_interfaces()
                
                # Update active connections
                await self._update_active_connections()
                
                # Sleep for 5 seconds before next collection
                await asyncio.sleep(5)
                
            except Exception as e:
                logger.error(f"❌ Monitoring loop error: {str(e)}")
                await asyncio.sleep(10)

    async def _collect_system_metrics(self) -> SystemMetrics:
        """Collect current system metrics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            
            # Disk usage
            disk = psutil.disk_usage('/')
            
            # Network I/O
            network_io = psutil.net_io_counters(pernic=True)
            
            # Process count
            running_processes = len(psutil.pids())
            
            # Active network connections count
            connections = psutil.net_connections()
            active_connections = len([c for c in connections if c.status == 'ESTABLISHED'])
            
            metrics = SystemMetrics(
                timestamp=datetime.now(),
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_available=memory.available,
                memory_total=memory.total,
                disk_usage_percent=disk.percent,
                disk_free=disk.free,
                disk_total=disk.total,
                network_io={name: {
                    'bytes_sent': stats.bytes_sent,
                    'bytes_recv': stats.bytes_recv,
                    'packets_sent': stats.packets_sent,
                    'packets_recv': stats.packets_recv
                } for name, stats in network_io.items()},
                active_connections=active_connections,
                running_processes=running_processes
            )
            
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Failed to collect system metrics: {str(e)}")
            # Return empty metrics on error
            return SystemMetrics(
                timestamp=datetime.now(),
                cpu_percent=0.0,
                memory_percent=0.0,
                memory_available=0,
                memory_total=0,
                disk_usage_percent=0.0,
                disk_free=0,
                disk_total=0,
                network_io={},
                active_connections=0,
                running_processes=0
            )

    async def _update_network_interfaces(self):
        """Update network interface information"""
        try:
            interfaces = []
            net_if_addrs = psutil.net_if_addrs()
            net_if_stats = psutil.net_if_stats()
            net_io_counters = psutil.net_io_counters(pernic=True)
            
            for interface_name, addresses in net_if_addrs.items():
                ip_address = ""
                mac_address = ""
                
                # Extract IP and MAC addresses
                for addr in addresses:
                    if addr.family == socket.AF_INET:
                        ip_address = addr.address
                    elif addr.family == psutil.AF_LINK:
                        mac_address = addr.address
                
                # Get interface status
                if_stats = net_if_stats.get(interface_name)
                status = "up" if if_stats and if_stats.isup else "down"
                
                # Get I/O counters
                io_counters = net_io_counters.get(interface_name)
                if io_counters:
                    interface = NetworkInterface(
                        name=interface_name,
                        ip_address=ip_address,
                        mac_address=mac_address,
                        status=status,
                        bytes_sent=io_counters.bytes_sent,
                        bytes_recv=io_counters.bytes_recv,
                        packets_sent=io_counters.packets_sent,
                        packets_recv=io_counters.packets_recv
                    )
                    interfaces.append(interface)
            
            self.network_interfaces = interfaces
            
        except Exception as e:
            logger.error(f"❌ Failed to update network interfaces: {str(e)}")

    async def _update_active_connections(self):
        """Update active network connections"""
        try:
            connections = []
            net_connections = psutil.net_connections(kind='inet')
            
            for conn in net_connections:
                if conn.status == 'ESTABLISHED':
                    process_name = None
                    if conn.pid:
                        try:
                            process = psutil.Process(conn.pid)
                            process_name = process.name()
                        except:
                            process_name = "Unknown"
                    
                    connection = NetworkConnection(
                        local_address=conn.laddr.ip if conn.laddr else "",
                        local_port=conn.laddr.port if conn.laddr else 0,
                        remote_address=conn.raddr.ip if conn.raddr else "",
                        remote_port=conn.raddr.port if conn.raddr else 0,
                        status=conn.status,
                        pid=conn.pid,
                        process_name=process_name
                    )
                    connections.append(connection)
            
            self.active_connections = connections
            
        except Exception as e:
            logger.error(f"❌ Failed to update active connections: {str(e)}")

    async def get_system_status(self) -> Dict:
        """Get current system status"""
        try:
            current_metrics = await self._collect_system_metrics()
            
            # Calculate network throughput if we have previous data
            network_throughput = {}
            if self._last_network_io and current_metrics.network_io:
                for interface, current_io in current_metrics.network_io.items():
                    if interface in self._last_network_io:
                        last_io = self._last_network_io[interface]
                        time_diff = 5  # 5 seconds between collections
                        
                        bytes_sent_per_sec = (current_io['bytes_sent'] - last_io['bytes_sent']) / time_diff
                        bytes_recv_per_sec = (current_io['bytes_recv'] - last_io['bytes_recv']) / time_diff
                        
                        network_throughput[interface] = {
                            'upload_speed': bytes_sent_per_sec,
                            'download_speed': bytes_recv_per_sec
                        }
            
            self._last_network_io = current_metrics.network_io
            
            # Get system uptime
            boot_time = psutil.boot_time()
            uptime_seconds = time.time() - boot_time
            uptime = str(timedelta(seconds=int(uptime_seconds)))
            
            # Get load average (on Unix systems)
            load_avg = None
            try:
                if hasattr(psutil, 'getloadavg'):
                    load_avg = psutil.getloadavg()
            except:
                pass
            
            status = {
                "timestamp": current_metrics.timestamp.isoformat(),
                "system": {
                    "platform": platform.system(),
                    "hostname": socket.gethostname(),
                    "uptime": uptime,
                    "load_average": load_avg
                },
                "cpu": {
                    "usage_percent": current_metrics.cpu_percent,
                    "count": psutil.cpu_count(),
                    "count_logical": psutil.cpu_count(logical=True)
                },
                "memory": {
                    "usage_percent": current_metrics.memory_percent,
                    "available_gb": round(current_metrics.memory_available / (1024**3), 2),
                    "total_gb": round(current_metrics.memory_total / (1024**3), 2)
                },
                "disk": {
                    "usage_percent": current_metrics.disk_usage_percent,
                    "free_gb": round(current_metrics.disk_free / (1024**3), 2),
                    "total_gb": round(current_metrics.disk_total / (1024**3), 2)
                },
                "network": {
                    "interfaces": [asdict(interface) for interface in self.network_interfaces],
                    "active_connections": current_metrics.active_connections,
                    "throughput": network_throughput
                },
                "processes": {
                    "running": current_metrics.running_processes
                }
            }
            
            return status
            
        except Exception as e:
            logger.error(f"❌ Failed to get system status: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}

    async def get_system_stats(self) -> Dict:
        """Get system statistics over time"""
        if not self.metrics_history:
            return {"error": "No metrics available"}
        
        try:
            # Calculate averages over the last hour
            recent_metrics = self.metrics_history[-60:] if len(self.metrics_history) >= 60 else self.metrics_history
            
            avg_cpu = sum(m.cpu_percent for m in recent_metrics) / len(recent_metrics)
            avg_memory = sum(m.memory_percent for m in recent_metrics) / len(recent_metrics)
            avg_disk = sum(m.disk_usage_percent for m in recent_metrics) / len(recent_metrics)
            
            # Get peak values
            peak_cpu = max(m.cpu_percent for m in recent_metrics)
            peak_memory = max(m.memory_percent for m in recent_metrics)
            
            # Network activity
            total_connections = sum(m.active_connections for m in recent_metrics)
            avg_connections = total_connections / len(recent_metrics)
            
            stats = {
                "time_range": f"Last {len(recent_metrics) * 5} seconds",
                "cpu": {
                    "average_percent": round(avg_cpu, 2),
                    "peak_percent": round(peak_cpu, 2)
                },
                "memory": {
                    "average_percent": round(avg_memory, 2),
                    "peak_percent": round(peak_memory, 2)
                },
                "disk": {
                    "average_usage_percent": round(avg_disk, 2)
                },
                "network": {
                    "average_connections": round(avg_connections, 2),
                    "total_interfaces": len(self.network_interfaces),
                    "active_interfaces": len([i for i in self.network_interfaces if i.status == "up"])
                },
                "data_points": len(recent_metrics),
                "monitoring_duration": f"{len(self.metrics_history) * 5} seconds"
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Failed to get system stats: {str(e)}")
            return {"error": str(e)}

    async def get_network_connections(self) -> List[Dict]:
        """Get active network connections"""
        return [asdict(conn) for conn in self.active_connections]

    async def get_network_interfaces(self) -> List[Dict]:
        """Get network interface information"""
        return [asdict(interface) for interface in self.network_interfaces]

    async def stop_monitoring(self):
        """Stop monitoring"""
        self._running = False
        if self._monitor_task:
            self._monitor_task.cancel()
        logger.info("Stopped network monitoring")

    async def get_security_alerts(self) -> List[Dict]:
        """Get security-related alerts based on monitoring data"""
        alerts = []
        
        if not self.metrics_history:
            return alerts
        
        # Check for high resource usage
        latest_metrics = self.metrics_history[-1]
        
        if latest_metrics.cpu_percent > 90:
            alerts.append({
                "type": "high_cpu",
                "severity": "warning",
                "message": f"High CPU usage: {latest_metrics.cpu_percent:.1f}%",
                "timestamp": latest_metrics.timestamp.isoformat()
            })
        
        if latest_metrics.memory_percent > 90:
            alerts.append({
                "type": "high_memory",
                "severity": "warning", 
                "message": f"High memory usage: {latest_metrics.memory_percent:.1f}%",
                "timestamp": latest_metrics.timestamp.isoformat()
            })
        
        # Check for suspicious network activity
        if latest_metrics.active_connections > 100:
            alerts.append({
                "type": "high_network_activity",
                "severity": "info",
                "message": f"High number of network connections: {latest_metrics.active_connections}",
                "timestamp": latest_metrics.timestamp.isoformat()
            })
        
        return alerts
