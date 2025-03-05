#!/usr/bin/env python3
"""
Simple test script to verify the webhook server is running and can receive notifications.
"""

import requests
import json
import time
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger("webhook-test")

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

def send_test_notification(notification_type="toast", url="http://localhost:5679/status"):
    """Send a test notification to the webhook server"""
    
    # Create notification data based on type
    if notification_type == "toast":
        data = {
            "type": "toast",
            "content": "Test toast notification",
            "toast_type": "info",
            "duration": 5000
        }
    elif notification_type == "status":
        data = {
            "type": "info",
            "title": "Test Status",
            "content": "This is a test status update",
            "icon": "info"
        }
    elif notification_type == "progress":
        data = {
            "type": "progress",
            "title": "Test Progress",
            "content": "This is a test progress update",
            "progress": 50,
            "icon": "loader"
        }
    else:
        logger.error(f"Unknown notification type: {notification_type}")
        return False
    
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

def main():
    """Main function"""
    # Check if the server is running
    health_data = check_server_health()
    if not health_data:
        logger.error("Webhook server is not running or not healthy")
        logger.info("Make sure the Chainlit application is running with: chainlit run app.py")
        return 1
    
    # Check if the server is processing status updates
    if not health_data.get("chainlit_processing", False):
        logger.warning("Webhook server is running but Chainlit is not processing status updates")
    
    # Send a test notification
    notification_type = "toast"
    if len(sys.argv) > 1:
        notification_type = sys.argv[1]
    
    logger.info(f"Sending test {notification_type} notification...")
    if send_test_notification(notification_type):
        logger.info(f"Test {notification_type} notification sent successfully")
        return 0
    else:
        logger.error(f"Failed to send test {notification_type} notification")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 