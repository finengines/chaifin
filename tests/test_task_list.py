"""
Test Task List

This script tests the task list functionality by sending webhook requests.
"""

import requests
import json
import time
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test-task-list")

def send_webhook(data):
    """Send a webhook request to the status endpoint"""
    url = "http://localhost:5679/status"
    
    try:
        response = requests.post(
            url,
            data=json.dumps(data),
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            logger.info(f"Webhook sent successfully: {response.json()}")
            return True
        else:
            logger.error(f"Error sending webhook: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"Exception sending webhook: {str(e)}")
        return False

def test_task_list_create():
    """Test creating a task list"""
    logger.info("Testing task list creation...")
    
    data = {
        "type": "task-list-create",
        "title": "Processing Tasks"
    }
    
    return send_webhook(data)

def test_task_list_add():
    """Test adding tasks to a task list"""
    logger.info("Testing adding tasks to task list...")
    
    # Add first task
    data1 = {
        "type": "task-list-add",
        "name": "Loading Data",
        "status": "running",
        "icon": "loader"
    }
    
    success1 = send_webhook(data1)
    time.sleep(1)
    
    # Add second task
    data2 = {
        "type": "task-list-add",
        "name": "Processing Information",
        "status": "running",
        "icon": "cpu"
    }
    
    success2 = send_webhook(data2)
    time.sleep(1)
    
    # Add third task
    data3 = {
        "type": "task-list-add",
        "name": "Generating Results",
        "status": "pending",
        "icon": "file-text"
    }
    
    success3 = send_webhook(data3)
    
    return success1 and success2 and success3

def test_task_list_update():
    """Test updating tasks in a task list"""
    logger.info("Testing updating tasks in task list...")
    
    # Update first task
    data1 = {
        "type": "task-list-update",
        "name": "Loading Data",
        "status": "done",
        "icon": "check-circle"
    }
    
    success1 = send_webhook(data1)
    time.sleep(1)
    
    # Update second task
    data2 = {
        "type": "task-list-update",
        "name": "Processing Information",
        "status": "done",
        "icon": "check-circle"
    }
    
    success2 = send_webhook(data2)
    time.sleep(1)
    
    # Update third task
    data3 = {
        "type": "task-list-update",
        "name": "Generating Results",
        "status": "running",
        "icon": "loader"
    }
    
    success3 = send_webhook(data3)
    time.sleep(2)
    
    # Final update
    data4 = {
        "type": "task-list-update",
        "name": "Generating Results",
        "status": "done",
        "icon": "check-circle"
    }
    
    success4 = send_webhook(data4)
    
    return success1 and success2 and success3 and success4

def test_full_task_list_flow():
    """Test the full task list flow"""
    logger.info("Testing full task list flow...")
    
    # Create task list
    if not test_task_list_create():
        logger.error("Failed to create task list")
        return False
    
    time.sleep(1)
    
    # Add tasks
    if not test_task_list_add():
        logger.error("Failed to add tasks")
        return False
    
    time.sleep(1)
    
    # Update tasks
    if not test_task_list_update():
        logger.error("Failed to update tasks")
        return False
    
    logger.info("Full task list flow completed successfully")
    return True

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Test task list functionality")
    parser.add_argument("--create", action="store_true", help="Test task list creation")
    parser.add_argument("--add", action="store_true", help="Test adding tasks")
    parser.add_argument("--update", action="store_true", help="Test updating tasks")
    parser.add_argument("--full", action="store_true", help="Test full task list flow")
    
    args = parser.parse_args()
    
    if args.create:
        test_task_list_create()
    elif args.add:
        test_task_list_add()
    elif args.update:
        test_task_list_update()
    elif args.full:
        test_full_task_list_flow()
    else:
        # Default to full flow
        test_full_task_list_flow()

if __name__ == "__main__":
    main() 