#!/usr/bin/env python3
"""
Example usage of SentinelAgent for POS monitoring
"""

from sentinel_agent import SentinelAgent
import time


def example_basic_usage():
    """Example: Basic usage"""
    print("=== Example 1: Basic Usage ===\n")
    
    # Create agent with default configuration
    agent = SentinelAgent()
    
    # Run a single monitoring cycle
    result = agent.run_monitoring_cycle()
    
    print(f"Health Status: {result['health_status']['status']}")
    print(f"CPU Usage: {result['system_metrics']['cpu_percent']}%")
    print(f"Memory Usage: {result['system_metrics']['memory_percent']}%")
    print()


def example_with_config():
    """Example: Using configuration file"""
    print("=== Example 2: With Configuration File ===\n")
    
    # Create agent with config file
    agent = SentinelAgent(config_path='config.example.json')
    
    # Get health status
    health = agent.get_health_status()
    print(f"System Status: {health.status}")
    print(f"Uptime: {health.uptime_seconds:.2f} seconds")
    print()


def example_custom_metrics():
    """Example: Recording custom metrics"""
    print("=== Example 3: Custom Metrics ===\n")
    
    agent = SentinelAgent()
    
    # Simulate POS transaction metrics
    agent.record_metric('transactions_per_minute', 45, 'tpm')
    agent.record_metric('average_transaction_value', 125.50, 'USD')
    agent.record_metric('payment_processing_time', 250, 'ms')
    agent.record_metric('queue_length', 3, 'customers')
    
    # Get metrics summary
    summary = agent.get_metrics_summary()
    print(f"Total metrics recorded: {summary['total_metrics']}")
    print("\nLatest metrics:")
    for metric in summary['latest_metrics']:
        print(f"  - {metric['metric_name']}: {metric['value']} {metric['unit']} [{metric['status']}]")
    print()


def example_alert_monitoring():
    """Example: Alert monitoring"""
    print("=== Example 4: Alert Monitoring ===\n")
    
    # Configure with lower thresholds for demonstration
    agent = SentinelAgent()
    agent.alert_thresholds['test_metric'] = 50.0
    
    # Record some metrics
    agent.record_metric('test_metric', 30.0, 'units')  # Normal
    agent.record_metric('test_metric', 60.0, 'units')  # Alert!
    agent.record_metric('test_metric', 75.0, 'units')  # Alert!
    
    # Check for alerts
    alerts = agent.check_alerts()
    
    print(f"Active system alerts: {len(alerts)}")
    for alert in alerts:
        print(f"  ⚠️  {alert['metric']}: {alert['value']:.2f} > {alert['threshold']:.2f}")
    
    # Check custom metric alerts
    summary = agent.get_metrics_summary()
    alert_count = summary.get('alert_count', 0)
    print(f"\nTotal custom metric alerts: {alert_count}")
    print()


def example_continuous_monitoring():
    """Example: Continuous monitoring (short demo)"""
    print("=== Example 5: Continuous Monitoring (3 cycles) ===\n")
    
    agent = SentinelAgent()
    agent.config['monitoring_interval'] = 5  # 5 seconds for demo
    
    print("Monitoring for 3 cycles (5 seconds each)...\n")
    
    for i in range(3):
        print(f"--- Cycle {i+1} ---")
        result = agent.run_monitoring_cycle()
        
        health = result['health_status']
        print(f"Status: {health['status']}")
        print(f"CPU: {health['cpu_percent']:.1f}%")
        print(f"Memory: {health['memory_percent']:.1f}%")
        print(f"Alerts: {len(result['alerts'])}")
        print()
        
        if i < 2:  # Don't sleep after last iteration
            time.sleep(5)


def example_pos_health_check():
    """Example: POS endpoint health check"""
    print("=== Example 6: POS Health Check ===\n")
    
    agent = SentinelAgent()
    
    # Check a public endpoint (example.com)
    print("Checking example.com endpoint...")
    health = agent.check_pos_health(endpoint='http://example.com')
    
    print(f"Status: {health.get('status', 'unknown')}")
    if 'response_time_ms' in health:
        print(f"Response time: {health['response_time_ms']:.2f} ms")
    if 'status_code' in health:
        print(f"HTTP Status: {health['status_code']}")
    print()


def main():
    """Run all examples"""
    print("=" * 60)
    print("SentinelAgent - POS Monitoring Examples")
    print("=" * 60)
    print()
    
    try:
        example_basic_usage()
        time.sleep(1)
        
        example_custom_metrics()
        time.sleep(1)
        
        example_alert_monitoring()
        time.sleep(1)
        
        example_pos_health_check()
        time.sleep(1)
        
        # Uncomment to run config and continuous examples
        # example_with_config()
        # example_continuous_monitoring()
        
        print("=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\nExamples interrupted by user")
    except Exception as e:
        print(f"\nError running examples: {e}")


if __name__ == '__main__':
    main()
