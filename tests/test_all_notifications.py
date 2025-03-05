#!/usr/bin/env python3
"""
Comprehensive test script to verify all notification types in the Chainlit UI.
This script sends various notification types to the webhook server in sequence.
"""

import requests
import json
import time
import logging
import sys
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger("notification-test")

def check_server_health(url="http://localhost:5679/health"):
    """Check if the webhook server is running and healthy"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Server health: {data}")
            return data
        else:
            logger.error(f"Server returned status code {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        logger.error(f"Could not connect to {url}")
        return None
    except Exception as e:
        logger.error(f"Error checking server health: {str(e)}")
        return None

def send_notification(data, url="http://localhost:5679/status"):
    """Send a notification to the webhook server"""
    try:
        response = requests.post(url, json=data, timeout=5)
        if response.status_code == 200:
            response_data = response.json()
            logger.info(f"Notification sent successfully: {data}")
            logger.info(f"Response: {response_data}")
            return True
        else:
            logger.error(f"Server returned status code {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        logger.error(f"Could not connect to {url}")
        return False
    except Exception as e:
        logger.error(f"Error sending notification: {str(e)}")
        return False

def test_toast_notifications():
    """Test toast notifications"""
    logger.info("Testing toast notifications...")
    
    # Test different toast types
    toast_types = ["info", "success", "warning", "error"]
    
    for toast_type in toast_types:
        data = {
            "type": "toast",
            "content": f"This is a {toast_type} toast notification",
            "toast_type": toast_type,
            "duration": 5000
        }
        
        if not send_notification(data):
            logger.error(f"Failed to send {toast_type} toast notification")
            return False
        
        time.sleep(1)  # Wait between notifications
    
    logger.info("All toast notifications sent successfully")
    return True

def test_status_notifications():
    """Test status notifications"""
    logger.info("Testing status notifications...")
    
    # Test different status types
    status_types = [
        {"type": "success", "icon": "check-circle"},
        {"type": "warning", "icon": "alert-triangle"},
        {"type": "error", "icon": "alert-circle"},
        {"type": "info", "icon": "info"}
    ]
    
    for status in status_types:
        data = {
            "type": status["type"],
            "title": f"{status['type'].capitalize()} Status",
            "content": f"This is a {status['type']} status notification",
            "icon": status["icon"]
        }
        
        if not send_notification(data):
            logger.error(f"Failed to send {status['type']} status notification")
            return False
        
        time.sleep(1)  # Wait between notifications
    
    logger.info("All status notifications sent successfully")
    return True

def test_agent_status_notifications():
    """Test agent status notifications"""
    logger.info("Testing agent status notifications...")
    
    # Test different agent status types
    agent_types = [
        {"type": "email", "icon": "mail"},
        {"type": "calendar", "icon": "calendar"},
        {"type": "web-search", "icon": "search"},
        {"type": "file-system", "icon": "folder"},
        {"type": "database", "icon": "database"},
        {"type": "api", "icon": "code"}
    ]
    
    for agent in agent_types:
        data = {
            "type": agent["type"],
            "title": f"{agent['type'].capitalize()} Agent",
            "content": f"This is a {agent['type']} agent status notification",
            "icon": agent["icon"]
        }
        
        if not send_notification(data):
            logger.error(f"Failed to send {agent['type']} agent status notification")
            return False
        
        time.sleep(1)  # Wait between notifications
    
    logger.info("All agent status notifications sent successfully")
    return True

def test_alert_notifications():
    """Test alert notifications"""
    logger.info("Testing alert notifications...")
    
    # Test different alert types
    alert_types = [
        {"type": "important_alert", "icon": "alert-circle"},
        {"type": "notification_alert", "icon": "bell"},
        {"type": "system_alert", "icon": "info"}
    ]
    
    for alert in alert_types:
        data = {
            "type": alert["type"],
            "title": f"{alert['type'].replace('_', ' ').capitalize()}",
            "content": f"This is a {alert['type'].replace('_', ' ')} notification",
            "icon": alert["icon"]
        }
        
        if not send_notification(data):
            logger.error(f"Failed to send {alert['type']} notification")
            return False
        
        time.sleep(1)  # Wait between notifications
    
    logger.info("All alert notifications sent successfully")
    return True

def test_progress_notification():
    """Test progress notification"""
    logger.info("Testing progress notification...")
    
    data = {
        "type": "progress",
        "title": "Progress Update",
        "content": "This is a progress update notification",
        "progress": 50,
        "icon": "loader"
    }
    
    if not send_notification(data):
        logger.error("Failed to send progress notification")
        return False
    
    logger.info("Progress notification sent successfully")
    return True

def test_task_list_notification():
    """Test task list notification"""
    logger.info("Testing task list notification...")
    
    data = {
        "type": "task_list",
        "title": "Task List",
        "tasks": [
            {"name": "Task 1", "status": "completed", "icon": "check-circle"},
            {"name": "Task 2", "status": "completed", "icon": "check-circle"},
            {"name": "Task 3", "status": "running", "icon": "loader"},
            {"name": "Task 4", "status": "waiting", "icon": "clock"}
        ]
    }
    
    if not send_notification(data):
        logger.error("Failed to send task list notification")
        return False
    
    logger.info("Task list notification sent successfully")
    return True

def test_animated_progress_notification():
    """Test animated progress notification"""
    logger.info("Testing animated progress notification...")
    
    data = {
        "type": "animated_progress",
        "title": "Animated Progress",
        "content": "This is an animated progress notification",
        "steps": [
            "Step 1: Initializing...",
            "Step 2: Loading data...",
            "Step 3: Processing data...",
            "Step 4: Finalizing..."
        ],
        "delay": 1.0
    }
    
    if not send_notification(data):
        logger.error("Failed to send animated progress notification")
        return False
    
    logger.info("Animated progress notification sent successfully")
    return True

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Test Chainlit notifications")
    parser.add_argument("--toast", action="store_true", help="Test toast notifications")
    parser.add_argument("--status", action="store_true", help="Test status notifications")
    parser.add_argument("--agent", action="store_true", help="Test agent status notifications")
    parser.add_argument("--alert", action="store_true", help="Test alert notifications")
    parser.add_argument("--progress", action="store_true", help="Test progress notification")
    parser.add_argument("--task-list", action="store_true", help="Test task list notification")
    parser.add_argument("--animated", action="store_true", help="Test animated progress notification")
    parser.add_argument("--all", action="store_true", help="Test all notification types")
    
    args = parser.parse_args()
    
    # Check if the server is running
    health_data = check_server_health()
    if not health_data:
        logger.error("Webhook server is not running or not healthy")
        logger.info("Make sure the Chainlit application is running with: chainlit run app.py")
        return 1
    
    # Check if the server is processing status updates
    if not health_data.get("chainlit_processing", False):
        logger.warning("Webhook server is running but Chainlit is not processing status updates")
    
    # Run the selected tests
    if args.toast or args.all:
        if not test_toast_notifications():
            return 1
    
    if args.status or args.all:
        if not test_status_notifications():
            return 1
    
    if args.agent or args.all:
        if not test_agent_status_notifications():
            return 1
    
    if args.alert or args.all:
        if not test_alert_notifications():
            return 1
    
    if args.progress or args.all:
        if not test_progress_notification():
            return 1
    
    if args.task_list or args.all:
        if not test_task_list_notification():
            return 1
    
    if args.animated or args.all:
        if not test_animated_progress_notification():
            return 1
    
    # If no specific test was selected, run all tests
    if not any([args.toast, args.status, args.agent, args.alert, args.progress, args.task_list, args.animated, args.all]):
        logger.info("No specific test selected, running all tests...")
        if not test_toast_notifications():
            return 1
        if not test_status_notifications():
            return 1
        if not test_agent_status_notifications():
            return 1
        if not test_alert_notifications():
            return 1
        if not test_progress_notification():
            return 1
        if not test_task_list_notification():
            return 1
        if not test_animated_progress_notification():
            return 1
    
    logger.info("All tests completed successfully")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 