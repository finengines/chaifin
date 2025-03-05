#!/usr/bin/env python3
"""
Test script to verify different notification types in Chainlit.
This script sends various notification types to the webhook server.
"""

import requests
import json
import time
import logging
import argparse
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger("test-notifications")

def check_server_health(url: str = "http://localhost:5679/health") -> bool:
    """Check if the webhook server is running and healthy"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Server health: {data}")
            return True
        else:
            logger.error(f"Server returned status code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        logger.error(f"Could not connect to {url}")
        return False
    except Exception as e:
        logger.error(f"Error checking server health: {str(e)}")
        return False

def send_status_update(data: Dict[str, Any], url: str = "http://localhost:5679/status") -> bool:
    """Send a status update to the webhook server"""
    try:
        response = requests.post(url, json=data, timeout=5)
        if response.status_code == 200:
            logger.info(f"Status update sent successfully: {data}")
            logger.info(f"Response: {response.json()}")
            return True
        else:
            logger.error(f"Server returned status code {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        logger.error(f"Could not connect to {url}")
        return False
    except Exception as e:
        logger.error(f"Error sending status update: {str(e)}")
        return False

def test_toast_notifications():
    """Test toast notifications"""
    logger.info("Testing toast notifications...")
    
    # Check if the server is running
    if not check_server_health():
        logger.error("Webhook server is not running or not healthy")
        logger.info("Make sure the Chainlit application is running with: chainlit run app.py")
        return False
    
    # Wait a moment to ensure the server is ready
    time.sleep(1)
    
    # Send a toast notification
    toast = {
        "type": "toast",
        "content": "This is a toast notification",
        "toast_type": "info",
        "duration": 5000  # 5 seconds
    }
    if not send_status_update(toast):
        logger.error("Failed to send toast notification")
        return False
    
    logger.info("Toast notification sent successfully")
    return True

def test_status_updates():
    """Test different status update types"""
    logger.info("Testing status updates...")
    
    # Check if the server is running
    if not check_server_health():
        logger.error("Webhook server is not running or not healthy")
        logger.info("Make sure the Chainlit application is running with: chainlit run app.py")
        return False
    
    # Wait a moment to ensure the server is ready
    time.sleep(1)
    
    # Test different status update types
    status_types = [
        {
            "type": "success",
            "title": "Success Status",
            "content": "This is a success status update",
            "icon": "check-circle"
        },
        {
            "type": "warning",
            "title": "Warning Status",
            "content": "This is a warning status update",
            "icon": "alert-triangle"
        },
        {
            "type": "error",
            "title": "Error Status",
            "content": "This is an error status update",
            "icon": "alert-circle"
        },
        {
            "type": "info",
            "title": "Info Status",
            "content": "This is an info status update",
            "icon": "info"
        },
        {
            "type": "email",
            "title": "Email Status",
            "content": "This is an email status update",
            "icon": "mail"
        },
        {
            "type": "calendar",
            "title": "Calendar Status",
            "content": "This is a calendar status update",
            "icon": "calendar"
        },
        {
            "type": "web-search",
            "title": "Web Search Status",
            "content": "This is a web search status update",
            "icon": "search"
        },
        {
            "type": "file-system",
            "title": "File System Status",
            "content": "This is a file system status update",
            "icon": "folder"
        },
        {
            "type": "database",
            "title": "Database Status",
            "content": "This is a database status update",
            "icon": "database"
        },
        {
            "type": "api",
            "title": "API Status",
            "content": "This is an API status update",
            "icon": "code"
        }
    ]
    
    for status in status_types:
        if not send_status_update(status):
            logger.error(f"Failed to send {status['type']} status update")
            return False
        time.sleep(1)  # Wait between status updates
    
    logger.info("All status updates sent successfully")
    return True

def test_progress_updates():
    """Test progress updates"""
    logger.info("Testing progress updates...")
    
    # Check if the server is running
    if not check_server_health():
        logger.error("Webhook server is not running or not healthy")
        logger.info("Make sure the Chainlit application is running with: chainlit run app.py")
        return False
    
    # Wait a moment to ensure the server is ready
    time.sleep(1)
    
    # Send a progress update
    progress = {
        "type": "progress",
        "title": "Progress Update",
        "content": "Processing data...",
        "progress": 50,
        "icon": "loader"
    }
    if not send_status_update(progress):
        logger.error("Failed to send progress update")
        return False
    
    logger.info("Progress update sent successfully")
    return True

def test_animated_progress():
    """Test animated progress"""
    logger.info("Testing animated progress...")
    
    # Check if the server is running
    if not check_server_health():
        logger.error("Webhook server is not running or not healthy")
        logger.info("Make sure the Chainlit application is running with: chainlit run app.py")
        return False
    
    # Wait a moment to ensure the server is ready
    time.sleep(1)
    
    # Send an animated progress update
    animated_progress = {
        "type": "animated_progress",
        "title": "Animated Progress",
        "content": "Processing steps...",
        "steps": [
            "Step 1: Initializing...",
            "Step 2: Loading data...",
            "Step 3: Processing data...",
            "Step 4: Finalizing..."
        ],
        "delay": 1.0
    }
    if not send_status_update(animated_progress):
        logger.error("Failed to send animated progress update")
        return False
    
    logger.info("Animated progress update sent successfully")
    return True

def test_alerts():
    """Test different alert types"""
    logger.info("Testing alerts...")
    
    # Check if the server is running
    if not check_server_health():
        logger.error("Webhook server is not running or not healthy")
        logger.info("Make sure the Chainlit application is running with: chainlit run app.py")
        return False
    
    # Wait a moment to ensure the server is ready
    time.sleep(1)
    
    # Test different alert types
    alert_types = [
        {
            "type": "important_alert",
            "title": "Important Alert",
            "content": "This is an important alert",
            "icon": "alert-circle"
        },
        {
            "type": "notification_alert",
            "title": "Notification Alert",
            "content": "This is a notification alert",
            "icon": "bell"
        },
        {
            "type": "system_alert",
            "title": "System Alert",
            "content": "This is a system alert",
            "icon": "info"
        }
    ]
    
    for alert in alert_types:
        if not send_status_update(alert):
            logger.error(f"Failed to send {alert['type']} alert")
            return False
        time.sleep(1)  # Wait between alerts
    
    logger.info("All alerts sent successfully")
    return True

def test_task_list():
    """Test task list"""
    logger.info("Testing task list...")
    
    # Check if the server is running
    if not check_server_health():
        logger.error("Webhook server is not running or not healthy")
        logger.info("Make sure the Chainlit application is running with: chainlit run app.py")
        return False
    
    # Wait a moment to ensure the server is ready
    time.sleep(1)
    
    # Send a task list update
    task_list = {
        "type": "task_list",
        "title": "Processing Tasks",
        "tasks": [
            {
                "name": "Initialize System",
                "status": "completed",
                "icon": "check-circle"
            },
            {
                "name": "Load Data",
                "status": "completed",
                "icon": "check-circle"
            },
            {
                "name": "Process Data",
                "status": "running",
                "icon": "loader"
            },
            {
                "name": "Generate Report",
                "status": "waiting",
                "icon": "clock"
            }
        ]
    }
    if not send_status_update(task_list):
        logger.error("Failed to send task list update")
        return False
    
    logger.info("Task list update sent successfully")
    return True

def test_all_notifications():
    """Test all notification types"""
    logger.info("Testing all notification types...")
    
    # Run all tests
    tests = [
        test_toast_notifications,
        test_status_updates,
        test_progress_updates,
        test_animated_progress,
        test_alerts,
        test_task_list
    ]
    
    for test_func in tests:
        if not test_func():
            logger.error(f"Test {test_func.__name__} failed")
            return False
        time.sleep(2)  # Wait between tests
    
    logger.info("All notification tests completed successfully")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Chainlit notifications")
    parser.add_argument("--toast", action="store_true", help="Test toast notifications")
    parser.add_argument("--status", action="store_true", help="Test status updates")
    parser.add_argument("--progress", action="store_true", help="Test progress updates")
    parser.add_argument("--animated", action="store_true", help="Test animated progress")
    parser.add_argument("--alerts", action="store_true", help="Test alerts")
    parser.add_argument("--task-list", action="store_true", help="Test task list")
    parser.add_argument("--all", action="store_true", help="Test all notification types")
    
    args = parser.parse_args()
    
    if args.toast:
        test_toast_notifications()
    elif args.status:
        test_status_updates()
    elif args.progress:
        test_progress_updates()
    elif args.animated:
        test_animated_progress()
    elif args.alerts:
        test_alerts()
    elif args.task_list:
        test_task_list()
    elif args.all:
        test_all_notifications()
    else:
        # Default to testing all notification types
        test_all_notifications() 