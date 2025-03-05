#!/usr/bin/env python3
"""
Diagnostic script for the status webhook server.
This script helps diagnose issues with the status webhook server integration.
"""

import requests
import json
import sys
import time
import argparse
from typing import Dict, Any, Optional

def check_server_health(url: str = "http://localhost:5679/health") -> Optional[Dict[str, Any]]:
    """Check if the webhook server is running and healthy"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Server returned status code {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to {url}")
        return None
    except Exception as e:
        print(f"Error checking server health: {str(e)}")
        return None

def send_test_update(url: str = "http://localhost:5679/status") -> bool:
    """Send a test status update to the webhook server"""
    try:
        data = {
            "type": "info",
            "title": "Diagnostic Test",
            "content": f"Webhook diagnostic test at {time.strftime('%H:%M:%S')}"
        }
        
        response = requests.post(url, json=data, timeout=5)
        if response.status_code == 200:
            print(f"Success: Test update sent successfully")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"Error: Server returned status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to {url}")
        return False
    except Exception as e:
        print(f"Error sending test update: {str(e)}")
        return False

def run_comprehensive_test():
    """Run a comprehensive test of the webhook server"""
    print("\n=== Status Webhook Server Diagnostic Tool ===\n")
    
    # Step 1: Check if the server is running
    print("Step 1: Checking if the webhook server is running...")
    health_data = check_server_health()
    
    if health_data:
        print(f"✅ Webhook server is running")
        print(f"   Server status: {health_data.get('status', 'unknown')}")
        print(f"   Server running: {health_data.get('server_running', False)}")
        print(f"   Queue size: {health_data.get('queue_size', 'unknown')}")
    else:
        print("❌ Webhook server is not running or not responding")
        print("   Please check that the Chainlit application is running")
        print("   Command: chainlit run app.py")
        return False
    
    # Step 2: Send a test update
    print("\nStep 2: Sending a test status update...")
    if not send_test_update():
        print("❌ Failed to send test update")
        return False
    
    # Step 3: Send different types of updates
    print("\nStep 3: Testing different status update types...")
    
    # Test progress update
    try:
        print("   Sending progress update...")
        response = requests.post("http://localhost:5679/status", json={
            "type": "progress",
            "title": "Progress Test",
            "content": "Testing progress updates...",
            "progress": 75
        }, timeout=5)
        if response.status_code == 200:
            print("   ✅ Progress update sent successfully")
        else:
            print(f"   ❌ Failed to send progress update: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error sending progress update: {str(e)}")
    
    # Test toast notification
    try:
        print("   Sending toast notification...")
        response = requests.post("http://localhost:5679/status", json={
            "type": "toast",
            "content": "This is a test toast notification",
            "duration": 3000
        }, timeout=5)
        if response.status_code == 200:
            print("   ✅ Toast notification sent successfully")
        else:
            print(f"   ❌ Failed to send toast notification: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error sending toast notification: {str(e)}")
    
    # Final check
    print("\nStep 4: Final health check...")
    health_data = check_server_health()
    
    if health_data:
        print(f"✅ Webhook server is still running")
        print(f"   Queue size: {health_data.get('queue_size', 'unknown')}")
    else:
        print("❌ Webhook server is no longer responding")
        return False
    
    print("\n=== Diagnostic Test Complete ===")
    print("\nIf you see all checkmarks but updates are not appearing in the Chainlit UI:")
    print("1. Make sure the Chainlit application is running and processing status updates")
    print("2. Check the application logs for any errors")
    print("3. Verify that the background task for processing updates is running")
    print("4. Restart the Chainlit application and try again")
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Diagnose issues with the status webhook server")
    parser.add_argument("--health", action="store_true", help="Check if the webhook server is running")
    parser.add_argument("--test", action="store_true", help="Send a test status update")
    parser.add_argument("--comprehensive", action="store_true", help="Run a comprehensive diagnostic test")
    
    args = parser.parse_args()
    
    if args.health:
        health_data = check_server_health()
        if health_data:
            print(f"Webhook server is running")
            print(f"Status: {health_data.get('status', 'unknown')}")
            print(f"Server running: {health_data.get('server_running', False)}")
            print(f"Queue size: {health_data.get('queue_size', 'unknown')}")
        else:
            print("Webhook server is not running or not responding")
            sys.exit(1)
    
    elif args.test:
        if send_test_update():
            print("Test update sent successfully")
        else:
            print("Failed to send test update")
            sys.exit(1)
    
    elif args.comprehensive:
        if not run_comprehensive_test():
            sys.exit(1)
    
    else:
        # Default to comprehensive test if no arguments provided
        if not run_comprehensive_test():
            sys.exit(1)

if __name__ == "__main__":
    main() 