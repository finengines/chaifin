"""
Health check script for the Chainlit application.
"""

import os
import sys
import json
import requests
import time
import logging
from config import N8N_WEBHOOK_URL, REQUEST_TIMEOUT

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def check_n8n_connection():
    """Check if the n8n webhook is accessible."""
    try:
        # Make a simple HEAD request to check if the webhook is accessible
        response = requests.head(
            N8N_WEBHOOK_URL,
            timeout=REQUEST_TIMEOUT / 2  # Use a shorter timeout for the health check
        )
        
        # Return True if the status code is 2xx or 3xx
        return 200 <= response.status_code < 400
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to n8n webhook: {str(e)}")
        return False

def check_chainlit_process():
    """Check if the Chainlit process is running."""
    try:
        # This is a simple check that looks for a running process with 'chainlit' in the name
        # This approach is platform-dependent and may need to be adjusted
        if sys.platform.startswith('win'):
            # Windows
            import subprocess
            output = subprocess.check_output('tasklist', shell=True).decode()
            return 'chainlit' in output.lower()
        else:
            # Unix-like systems
            import subprocess
            output = subprocess.check_output(['ps', 'aux']).decode()
            return 'chainlit run app.py' in output
    
    except Exception as e:
        logger.error(f"Error checking Chainlit process: {str(e)}")
        return False

def run_health_check():
    """Run a comprehensive health check and return the results."""
    results = {
        "timestamp": time.time(),
        "n8n_connection": check_n8n_connection(),
        "chainlit_process": check_chainlit_process(),
        "overall_status": "healthy"
    }
    
    # If any check fails, mark the overall status as unhealthy
    if not all([results["n8n_connection"], results["chainlit_process"]]):
        results["overall_status"] = "unhealthy"
    
    return results

def print_health_check_results(results):
    """Print the health check results in a human-readable format."""
    print("\n=== Health Check Results ===")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(results['timestamp']))}")
    print(f"n8n Connection: {'✅' if results['n8n_connection'] else '❌'}")
    print(f"Chainlit Process: {'✅' if results['chainlit_process'] else '❌'}")
    print(f"Overall Status: {'✅ HEALTHY' if results['overall_status'] == 'healthy' else '❌ UNHEALTHY'}")
    print("===========================\n")

if __name__ == "__main__":
    # Run the health check
    results = run_health_check()
    
    # Print the results
    print_health_check_results(results)
    
    # Write the results to a file
    with open('health_check_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Exit with an appropriate status code
    sys.exit(0 if results["overall_status"] == "healthy" else 1) 