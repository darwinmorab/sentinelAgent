#!/usr/bin/env python3
"""
SentinelAgent - Monitoring Agent for Point of Sale Systems
Monitors POS system health, transactions, and generates alerts
"""

import time
import json
import logging
import psutil
import requests
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class MetricData:
    """Data class for metric information"""
    timestamp: str
    metric_name: str
    value: float
    unit: str
    status: str


@dataclass
class HealthStatus:
    """Data class for health status information"""
    timestamp: str
    status: str
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    uptime_seconds: float


class SentinelAgent:
    """Main monitoring agent for POS systems"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the SentinelAgent
        
        Args:
            config_path: Path to configuration file (JSON or YAML)
        """
        self.config = self._load_config(config_path) if config_path else self._default_config()
        self.start_time = time.time()
        self._setup_logging()
        self.metrics_history: List[MetricData] = []
        self.alert_thresholds = self.config.get('alert_thresholds', {})
        
    def _default_config(self) -> Dict:
        """Return default configuration"""
        return {
            'monitoring_interval': 60,
            'alert_thresholds': {
                'cpu_percent': 80.0,
                'memory_percent': 85.0,
                'disk_percent': 90.0,
                'response_time_ms': 1000.0
            },
            'pos_endpoint': None,
            'log_level': 'INFO',
            'metrics_retention': 1000
        }
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from file"""
        try:
            with open(config_path, 'r') as f:
                if config_path.endswith('.json'):
                    return json.load(f)
                elif config_path.endswith('.yaml') or config_path.endswith('.yml'):
                    import yaml
                    return yaml.safe_load(f)
                else:
                    logging.warning(f"Unknown config format, using defaults")
                    return self._default_config()
        except Exception as e:
            logging.error(f"Error loading config: {e}, using defaults")
            return self._default_config()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_level = self.config.get('log_level', 'INFO')
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('sentinel_agent.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('SentinelAgent')
    
    def collect_system_metrics(self) -> Dict[str, float]:
        """Collect system resource metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            metrics = {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'disk_percent': disk.percent,
                'memory_available_mb': memory.available / (1024 * 1024),
                'disk_free_gb': disk.free / (1024 * 1024 * 1024)
            }
            
            self.logger.debug(f"System metrics collected: {metrics}")
            return metrics
        except Exception as e:
            self.logger.error(f"Error collecting system metrics: {e}")
            return {}
    
    def check_pos_health(self, endpoint: Optional[str] = None) -> Dict:
        """
        Check POS endpoint health
        
        Args:
            endpoint: POS system endpoint URL
            
        Returns:
            Dictionary with health check results
        """
        endpoint = endpoint or self.config.get('pos_endpoint')
        
        if not endpoint:
            self.logger.warning("No POS endpoint configured")
            return {'status': 'unknown', 'message': 'No endpoint configured'}
        
        try:
            start_time = time.time()
            response = requests.get(endpoint, timeout=10)
            response_time = (time.time() - start_time) * 1000  # Convert to ms
            
            health = {
                'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                'status_code': response.status_code,
                'response_time_ms': response_time,
                'timestamp': datetime.now().isoformat()
            }
            
            self.logger.info(f"POS health check: {health}")
            return health
        except requests.exceptions.RequestException as e:
            self.logger.error(f"POS health check failed: {e}")
            return {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_health_status(self) -> HealthStatus:
        """Get overall health status"""
        metrics = self.collect_system_metrics()
        uptime = time.time() - self.start_time
        
        # Determine overall status
        status = 'healthy'
        if (metrics.get('cpu_percent', 0) > self.alert_thresholds.get('cpu_percent', 100) or
            metrics.get('memory_percent', 0) > self.alert_thresholds.get('memory_percent', 100) or
            metrics.get('disk_percent', 0) > self.alert_thresholds.get('disk_percent', 100)):
            status = 'warning'
        
        health = HealthStatus(
            timestamp=datetime.now().isoformat(),
            status=status,
            cpu_percent=metrics.get('cpu_percent', 0.0),
            memory_percent=metrics.get('memory_percent', 0.0),
            disk_percent=metrics.get('disk_percent', 0.0),
            uptime_seconds=uptime
        )
        
        return health
    
    def record_metric(self, metric_name: str, value: float, unit: str = ''):
        """
        Record a custom metric
        
        Args:
            metric_name: Name of the metric
            value: Metric value
            unit: Unit of measurement
        """
        status = 'normal'
        if metric_name in self.alert_thresholds:
            if value > self.alert_thresholds[metric_name]:
                status = 'alert'
        
        metric = MetricData(
            timestamp=datetime.now().isoformat(),
            metric_name=metric_name,
            value=value,
            unit=unit,
            status=status
        )
        
        self.metrics_history.append(metric)
        
        # Keep only recent metrics
        max_metrics = self.config.get('metrics_retention', 1000)
        if len(self.metrics_history) > max_metrics:
            self.metrics_history = self.metrics_history[-max_metrics:]
        
        if status == 'alert':
            self.logger.warning(f"ALERT: {metric_name} = {value}{unit} exceeds threshold")
        
        return metric
    
    def check_alerts(self) -> List[Dict]:
        """Check for alert conditions"""
        alerts = []
        metrics = self.collect_system_metrics()
        
        for metric_name, threshold in self.alert_thresholds.items():
            if metric_name in metrics and metrics[metric_name] > threshold:
                alert = {
                    'timestamp': datetime.now().isoformat(),
                    'metric': metric_name,
                    'value': metrics[metric_name],
                    'threshold': threshold,
                    'severity': 'warning'
                }
                alerts.append(alert)
                self.logger.warning(f"Alert: {metric_name} = {metrics[metric_name]} > {threshold}")
        
        return alerts
    
    def get_metrics_summary(self) -> Dict:
        """Get summary of collected metrics"""
        if not self.metrics_history:
            return {'message': 'No metrics recorded yet'}
        
        summary = {
            'total_metrics': len(self.metrics_history),
            'latest_metrics': [asdict(m) for m in self.metrics_history[-10:]],
            'alert_count': sum(1 for m in self.metrics_history if m.status == 'alert')
        }
        
        return summary
    
    def run_monitoring_cycle(self):
        """Run a single monitoring cycle"""
        self.logger.info("=== Starting Monitoring Cycle ===")
        
        # Collect system metrics
        system_metrics = self.collect_system_metrics()
        for metric_name, value in system_metrics.items():
            self.record_metric(metric_name, value, '%' if 'percent' in metric_name else '')
        
        # Check POS health
        pos_health = self.check_pos_health()
        
        # Check alerts
        alerts = self.check_alerts()
        
        # Get overall health
        health_status = self.get_health_status()
        
        self.logger.info(f"Health Status: {health_status.status}")
        self.logger.info(f"Active Alerts: {len(alerts)}")
        self.logger.info("=== Monitoring Cycle Complete ===")
        
        return {
            'health_status': asdict(health_status),
            'pos_health': pos_health,
            'alerts': alerts,
            'system_metrics': system_metrics
        }
    
    def start(self, continuous: bool = False):
        """
        Start the monitoring agent
        
        Args:
            continuous: If True, run continuously; if False, run once
        """
        self.logger.info("SentinelAgent starting...")
        self.logger.info(f"Configuration: {self.config}")
        
        try:
            if continuous:
                interval = self.config.get('monitoring_interval', 60)
                self.logger.info(f"Running in continuous mode (interval: {interval}s)")
                
                while True:
                    self.run_monitoring_cycle()
                    time.sleep(interval)
            else:
                self.logger.info("Running single monitoring cycle")
                result = self.run_monitoring_cycle()
                return result
        except KeyboardInterrupt:
            self.logger.info("SentinelAgent stopped by user")
        except Exception as e:
            self.logger.error(f"SentinelAgent error: {e}", exc_info=True)
            raise


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SentinelAgent - POS Monitoring System')
    parser.add_argument('--config', type=str, help='Path to configuration file')
    parser.add_argument('--continuous', action='store_true', help='Run continuously')
    parser.add_argument('--endpoint', type=str, help='POS endpoint URL to monitor')
    
    args = parser.parse_args()
    
    agent = SentinelAgent(config_path=args.config)
    
    if args.endpoint:
        agent.config['pos_endpoint'] = args.endpoint
    
    agent.start(continuous=args.continuous)


if __name__ == '__main__':
    main()
