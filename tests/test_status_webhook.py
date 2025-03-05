import requests
import json
import time
import argparse
from typing import Dict, Any

def send_status_update(data: Dict[str, Any], webhook_url: str = "http://localhost:5679/status") -> Dict[str, Any]:
    """
    Send a status update to the webhook server.
    
    Args:
        data: The status update data to send
        webhook_url: The webhook URL (default: http://localhost:5679/status)
        
    Returns:
        The response from the webhook server
    """
    try:
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
        return {"status": "error", "message": str(e)}

def run_demo():
    """Run a demonstration of different status update types"""
    
    # Check if the webhook server is running
    try:
        health_check = requests.get("http://localhost:5679/health")
        if health_check.status_code != 200:
            print("Warning: Webhook server doesn't appear to be healthy")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to webhook server. Make sure it's running on localhost:5679")
        print("Run: python status_webhook_server.py")
        return
    
    print("Starting status updates demo...")
    
    # Progress status updates
    print("\nSending progress status updates...")
    for i in range(0, 101, 20):
        send_status_update({
            "type": "progress",
            "title": "Processing Data",
            "content": f"Processing data... {i}% complete",
            "progress": i
        })
        time.sleep(1)
    
    # Success status
    print("\nSending success status...")
    send_status_update({
        "type": "success",
        "title": "Task Completed",
        "content": "The task has been completed successfully!"
    })
    time.sleep(1)
    
    # Warning status
    print("\nSending warning status...")
    send_status_update({
        "type": "warning",
        "title": "Warning",
        "content": "This operation might take longer than expected."
    })
    time.sleep(1)
    
    # Error status
    print("\nSending error status...")
    send_status_update({
        "type": "error",
        "title": "Error Occurred",
        "content": "Failed to connect to the database."
    })
    time.sleep(1)
    
    # Info status
    print("\nSending info status...")
    send_status_update({
        "type": "info",
        "title": "Information",
        "content": "The system will be updated tomorrow."
    })
    time.sleep(1)
    
    # Email status
    print("\nSending email status...")
    send_status_update({
        "type": "email",
        "title": "Email Sent",
        "content": "Your email to john@example.com has been sent."
    })
    time.sleep(1)
    
    # Calendar status
    print("\nSending calendar status...")
    send_status_update({
        "type": "calendar",
        "title": "Meeting Scheduled",
        "content": "Team meeting scheduled for tomorrow at 10:00 AM."
    })
    time.sleep(1)
    
    # Web search status
    print("\nSending web search status...")
    send_status_update({
        "type": "web-search",
        "title": "Search Results",
        "content": "Found 5 results for your query."
    })
    time.sleep(1)
    
    # Toast notification
    print("\nSending toast notification...")
    send_status_update({
        "type": "toast",
        "content": "This is a toast notification",
        "duration": 5000  # 5 seconds
    })
    
    print("\nDemo completed! All status updates have been sent.")

def main():
    parser = argparse.ArgumentParser(description="Send status updates to the webhook server")
    parser.add_argument("--type", help="Status update type (progress, success, warning, error, info, etc.)")
    parser.add_argument("--title", help="Status update title")
    parser.add_argument("--content", help="Status update content")
    parser.add_argument("--progress", type=int, help="Progress percentage (0-100)")
    parser.add_argument("--icon", help="Icon name")
    parser.add_argument("--duration", type=int, help="Duration for toast notifications (in ms)")
    parser.add_argument("--demo", action="store_true", help="Run a demonstration of different status update types")
    
    args = parser.parse_args()
    
    if args.demo:
        run_demo()
        return
    
    if not args.content:
        print("Error: --content is required")
        parser.print_help()
        return
    
    data = {
        "content": args.content
    }
    
    if args.type:
        data["type"] = args.type
    
    if args.title:
        data["title"] = args.title
    
    if args.progress is not None:
        data["progress"] = args.progress
    
    if args.icon:
        data["icon"] = args.icon
    
    if args.duration:
        data["duration"] = args.duration
    
    response = send_status_update(data)
    print(f"Response: {json.dumps(response, indent=2)}")

if __name__ == "__main__":
    main() 