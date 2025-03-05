"""
Test Webhook Server

This script tests if the status webhook server is running and functioning correctly.
"""

import requests
import time
import sys

def test_webhook_server():
    """Test if the webhook server is running and functioning correctly"""
    
    print("Testing Status Webhook Server...")
    
    # Check if the server is running
    try:
        health_response = requests.get("http://localhost:5679/health")
        health_response.raise_for_status()
        health_data = health_response.json()
        
        print(f"✅ Server is running: {health_data}")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to webhook server. Make sure the Chainlit app is running")
        print("Run: chainlit run app.py")
        return False
    except Exception as e:
        print(f"❌ Error checking server health: {str(e)}")
        return False
    
    # Send a test status update
    try:
        test_data = {
            "type": "info",
            "title": "Test Status",
            "content": "This is a test status update."
        }
        
        print(f"Sending test status update: {test_data}")
        
        response = requests.post("http://localhost:5679/status", json=test_data)
        response.raise_for_status()
        
        print(f"✅ Test status update sent successfully: {response.json()}")
        
        # Send a test toast notification
        toast_data = {
            "type": "toast",
            "content": "This is a test toast notification",
            "duration": 3000
        }
        
        print(f"Sending test toast notification: {toast_data}")
        
        toast_response = requests.post("http://localhost:5679/status", json=toast_data)
        toast_response.raise_for_status()
        
        print(f"✅ Test toast notification sent successfully: {toast_response.json()}")
        
        return True
    except Exception as e:
        print(f"❌ Error sending test status update: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_webhook_server()
    sys.exit(0 if success else 1) 