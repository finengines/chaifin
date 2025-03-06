"""
Simple Webhook Server

This file creates a simple webhook server that can handle task list updates.
"""

from fastapi import FastAPI, Request
import uvicorn
import json
import asyncio
import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger("webhook_server")

# Create a FastAPI app
app = FastAPI(title="Simple Webhook Server")

# Chainlit app URL
CHAINLIT_URL = "http://localhost:8007"

@app.post("/status")
async def status_webhook(request: Request):
    """Receive status updates and forward them to the Chainlit app."""
    try:
        # Get the request body
        body = await request.body()
        
        # Parse the JSON data
        data = json.loads(body)
        logger.info(f"Received status update: {data}")
        
        # Process the status update
        update_type = data.get("type")
        
        if update_type == "task_list":
            # Create a task list in the Chainlit app
            await create_task_list_in_chainlit(data)
        elif update_type == "task-list-update":
            # Update a task in the Chainlit app
            await update_task_in_chainlit(data)
        
        return {
            "status": "success",
            "message": "Status update received and processed",
        }
    except Exception as e:
        logger.error(f"Error processing status update: {str(e)}")
        return {
            "status": "error",
            "message": f"Error processing status update: {str(e)}",
        }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "server_running": True,
    }

async def create_task_list_in_chainlit(data):
    """Create a task list in the Chainlit app by simulating user input."""
    # This is a placeholder function
    # In a real implementation, you would use the Chainlit API to create a task list
    logger.info(f"Creating task list in Chainlit: {data}")
    
    # Simulate a delay
    await asyncio.sleep(1)
    
    return True

async def update_task_in_chainlit(data):
    """Update a task in the Chainlit app by simulating user input."""
    # This is a placeholder function
    # In a real implementation, you would use the Chainlit API to update a task
    logger.info(f"Updating task in Chainlit: {data}")
    
    # Simulate a delay
    await asyncio.sleep(1)
    
    return True

if __name__ == "__main__":
    # Run the webhook server
    uvicorn.run(app, host="0.0.0.0", port=5682) 