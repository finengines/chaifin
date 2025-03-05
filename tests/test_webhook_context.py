#!/usr/bin/env python3
"""
Test script to diagnose and fix the "Chainlit context not found" error.
This script simulates sending status updates to the webhook server and checks if they're being processed correctly.
"""

import requests
import json
import time
import sys
import logging
import argparse
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger("test-webhook")

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

def run_test_sequence():
    """Run a sequence of test status updates"""
    logger.info("Starting test sequence...")
    
    # Check if the server is running
    if not check_server_health():
        logger.error("Webhook server is not running or not healthy")
        logger.info("Make sure the Chainlit application is running with: chainlit run app.py")
        return False
    
    # Wait a moment to ensure the server is ready
    time.sleep(1)
    
    # Send a simple info status update
    info_update = {
        "type": "info",
        "title": "Test Info",
        "content": "This is a test info status update"
    }
    if not send_status_update(info_update):
        logger.error("Failed to send info status update")
        return False
    
    # Wait a moment to allow processing
    time.sleep(1)
    
    # Send a progress status update
    progress_update = {
        "type": "progress",
        "title": "Test Progress",
        "content": "This is a test progress status update",
        "progress": 50
    }
    if not send_status_update(progress_update):
        logger.error("Failed to send progress status update")
        return False
    
    # Wait a moment to allow processing
    time.sleep(1)
    
    # Send a toast notification
    toast_update = {
        "type": "toast",
        "content": "This is a test toast notification",
        "duration": 3000
    }
    if not send_status_update(toast_update):
        logger.error("Failed to send toast notification")
        return False
    
    # Wait a moment to allow processing
    time.sleep(1)
    
    # Send a success status update
    success_update = {
        "type": "success",
        "title": "Test Success",
        "content": "This is a test success status update"
    }
    if not send_status_update(success_update):
        logger.error("Failed to send success status update")
        return False
    
    # Wait a moment to allow processing
    time.sleep(1)
    
    # Check server health again
    if not check_server_health():
        logger.error("Webhook server is not running or not healthy after tests")
        return False
    
    logger.info("Test sequence completed successfully")
    return True

def main():
    parser = argparse.ArgumentParser(description="Test the webhook server and diagnose context errors")
    parser.add_argument("--health", action="store_true", help="Check if the webhook server is running")
    parser.add_argument("--test", action="store_true", help="Run a test sequence of status updates")
    parser.add_argument("--info", action="store_true", help="Send an info status update")
    parser.add_argument("--progress", action="store_true", help="Send a progress status update")
    parser.add_argument("--toast", action="store_true", help="Send a toast notification")
    parser.add_argument("--success", action="store_true", help="Send a success status update")
    parser.add_argument("--warning", action="store_true", help="Send a warning status update")
    parser.add_argument("--error", action="store_true", help="Send an error status update")
    
    args = parser.parse_args()
    
    if args.health:
        if check_server_health():
            logger.info("Webhook server is running and healthy")
        else:
            logger.error("Webhook server is not running or not healthy")
            sys.exit(1)
    
    elif args.test:
        if run_test_sequence():
            logger.info("All tests passed")
        else:
            logger.error("Some tests failed")
            sys.exit(1)
    
    elif args.info:
        info_update = {
            "type": "info",
            "title": "Test Info",
            "content": "This is a test info status update"
        }
        if send_status_update(info_update):
            logger.info("Info status update sent successfully")
        else:
            logger.error("Failed to send info status update")
            sys.exit(1)
    
    elif args.progress:
        progress_update = {
            "type": "progress",
            "title": "Test Progress",
            "content": "This is a test progress status update",
            "progress": 50
        }
        if send_status_update(progress_update):
            logger.info("Progress status update sent successfully")
        else:
            logger.error("Failed to send progress status update")
            sys.exit(1)
    
    elif args.toast:
        toast_update = {
            "type": "toast",
            "content": "This is a test toast notification",
            "duration": 3000
        }
        if send_status_update(toast_update):
            logger.info("Toast notification sent successfully")
        else:
            logger.error("Failed to send toast notification")
            sys.exit(1)
    
    elif args.success:
        success_update = {
            "type": "success",
            "title": "Test Success",
            "content": "This is a test success status update"
        }
        if send_status_update(success_update):
            logger.info("Success status update sent successfully")
        else:
            logger.error("Failed to send success status update")
            sys.exit(1)
    
    elif args.warning:
        warning_update = {
            "type": "warning",
            "title": "Test Warning",
            "content": "This is a test warning status update"
        }
        if send_status_update(warning_update):
            logger.info("Warning status update sent successfully")
        else:
            logger.error("Failed to send warning status update")
            sys.exit(1)
    
    elif args.error:
        error_update = {
            "type": "error",
            "title": "Test Error",
            "content": "This is a test error status update"
        }
        if send_status_update(error_update):
            logger.info("Error status update sent successfully")
        else:
            logger.error("Failed to send error status update")
            sys.exit(1)
    
    else:
        # Default to running the test sequence
        if run_test_sequence():
            logger.info("All tests passed")
        else:
            logger.error("Some tests failed")
            sys.exit(1)

if __name__ == "__main__":
    main() 