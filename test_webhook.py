"""
Test script to verify that the webhook integration is working correctly for task lists.
"""

import requests
import time
import json
import argparse

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Test webhook integration")
    parser.add_argument("--port", type=int, default=5681, help="Webhook server port")
    return parser.parse_args()

def send_webhook(data, port):
    """Send a webhook request to the status endpoint."""
    webhook_url = f"http://localhost:{port}/status"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
        print(f"Response: {response.status_code} - {response.text}")
        return response
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to webhook server at {webhook_url}")
        return None

def test_task_list(port):
    """Test the task list webhook integration."""
    print("\n=== Testing Task List Webhook Integration ===\n")
    
    # 1. Create a task list with all tasks at once
    print("1. Creating complete task list...")
    complete_data = {
        "type": "task_list",
        "title": "Processing Your Request",
        "tasks": [
            {"name": "Understanding request", "status": "running", "icon": "loader"},
            {"name": "Retrieving information", "status": "ready", "icon": "clock"},
            {"name": "Generating response", "status": "ready", "icon": "clock"}
        ]
    }
    send_webhook(complete_data, port)
    time.sleep(2)
    
    # 2. Update tasks one by one
    print("\n2. Updating tasks one by one...")
    updates = [
        {"name": "Understanding request", "status": "done", "icon": "check-circle"},
        {"name": "Retrieving information", "status": "running", "icon": "loader"},
        {"name": "Retrieving information", "status": "done", "icon": "check-circle"},
        {"name": "Generating response", "status": "running", "icon": "loader"},
        {"name": "Generating response", "status": "done", "icon": "check-circle"}
    ]
    
    for update in updates:
        update_data = {
            "type": "task-list-update",
            **update
        }
        send_webhook(update_data, port)
        time.sleep(2)
    
    # 3. Close the task list with is_final flag
    print("\n3. Closing the task list...")
    close_data = {
        "type": "task-list-update",
        "name": "Final Status",
        "status": "done",
        "icon": "check-circle",
        "is_final": True
    }
    send_webhook(close_data, port)
    time.sleep(2)
    
    print("\n=== Task List Webhook Integration Test Complete ===\n")

def test_simple_task_list(port):
    """Test a simpler task list workflow."""
    print("\n=== Testing Simple Task List Workflow ===\n")
    
    # 1. Create a task list
    print("1. Creating task list...")
    create_data = {
        "type": "task-list-create",
        "title": "Simple Task List"
    }
    send_webhook(create_data, port)
    time.sleep(1)
    
    # 2. Add tasks
    print("\n2. Adding tasks...")
    tasks = [
        {"name": "Task 1", "status": "running", "icon": "loader"},
        {"name": "Task 2", "status": "ready", "icon": "clock"},
        {"name": "Task 3", "status": "ready", "icon": "clock"}
    ]
    
    for task in tasks:
        add_data = {
            "type": "task-list-add",
            **task
        }
        send_webhook(add_data, port)
        time.sleep(1)
    
    # 3. Complete tasks
    print("\n3. Completing tasks...")
    for task_name in ["Task 1", "Task 2", "Task 3"]:
        update_data = {
            "type": "task-list-update",
            "name": task_name,
            "status": "done",
            "icon": "check-circle"
        }
        send_webhook(update_data, port)
        time.sleep(1)
    
    # 4. Close the task list
    print("\n4. Closing the task list...")
    close_data = {
        "type": "task-list-update",
        "name": "Final Status",
        "status": "done",
        "icon": "check-circle",
        "is_final": True
    }
    send_webhook(close_data, port)
    time.sleep(1)
    
    print("\n=== Simple Task List Test Complete ===\n")

if __name__ == "__main__":
    args = parse_args()
    test_task_list(args.port)
    test_simple_task_list(args.port) 