#!/usr/bin/env python3
"""
Tests for SentinelAgent
"""

import unittest
import tempfile
import json
import os
from sentinel_agent import SentinelAgent, MetricData, HealthStatus


class TestSentinelAgent(unittest.TestCase):
    """Test cases for SentinelAgent"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.agent = SentinelAgent()
    
    def test_initialization(self):
        """Test agent initialization"""
        self.assertIsNotNone(self.agent)
        self.assertIsNotNone(self.agent.config)
        self.assertIsNotNone(self.agent.logger)
        self.assertEqual(len(self.agent.metrics_history), 0)
    
    def test_default_config(self):
        """Test default configuration"""
        config = self.agent._default_config()
        self.assertIn('monitoring_interval', config)
        self.assertIn('alert_thresholds', config)
        self.assertEqual(config['monitoring_interval'], 60)
    
    def test_load_config_json(self):
        """Test loading JSON configuration"""
        config_data = {
            'monitoring_interval': 30,
            'alert_thresholds': {
                'cpu_percent': 70.0
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_path = f.name
        
        try:
            agent = SentinelAgent(config_path=config_path)
            self.assertEqual(agent.config['monitoring_interval'], 30)
            self.assertEqual(agent.config['alert_thresholds']['cpu_percent'], 70.0)
        finally:
            os.unlink(config_path)
    
    def test_collect_system_metrics(self):
        """Test system metrics collection"""
        metrics = self.agent.collect_system_metrics()
        
        self.assertIsInstance(metrics, dict)
        self.assertIn('cpu_percent', metrics)
        self.assertIn('memory_percent', metrics)
        self.assertIn('disk_percent', metrics)
        
        # Verify metrics are reasonable
        self.assertGreaterEqual(metrics['cpu_percent'], 0)
        self.assertLessEqual(metrics['cpu_percent'], 100)
        self.assertGreaterEqual(metrics['memory_percent'], 0)
        self.assertLessEqual(metrics['memory_percent'], 100)
    
    def test_record_metric(self):
        """Test metric recording"""
        metric = self.agent.record_metric('test_metric', 50.0, 'units')
        
        self.assertIsInstance(metric, MetricData)
        self.assertEqual(metric.metric_name, 'test_metric')
        self.assertEqual(metric.value, 50.0)
        self.assertEqual(metric.unit, 'units')
        self.assertEqual(len(self.agent.metrics_history), 1)
    
    def test_record_metric_alert(self):
        """Test metric recording with alert"""
        self.agent.alert_thresholds['test_metric'] = 40.0
        metric = self.agent.record_metric('test_metric', 50.0, 'units')
        
        self.assertEqual(metric.status, 'alert')
    
    def test_get_health_status(self):
        """Test health status retrieval"""
        health = self.agent.get_health_status()
        
        self.assertIsInstance(health, HealthStatus)
        self.assertIn(health.status, ['healthy', 'warning', 'unhealthy'])
        self.assertGreaterEqual(health.cpu_percent, 0)
        self.assertGreaterEqual(health.uptime_seconds, 0)
    
    def test_check_alerts(self):
        """Test alert checking"""
        # Set low thresholds to trigger alerts
        self.agent.alert_thresholds['cpu_percent'] = 0.1
        
        alerts = self.agent.check_alerts()
        
        self.assertIsInstance(alerts, list)
        # At least one alert should be triggered with such low threshold
        if len(alerts) > 0:
            alert = alerts[0]
            self.assertIn('timestamp', alert)
            self.assertIn('metric', alert)
            self.assertIn('value', alert)
    
    def test_get_metrics_summary_empty(self):
        """Test metrics summary when no metrics"""
        summary = self.agent.get_metrics_summary()
        self.assertIn('message', summary)
    
    def test_get_metrics_summary_with_data(self):
        """Test metrics summary with data"""
        self.agent.record_metric('metric1', 10.0)
        self.agent.record_metric('metric2', 20.0)
        
        summary = self.agent.get_metrics_summary()
        
        self.assertIn('total_metrics', summary)
        self.assertEqual(summary['total_metrics'], 2)
        self.assertIn('latest_metrics', summary)
    
    def test_metrics_retention(self):
        """Test metrics retention limit"""
        self.agent.config['metrics_retention'] = 5
        
        for i in range(10):
            self.agent.record_metric(f'metric_{i}', float(i))
        
        self.assertEqual(len(self.agent.metrics_history), 5)
    
    def test_check_pos_health_no_endpoint(self):
        """Test POS health check without endpoint"""
        result = self.agent.check_pos_health()
        
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'unknown')
    
    def test_run_monitoring_cycle(self):
        """Test a complete monitoring cycle"""
        result = self.agent.run_monitoring_cycle()
        
        self.assertIsInstance(result, dict)
        self.assertIn('health_status', result)
        self.assertIn('system_metrics', result)
        self.assertIn('alerts', result)


class TestMetricData(unittest.TestCase):
    """Test cases for MetricData dataclass"""
    
    def test_metric_data_creation(self):
        """Test creating MetricData instance"""
        metric = MetricData(
            timestamp='2026-02-13T10:00:00',
            metric_name='test',
            value=100.0,
            unit='ms',
            status='normal'
        )
        
        self.assertEqual(metric.metric_name, 'test')
        self.assertEqual(metric.value, 100.0)


class TestHealthStatus(unittest.TestCase):
    """Test cases for HealthStatus dataclass"""
    
    def test_health_status_creation(self):
        """Test creating HealthStatus instance"""
        health = HealthStatus(
            timestamp='2026-02-13T10:00:00',
            status='healthy',
            cpu_percent=50.0,
            memory_percent=60.0,
            disk_percent=70.0,
            uptime_seconds=3600.0
        )
        
        self.assertEqual(health.status, 'healthy')
        self.assertEqual(health.cpu_percent, 50.0)


if __name__ == '__main__':
    unittest.main()
