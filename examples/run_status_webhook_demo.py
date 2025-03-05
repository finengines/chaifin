"""
Status Webhook Demo Runner

This script provides a convenient way to start the status webhook server
and run the demo.
"""

import subprocess
import time
import sys
import os
import signal
import argparse

def start_webhook_server():
    """Start the status webhook server in a separate process"""
    print("Starting Status Webhook Server...")
    
    # Start the webhook server in a separate process
    server_process = subprocess.Popen(
        [sys.executable, "status_webhook_server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for the server to start
    print("Waiting for server to start...")
    time.sleep(2)
    
    return server_process

def run_demo():
    """Run the demo by starting the webhook server and sending test notifications."""
    print("Starting status webhook server...")
    server_process = subprocess.Popen(
        [sys.executable, "scripts/status_webhook_server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    
    # Wait for the server to start
    time.sleep(2)
    
    # Run the test script
    print("Sending test notifications...")
    subprocess.run([sys.executable, "tests/test_status_webhook.py", "--demo"])
    
    # Wait for a moment to see the results
    time.sleep(5)
    
    # Stop the server
    print("Stopping the server...")
    server_process.terminate()
    server_process.wait()

def run_n8n_demo():
    """Run the n8n integration demo"""
    print("\nRunning n8n Integration Demo...")
    
    # Run the n8n integration demo script
    subprocess.run([sys.executable, "n8n_integration_example.py"])

def main():
    parser = argparse.ArgumentParser(description="Run the Status Webhook Demo")
    parser.add_argument("--no-server", action="store_true", help="Don't start the webhook server (use if it's already running)")
    parser.add_argument("--n8n", action="store_true", help="Run the n8n integration demo instead of the standard demo")
    parser.add_argument("--test-only", action="store_true", help="Only test if the server is running, don't run the demo")
    
    args = parser.parse_args()
    
    server_process = None
    
    try:
        # Start the webhook server if needed
        if not args.no_server:
            server_process = start_webhook_server()
        
        # Test if the server is running
        test_result = subprocess.run(
            [sys.executable, "test_webhook_server.py"],
            capture_output=True,
            text=True
        )
        
        if test_result.returncode != 0:
            print("Error: Webhook server is not running or not functioning correctly.")
            print(test_result.stdout)
            print(test_result.stderr)
            return 1
        
        # If test-only flag is set, don't run the demo
        if args.test_only:
            print("Server test successful. Exiting without running demo.")
            return 0
        
        # Run the appropriate demo
        if args.n8n:
            run_n8n_demo()
        else:
            run_demo()
        
        return 0
    
    except KeyboardInterrupt:
        print("\nInterrupted by user. Shutting down...")
        return 1
    
    finally:
        # Clean up the server process if we started it
        if server_process:
            print("\nStopping webhook server...")
            if sys.platform == "win32":
                server_process.terminate()
            else:
                os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
            
            server_process.wait()
            print("Webhook server stopped.")

if __name__ == "__main__":
    sys.exit(main()) 