"""
n8n Integration Example for Status Updates

This script demonstrates how to integrate with n8n to send status updates
to the status webhook server.

Usage:
    python n8n_integration_example.py
"""

import requests
import json
import time
import os
import sys
from typing import Dict, Any, Optional

# Configuration
N8N_WEBHOOK_URL = os.environ.get("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/status")
STATUS_WEBHOOK_URL = "http://localhost:5679/status"  # Updated to use the correct webhook URL

def send_to_n8n(data: Dict[str, Any], webhook_url: str = N8N_WEBHOOK_URL) -> Dict[str, Any]:
    """
    Send data to n8n webhook.
    
    Args:
        data: The data to send
        webhook_url: The n8n webhook URL
        
    Returns:
        The response from n8n
    """
    try:
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
        return response.json() if response.text else {"status": "success"}
    except requests.exceptions.RequestException as e:
        print(f"Error sending to n8n: {str(e)}")
        return {"status": "error", "message": str(e)}

def send_direct_to_status_webhook(data: Dict[str, Any], webhook_url: str = STATUS_WEBHOOK_URL) -> Dict[str, Any]:
    """
    Send data directly to the status webhook server.
    
    Args:
        data: The data to send
        webhook_url: The status webhook URL
        
    Returns:
        The response from the webhook server
    """
    try:
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending to status webhook: {str(e)}")
        return {"status": "error", "message": str(e)}

def run_n8n_demo():
    """Run a demonstration of n8n integration"""
    print("Starting n8n integration demo...")
    
    # Check if n8n is running
    try:
        response = requests.get("http://localhost:5678/healthz")
        if response.status_code != 200:
            print("Warning: n8n doesn't appear to be running or the health endpoint is not available")
    except requests.exceptions.ConnectionError:
        print("Warning: Could not connect to n8n. Make sure it's running on localhost:5678")
        print("Continuing with direct webhook calls...")
    
    # Simulate a workflow with multiple steps
    steps = [
        {
            "type": "progress",
            "title": "Starting Workflow",
            "content": "Initializing workflow process...",
            "progress": 0
        },
        {
            "type": "progress",
            "title": "Data Collection",
            "content": "Collecting data from sources...",
            "progress": 20
        },
        {
            "type": "progress",
            "title": "Data Processing",
            "content": "Processing collected data...",
            "progress": 40
        },
        {
            "type": "warning",
            "title": "Processing Delay",
            "content": "Data processing is taking longer than expected."
        },
        {
            "type": "progress",
            "title": "Data Analysis",
            "content": "Analyzing processed data...",
            "progress": 60
        },
        {
            "type": "progress",
            "title": "Report Generation",
            "content": "Generating final report...",
            "progress": 80
        },
        {
            "type": "progress",
            "title": "Finalizing",
            "content": "Finalizing workflow process...",
            "progress": 95
        },
        {
            "type": "success",
            "title": "Workflow Complete",
            "content": "The workflow has completed successfully!"
        }
    ]
    
    # Process each step
    for step in steps:
        print(f"Sending step: {step['title']}")
        
        try:
            # Try to send to n8n first
            n8n_response = send_to_n8n(step)
            if n8n_response.get("status") == "error":
                # If n8n fails, send directly to the status webhook
                print("Falling back to direct webhook call...")
                send_direct_to_status_webhook(step)
        except Exception as e:
            print(f"Error: {str(e)}")
            # If n8n call fails, send directly to the status webhook
            send_direct_to_status_webhook(step)
        
        # Wait between steps
        time.sleep(2)
    
    print("\nDemo completed! All status updates have been sent.")

if __name__ == "__main__":
    run_n8n_demo() 