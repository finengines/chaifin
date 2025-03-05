from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import logging
import json
from typing import Dict, Any, Optional, List, Union
import sys
import os

# Add the current directory to the path so we can import the status_updates module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Try to import the status_updates module
try:
    import status_updates
    import chainlit as cl
except ImportError:
    print("Warning: Could not import status_updates or chainlit. Status updates will be logged but not displayed.")
    status_updates = None
    cl = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("status-webhook")

# Create a FastAPI app
app = FastAPI(title="Status Updates Webhook Server")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify your allowed origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory queue for status updates
status_update_queue: List[Dict[str, Any]] = []

# Status update types mapping to functions
STATUS_TYPE_MAPPING = {
    "progress": "progress_status",
    "success": "success_status",
    "warning": "warning_status",
    "error": "error_status",
    "info": "info_status",
    "email": "email_status",
    "calendar": "calendar_status",
    "web-search": "web_search_status",
    "file-system": "file_system_status",
    "database": "database_status",
    "api": "api_status",
    "important-alert": "important_alert",
    "notification-alert": "notification_alert",
    "system-alert": "system_alert",
    "toast": "show_toast"
}

# Background task to process status updates
async def process_status_updates():
    while True:
        if status_update_queue and status_updates and cl:
            try:
                update = status_update_queue.pop(0)
                update_type = update.get("type", "info")
                content = update.get("content", "")
                
                # Extract additional parameters
                title = update.get("title", "Status Update")
                icon = update.get("icon", None)
                progress = update.get("progress", None)
                duration = update.get("duration", 3000)
                
                # Call the appropriate function based on the type
                if update_type in STATUS_TYPE_MAPPING:
                    function_name = STATUS_TYPE_MAPPING[update_type]
                    if hasattr(status_updates, function_name):
                        func = getattr(status_updates, function_name)
                        
                        # Handle special case for toast
                        if function_name == "show_toast":
                            await func(content, update_type, duration)
                        # Handle special case for progress status
                        elif function_name == "progress_status":
                            await func(title, content, progress, icon)
                        # Handle all other status updates
                        else:
                            await func(title, content, icon)
                    else:
                        logger.warning(f"Function {function_name} not found in status_updates module")
                else:
                    logger.warning(f"Unknown status update type: {update_type}")
                    
            except Exception as e:
                logger.error(f"Error processing status update: {str(e)}")
        
        # Sleep to avoid high CPU usage
        await asyncio.sleep(0.1)

# Start the background task when the app starts
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(process_status_updates())
    logger.info("Status webhook server started on port 5679")

# Webhook endpoint to receive status updates
@app.post("/status")
async def status_webhook(request: Request):
    try:
        data = await request.json()
        logger.info(f"Received status update: {data}")
        
        # Validate required fields
        if "content" not in data:
            raise HTTPException(status_code=400, detail="Missing required field: content")
        
        if "type" not in data:
            data["type"] = "info"  # Default to info type
            
        # Add to queue for processing
        status_update_queue.append(data)
        
        return {"status": "success", "message": "Status update received"}
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing webhook: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "queue_size": len(status_update_queue)}

# Run the FastAPI app with uvicorn when executed directly
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5679) 