"""
Test script to verify the connection to the n8n webhook.
"""

import json
import requests
import uuid
import time
from config import N8N_WEBHOOK_URL, DEFAULT_PROVIDER, DEFAULT_MODEL, REQUEST_TIMEOUT

def test_n8n_connection():
    """Test the connection to the n8n webhook."""
    # Generate a test session ID
    session_id = str(uuid.uuid4())
    
    # Prepare the test payload
    payload = {
        "chatInput": "Hello, this is a test message. How are you?",
        "sessionID": session_id,
        "provider": DEFAULT_PROVIDER,
        "model": DEFAULT_MODEL
    }
    
    print(f"Testing connection to n8n webhook at: {N8N_WEBHOOK_URL}")
    print(f"Using provider: {DEFAULT_PROVIDER}, model: {DEFAULT_MODEL}")
    print(f"Sending payload: {json.dumps(payload, indent=2)}")
    
    try:
        # Make the POST request to n8n
        headers = {"Content-Type": "application/json"}
        
        print("\nSending request...")
        start_time = time.time()
        
        response = requests.post(
            N8N_WEBHOOK_URL,
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT
        )
        
        response_time = time.time() - start_time
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Parse and print the JSON response
        json_response = response.json()
        print("\nResponse received successfully!")
        print(f"Status code: {response.status_code}")
        print(f"Response time: {response_time:.2f} seconds")
        print(f"Response: {json.dumps(json_response, indent=2)}")
        
        return True
    
    except requests.exceptions.Timeout:
        print(f"\nError: Request timed out after {REQUEST_TIMEOUT} seconds")
        return False
    
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the n8n webhook. Please check if the n8n service is running.")
        return False
    
    except requests.exceptions.RequestException as e:
        print(f"\nError making request to n8n: {str(e)}")
        return False
    
    except json.JSONDecodeError as e:
        print(f"\nError decoding JSON response: {str(e)}")
        print(f"Raw response: {response.text}")
        return False

if __name__ == "__main__":
    test_n8n_connection() 