"""
Test Integrated Webhook

This script tests the integrated webhook server by sending a series of status updates.
"""

import requests
import time
import sys
import logging
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test-webhook")

def test_integrated_webhook():
    """Test the integrated webhook server"""
    
    logger.info("Testing Integrated Webhook Server...")
    
    # Check if the server is running
    try:
        health_response = requests.get("http://localhost:5679/health")
        health_response.raise_for_status()
        health_data = health_response.json()
        
        logger.info(f"Server is running: {health_data}")
    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to webhook server. Make sure the Chainlit app is running")
        logger.error("Run: chainlit run app.py")
        return False
    except Exception as e:
        logger.error(f"Error checking server health: {str(e)}")
        logger.error(traceback.format_exc())
        return False
    
    # Send a series of status updates
    updates = [
        {
            "type": "info",
            "title": "Starting Test",
            "content": "Beginning the integrated webhook test..."
        },
        {
            "type": "progress",
            "title": "Test Progress",
            "content": "Testing progress updates...",
            "progress": 25
        },
        {
            "type": "progress",
            "title": "Test Progress",
            "content": "Testing progress updates...",
            "progress": 50
        },
        {
            "type": "warning",
            "title": "Test Warning",
            "content": "This is a test warning message."
        },
        {
            "type": "progress",
            "title": "Test Progress",
            "content": "Testing progress updates...",
            "progress": 75
        },
        {
            "type": "error",
            "title": "Test Error",
            "content": "This is a test error message."
        },
        {
            "type": "progress",
            "title": "Test Progress",
            "content": "Testing progress updates...",
            "progress": 100
        },
        {
            "type": "success",
            "title": "Test Complete",
            "content": "The integrated webhook test has completed successfully!"
        },
        {
            "type": "toast",
            "content": "Test completed!",
            "duration": 5000
        }
    ]
    
    # Send each update with a delay
    for i, update in enumerate(updates):
        try:
            logger.info(f"Sending update {i+1}/{len(updates)}: {update['title'] if 'title' in update else update['content']}")
            
            response = requests.post("http://localhost:5679/status", json=update)
            response.raise_for_status()
            
            logger.info(f"Update sent successfully: {response.json()}")
            
            # Wait between updates
            time.sleep(2)
        except Exception as e:
            logger.error(f"Error sending update: {str(e)}")
            logger.error(traceback.format_exc())
            return False
    
    logger.info("All updates sent successfully!")
    logger.info("Check the Chainlit UI to verify that the updates are displayed correctly.")
    return True

if __name__ == "__main__":
    try:
        success = test_integrated_webhook()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}")
        logger.error(traceback.format_exc())
        sys.exit(1) 