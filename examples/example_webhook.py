from fastapi import FastAPI, Request, Depends, HTTPException, Header
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
import chainlit as cl
from chainlit.server import app as chainlit_app
import json
import asyncio
import uuid
from typing import Dict, Any, Optional, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify your allowed origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Chainlit as a sub-application
app.mount("/chat", chainlit_app)

# API key security
API_KEY_NAME = "X-API-Key"
API_KEY = "your-secret-api-key"  # In production, use environment variables
api_key_header = APIKeyHeader(name=API_KEY_NAME)

# In-memory storage for webhook data (use a database in production)
webhook_data_store: Dict[str, List[Dict[str, Any]]] = {}

# Verify API key
async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

# Webhook endpoint to receive data
@app.post("/webhook", dependencies=[Depends(verify_api_key)])
async def webhook(request: Request):
    try:
        data = await request.json()
        
        # Log the received data
        logger.info(f"Received webhook data: {data}")
        
        # Extract user ID or generate one if not provided
        user_id = data.get("user_id", str(uuid.uuid4()))
        
        # Store the data
        if user_id not in webhook_data_store:
            webhook_data_store[user_id] = []
        
        webhook_data_store[user_id].append(data)
        
        return {"status": "success", "message": "Data received", "user_id": user_id}
    
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing webhook: {str(e)}")

# Endpoint to get data for a specific user
@app.get("/webhook/data/{user_id}", dependencies=[Depends(verify_api_key)])
async def get_webhook_data(user_id: str):
    if user_id not in webhook_data_store:
        return {"status": "success", "data": []}
    
    return {"status": "success", "data": webhook_data_store[user_id]}

# Endpoint to clear data for a specific user
@app.delete("/webhook/data/{user_id}", dependencies=[Depends(verify_api_key)])
async def clear_webhook_data(user_id: str):
    if user_id in webhook_data_store:
        del webhook_data_store[user_id]
    
    return {"status": "success", "message": f"Data cleared for user {user_id}"}

# Custom header for user identification
@app.get("/user/info")
async def get_user_info(x_user_id: Optional[str] = Header(None)):
    if not x_user_id:
        raise HTTPException(status_code=400, detail="X-User-Id header is required")
    
    # In a real app, you would fetch user info from a database
    return {
        "user_id": x_user_id,
        "name": f"User {x_user_id}",
        "role": "user"
    }

# Chainlit chat handlers
@cl.on_chat_start
async def on_chat_start():
    # Store a session ID in the user session
    session_id = str(uuid.uuid4())
    cl.user_session.set("session_id", session_id)
    
    # Welcome message
    await cl.Message(
        content=f"""
# Webhook Integration Demo

This demo shows how to integrate Chainlit with webhooks and backend routing.

- Your session ID: `{session_id}`
- Type `fetch` to retrieve webhook data
- Type `send` to simulate sending data to a webhook
- Type `clear` to clear your data
"""
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    session_id = cl.user_session.get("session_id")
    
    if message.content.lower() == "fetch":
        # Create a TaskList to show progress
        task_list = cl.TaskList(status="Fetching data...")
        fetch_task = cl.Task(title="Retrieving webhook data", status=cl.TaskStatus.RUNNING)
        await task_list.add_task(fetch_task)
        await task_list.send()
        
        # Simulate API call to fetch data
        await asyncio.sleep(1)
        
        # Get data for this session
        data = webhook_data_store.get(session_id, [])
        
        fetch_task.status = cl.TaskStatus.DONE
        task_list.status = "Data retrieved"
        await task_list.send()
        
        if not data:
            await cl.Message(content="No webhook data found for your session.").send()
        else:
            # Format the data as markdown
            data_md = "## Webhook Data\n\n"
            for i, item in enumerate(data):
                data_md += f"### Entry {i+1}\n```json\n{json.dumps(item, indent=2)}\n```\n\n"
            
            await cl.Message(content=data_md).send()
    
    elif message.content.lower() == "send":
        # Ask for data to send
        response = await cl.AskUserMessage(
            content="Enter the data you want to send to the webhook (JSON format):",
            timeout=180
        ).send()
        
        if response:
            try:
                # Parse the JSON data
                data = json.loads(response["content"])
                
                # Add session ID
                data["session_id"] = session_id
                
                # Create a TaskList to show progress
                task_list = cl.TaskList(status="Sending data...")
                send_task = cl.Task(title="Sending to webhook", status=cl.TaskStatus.RUNNING)
                await task_list.add_task(send_task)
                await task_list.send()
                
                # Simulate sending to webhook
                await asyncio.sleep(1)
                
                # Store the data
                if session_id not in webhook_data_store:
                    webhook_data_store[session_id] = []
                
                webhook_data_store[session_id].append(data)
                
                send_task.status = cl.TaskStatus.DONE
                task_list.status = "Data sent"
                await task_list.send()
                
                await cl.Message(content=f"Data sent successfully to webhook:\n```json\n{json.dumps(data, indent=2)}\n```").send()
            
            except json.JSONDecodeError:
                await cl.Message(content="Error: Invalid JSON format. Please try again.").send()
    
    elif message.content.lower() == "clear":
        # Clear data for this session
        if session_id in webhook_data_store:
            del webhook_data_store[session_id]
            await cl.Message(content="Your webhook data has been cleared.").send()
        else:
            await cl.Message(content="No data to clear.").send()
    
    elif message.content.lower() == "help":
        await cl.Message(
            content="""
## Available Commands

- `fetch`: Retrieve webhook data for your session
- `send`: Send data to the webhook
- `clear`: Clear your webhook data
- `help`: Show this help message
"""
        ).send()
    
    else:
        await cl.Message(
            content="I'm a webhook integration demo. Type `help` to see available commands."
        ).send()

# Run the FastAPI app with uvicorn when executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    # Note: To run this example, use:
    # python example_webhook.py
    # 
    # This will start both the FastAPI server and the Chainlit app.
    # Access the Chainlit interface at: http://localhost:8000/chat 