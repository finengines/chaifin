from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import json
import os
import threading
import time
import queue
import traceback
import socket
from typing import Dict, Any, List, Union, Optional
import asyncio
import uvicorn
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger("status_webhook")

# Create a global queue for status updates that can be accessed from other modules
STATUS_QUEUE: List[Dict[str, Any]] = []

# Flag to indicate if the webhook server is running
WEBHOOK_SERVER_RUNNING = False

# Server thread reference
WEBHOOK_SERVER_THREAD = None

# Status update types
STATUS_TYPES = [
    "progress", "success", "warning", "error", "info",
    "email", "calendar", "web-search", "file-system", 
    "database", "api", "important-alert", "notification-alert", 
    "system-alert", "toast"
]

# Create a FastAPI app
app = FastAPI(title="Status Webhook Server")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Webhook endpoint to receive status updates
@app.post("/status")
async def status_webhook(request: Request):
    """Receive status updates from external sources"""
    try:
        # Get the request body
        body = await request.body()
        
        # Parse the JSON data
        try:
            data = json.loads(body)
            logger.info(f"Received status update: {data}")
            
            # Add to queue for processing by Chainlit
            STATUS_QUEUE.append(data)
            
            return {
                "status": "success", 
                "message": "Status update received", 
                "queue_size": len(STATUS_QUEUE),
                "chainlit_processing": True,
                "server_running": WEBHOOK_SERVER_RUNNING
            }
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")
    except Exception as e:
        logger.error(f"Error processing status update: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error processing status update: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "server_running": WEBHOOK_SERVER_RUNNING,
        "queue_size": len(STATUS_QUEUE),
        "chainlit_processing": True
    }

def is_port_in_use(port: int) -> bool:
    """Check if a port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def stop_webhook_server():
    """Stop the webhook server if it's running"""
    global WEBHOOK_SERVER_RUNNING, WEBHOOK_SERVER_THREAD
    
    if WEBHOOK_SERVER_RUNNING:
        logger.info("Stopping webhook server...")
        WEBHOOK_SERVER_RUNNING = False
        
        # Wait for the server thread to terminate
        if WEBHOOK_SERVER_THREAD and WEBHOOK_SERVER_THREAD.is_alive():
            WEBHOOK_SERVER_THREAD.join(timeout=2)
            logger.info("Webhook server thread stopped")
        
        WEBHOOK_SERVER_THREAD = None
        return True
    
    return False

def start_webhook_server(host: str = "0.0.0.0", port: int = 5679):
    """Start the webhook server in a separate thread"""
    global WEBHOOK_SERVER_RUNNING, WEBHOOK_SERVER_THREAD
    
    # Stop any existing server
    stop_webhook_server()
    
    # Check if the port is already in use
    if is_port_in_use(port):
        logger.warning(f"Port {port} is already in use. Attempting to use a different port.")
        # Try a few different ports
        for alt_port in [5680, 5681, 5682, 5683]:
            if not is_port_in_use(alt_port):
                port = alt_port
                logger.info(f"Using alternative port {port}")
                break
        else:
            logger.error("Could not find an available port. Webhook server will not start.")
            return None
    
    def run_server():
        global WEBHOOK_SERVER_RUNNING
        logger.info(f"Starting status webhook server on {host}:{port}")
        
        try:
            import uvicorn
            WEBHOOK_SERVER_RUNNING = True
            uvicorn.run(app, host=host, port=port, log_level="info")
        except Exception as e:
            logger.error(f"Error running webhook server: {str(e)}")
            logger.error(traceback.format_exc())
        finally:
            logger.info("Status webhook server stopped")
            WEBHOOK_SERVER_RUNNING = False
    
    # Start the server in a separate thread
    WEBHOOK_SERVER_THREAD = threading.Thread(target=run_server, daemon=True)
    WEBHOOK_SERVER_THREAD.start()
    
    # Wait for the server to start
    time.sleep(1)
    
    # Verify the server is running
    if is_port_in_use(port):
        logger.info(f"Status webhook server started on http://{host}:{port}")
        return WEBHOOK_SERVER_THREAD
    else:
        logger.error(f"Failed to start webhook server on port {port}")
        WEBHOOK_SERVER_RUNNING = False
        return None

# Function to get the next status update from the queue (non-blocking)
def get_next_status_update() -> Optional[Dict[str, Any]]:
    """Get the next status update from the queue"""
    if STATUS_QUEUE:
        return STATUS_QUEUE.pop(0)
    return None

# Function to clear the queue
def clear_queue() -> None:
    """Clear all status updates from the queue"""
    global STATUS_QUEUE
    queue_size = len(STATUS_QUEUE)
    STATUS_QUEUE = []
    logger.info(f"Cleared status update queue ({queue_size} items)") 