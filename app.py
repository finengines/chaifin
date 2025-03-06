"""
Chainlit frontend for n8n-powered personal assistant.
"""

import uuid
import json
import logging
import requests
import time
import os
from typing import Dict, Any, List, Optional
import chainlit as cl
import asyncio

# Import configuration
import config

# Import status webhook integration
import status_webhook_integration

# Import status updates
from status_updates import (
    web_search_status,
    email_status,
    calendar_status,
    file_system_status,
    database_status,
    api_status,
    progress_status,
    success_status,
    warning_status,
    error_status,
    info_status,
    important_alert,
    notification_alert,
    system_alert,
    animated_progress,
    StyledTaskList,
    show_toast
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("chainlit_app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Stop any existing webhook server
status_webhook_integration.stop_webhook_server()
logger.info("Stopped any existing webhook server")

# Start the webhook server - ONLY ONCE at application startup
webhook_server_thread = status_webhook_integration.start_webhook_server(port=5679)
if webhook_server_thread:
    logger.info("Started status webhook server on port 5679")
else:
    logger.error("Failed to start webhook server. Notifications may not work correctly.")

@cl.set_chat_profiles
def chat_profiles():
    """Define available chat profiles based on providers and models."""
    profiles = []
    default_set = False
    
    print("Creating chat profiles...")
    
    # Create a factory function outside the loops to properly capture values
    def create_on_select_function(provider, model_id):
        """Create an on_select function with fixed provider and model_id values."""
        def on_select():
            print(f"Selected profile with provider: {provider}, model_id: {model_id}")
            logger.info(f"Selected profile with provider: {provider}, model_id: {model_id}")
            return {"provider": provider, "model_id": model_id}
        return on_select
    
    # Create OpenRouter profiles
    if "openrouter" in config.PROVIDER_MODELS:
        print(f"Creating OpenRouter profiles: {len(config.PROVIDER_MODELS['openrouter'])} models")
        for model in config.PROVIDER_MODELS["openrouter"]:
            profile = cl.ChatProfile(
                name=f"OpenRouter - {model['name']}",
                markdown_description=f"**{model['name']}**\n\n{model.get('description', 'OpenRouter model')}",
                icon="openrouter"
            )
            
            # Use the factory function to create a closure with fixed values
            profile.on_select = create_on_select_function("openrouter", model["id"])
            
            # Set  2.0 Flash as the default
            if model["id"] == "google/gemini-2.0-flash-001":
                profile.default = True
                default_set = True
                print(f"Setting default profile: OpenRouter - {model['name']}")
                
            profiles.append(profile)
    
    # Create OpenAI profiles
    if "openai" in config.PROVIDER_MODELS:
        for model in config.PROVIDER_MODELS["openai"]:
            profile = cl.ChatProfile(
                name=f"OpenAI - {model['name']}",
                markdown_description=f"**{model['name']}**\n\n{model.get('description', 'OpenAI model')}",
                icon="openai"
            )
            
            # Use the factory function to create a closure with fixed values
            profile.on_select = create_on_select_function("openai", model["id"])
            
            profiles.append(profile)
    
    # Create Anthropic profiles
    if "anthropic" in config.PROVIDER_MODELS:
        for model in config.PROVIDER_MODELS["anthropic"]:
            profile = cl.ChatProfile(
                name=f"Anthropic - {model['name']}",
                markdown_description=f"**{model['name']}**\n\n{model.get('description', 'Anthropic model')}",
                icon="anthropic"
            )
            
            # Use the factory function to create a closure with fixed values
            profile.on_select = create_on_select_function("anthropic", model["id"])
            
            profiles.append(profile)
    
    # Create Ollama profiles
    if "ollama" in config.PROVIDER_MODELS:
        for model in config.PROVIDER_MODELS["ollama"]:
            profile = cl.ChatProfile(
                name=f"Ollama - {model['name']}",
                markdown_description=f"**{model['name']}**\n\n{model.get('description', 'Ollama model')}",
                icon="ollama"
            )
            
            # Use the factory function to create a closure with fixed values
            profile.on_select = create_on_select_function("ollama", model["id"])
            
            profiles.append(profile)
    
    # Set a default profile if there are any profiles and no default was set
    if profiles and not default_set:
        profiles[0].default = True
    
    return profiles

@cl.on_chat_start
async def on_chat_start():
    """
    Initialize the chat session when a new user connects.
    It initializes the conversation history and sets the initial model.
    """
    print("Starting new chat session...")
    
    # Verify webhook server is running
    try:
        health_response = requests.get("http://localhost:5679/health", timeout=2)
        if health_response.status_code == 200:
            health_data = health_response.json()
            logger.info(f"Webhook server health: {health_data}")
            
            if not health_data.get("server_running", False):
                logger.warning("Webhook server reports it's not running. Attempting to restart...")
                # We'll only restart if the server reports it's not running
                status_webhook_integration.stop_webhook_server()
                # Properly restart the server when needed
                webhook_server_thread = status_webhook_integration.start_webhook_server(port=5679)
                if webhook_server_thread:
                    logger.info("Restarted webhook server successfully")
                else:
                    logger.error("Failed to restart webhook server")
        else:
            logger.warning(f"Webhook server health check failed with status code: {health_response.status_code}")
    except Exception as e:
        logger.error(f"Error checking webhook server health: {str(e)}")
        # Restart the server if the health check fails completely
        logger.info("Health check failed. Attempting to restart webhook server...")
        status_webhook_integration.stop_webhook_server()
        webhook_server_thread = status_webhook_integration.start_webhook_server(port=5679)
        if webhook_server_thread:
            logger.info("Restarted webhook server after health check failure")
        else:
            logger.error("Failed to restart webhook server after health check failure")
    
    # Start a background task to process status updates
    cl.user_session.set("process_status_updates", True)
    
    async def process_status_updates():
        """Process status updates from the queue"""
        logger.info("Starting status update processing task")
        
        # Clear any existing status updates in the queue
        status_webhook_integration.clear_queue()
        
        while cl.user_session.get("process_status_updates", True):
            try:
                # Check if there are any status updates in the queue
                update = status_webhook_integration.get_next_status_update()
                if update:
                    try:
                        # Extract update data
                        update_type = update.get("type", "info")
                        content = update.get("content", "")
                        title = update.get("title", "Status Update")
                        progress = update.get("progress", None)
                        duration = update.get("duration", 3000)
                        icon = update.get("icon", None)
                        
                        logger.info(f"Processing status update: {update_type} - {title}")
                        
                        # Handle different types of status updates
                        if update_type == "toast":
                            # Use only one method for toast notifications
                            toast_type = update.get("toast_type", "info")
                            try:
                                success = await show_toast(content, toast_type, duration)
                                if success:
                                    logger.info(f"Sent toast notification: {content}")
                                else:
                                    logger.warning(f"Failed to send toast notification: {content}")
                            except Exception as e:
                                logger.error(f"Error sending toast notification: {str(e)}")
                                
                                # Only if the above fails, use a fallback
                                try:
                                    msg = cl.Message(content=f"**{toast_type.upper()}**: {content}")
                                    await msg.send()
                                    logger.info(f"Sent fallback toast message: {content}")
                                except Exception as e2:
                                    logger.error(f"Error sending fallback toast message: {str(e2)}")
                        
                        elif update_type == "progress" and progress is not None:
                            # Use the progress status function
                            try:
                                await progress_status(title, content, progress, icon)
                                logger.info(f"Sent progress update: {progress}%")
                            except Exception as e:
                                logger.error(f"Error sending progress update: {str(e)}")
                                # Fallback: Send as a regular message
                                msg = cl.Message(content=f"**Progress ({progress}%)**: {content}")
                                await msg.send()
                        
                        elif update_type == "task_list":
                            # Handle task list updates
                            try:
                                tasks = update.get("tasks", [])
                                
                                # Create a native Chainlit TaskList following the official documentation
                                task_list = cl.TaskList(title=title)
                                
                                # First message to associate with tasks
                                first_message = await cl.Message(content=f"Processing: {title}").send()
                                
                                # Add tasks to the list
                                for i, task in enumerate(tasks):
                                    task_name = task.get("name", f"Task {i+1}")
                                    task_status = task.get("status", "running")
                                    task_icon = task.get("icon", None)
                                    
                                    # Convert string status to TaskStatus enum
                                    status_enum = cl.TaskStatus.RUNNING
                                    if task_status == "done":
                                        status_enum = cl.TaskStatus.DONE
                                    elif task_status == "failed":
                                        status_enum = cl.TaskStatus.FAILED
                                    elif task_status == "ready":
                                        status_enum = cl.TaskStatus.READY
                                    
                                    # Create the task
                                    task_obj = cl.Task(title=task_name, status=status_enum, icon=task_icon)
                                    
                                    # Link the first task to the first message
                                    if i == 0:
                                        task_obj.forId = first_message.id
                                    
                                    # Add the task to the list
                                    await task_list.add_task(task_obj)
                                
                                # Send the task list to display it on the right side
                                await task_list.send()
                                
                                # Store the task list and tasks in the user session
                                cl.user_session.set("current_task_list", task_list)
                                cl.user_session.set("current_tasks", {task.get("name"): task for task in tasks})
                                
                                logger.info(f"Created task list with {len(tasks)} tasks")
                            except Exception as e:
                                logger.error(f"Error creating task list: {str(e)}")
                                # Fallback: Send as a regular message
                                msg = cl.Message(content=f"**Task List**: {title}")
                                await msg.send()
                        
                        elif update_type == "task-list-create":
                            # Handle task list creation
                            try:
                                # Create a native Chainlit TaskList
                                task_list = cl.TaskList(title=title)
                                
                                # Send the task list to display it on the right side
                                await task_list.send()
                                
                                # Store the task list in the user session
                                cl.user_session.set("current_task_list", task_list)
                                cl.user_session.set("current_tasks", {})
                                
                                logger.info(f"Created task list: {title}")
                            except Exception as e:
                                logger.error(f"Error creating task list: {str(e)}")
                                # Fallback: Send as a regular message
                                msg = cl.Message(content=f"**Task List**: {title}")
                                await msg.send()
                        
                        elif update_type == "task-list-add":
                            # Handle adding a task to the task list
                            try:
                                task_name = update.get("name", "Task")
                                task_status = update.get("status", "running")
                                task_icon = update.get("icon", None)
                                
                                # Get the current task list or create a new one
                                task_list = cl.user_session.get("current_task_list")
                                current_tasks = cl.user_session.get("current_tasks", {})
                                
                                if not task_list:
                                    # Create a new task list
                                    task_list = cl.TaskList(title="Processing Tasks")
                                    
                                    # Send the task list to display it
                                    await task_list.send()
                                    
                                    # Store the task list in the user session
                                    cl.user_session.set("current_task_list", task_list)
                                    current_tasks = {}
                                
                                # Create a message for this task
                                task_message = await cl.Message(content=f"**{task_name}**: Started").send()
                                
                                # Convert string status to TaskStatus enum
                                status_enum = cl.TaskStatus.RUNNING
                                if task_status == "done":
                                    status_enum = cl.TaskStatus.DONE
                                elif task_status == "failed":
                                    status_enum = cl.TaskStatus.FAILED
                                elif task_status == "ready":
                                    status_enum = cl.TaskStatus.READY
                                
                                # Create and add the task
                                task_obj = cl.Task(title=task_name, status=status_enum, icon=task_icon)
                                task_obj.forId = task_message.id  # Link the task to the message
                                await task_list.add_task(task_obj)
                                
                                # Update the current tasks
                                current_tasks[task_name] = {"status": task_status, "icon": task_icon}
                                cl.user_session.set("current_tasks", current_tasks)
                                
                                # Send the task list to update the UI
                                await task_list.send()
                                
                                logger.info(f"Added task to task list: {task_name}")
                            except Exception as e:
                                logger.error(f"Error adding task to task list: {str(e)}")
                                # Fallback: Send as a regular message
                                msg = cl.Message(content=f"**Task**: {update.get('name', 'Task')} ({update.get('status', 'running')})")
                                await msg.send()
                        
                        elif update_type == "task-list-update":
                            # Handle updating a task in the task list
                            try:
                                task_name = update.get("name", "Task")
                                task_status = update.get("status", "running")
                                task_icon = update.get("icon", None)
                                
                                # Get the current task list
                                task_list = cl.user_session.get("current_task_list")
                                
                                if task_list:
                                    # Create a message for this update
                                    update_message = await cl.Message(content=f"**{task_name}**: {task_status.capitalize()}").send()
                                    
                                    # Find the task to update
                                    found_task = None
                                    for task in task_list.tasks:
                                        if task.title == task_name:
                                            found_task = task
                                            break
                                    
                                    if found_task:
                                        # Update the task status
                                        if task_status == "done":
                                            found_task.status = cl.TaskStatus.DONE
                                        elif task_status == "failed":
                                            found_task.status = cl.TaskStatus.FAILED
                                        elif task_status == "ready":
                                            found_task.status = cl.TaskStatus.READY
                                        elif task_status == "running":
                                            found_task.status = cl.TaskStatus.RUNNING
                                        
                                        # Update the task icon if provided
                                        if task_icon:
                                            found_task.icon = task_icon
                                        
                                        # Link the task to the new message
                                        found_task.forId = update_message.id
                                    else:
                                        # Task not found, create a new one
                                        # Convert string status to TaskStatus enum
                                        status_enum = cl.TaskStatus.RUNNING
                                        if task_status == "done":
                                            status_enum = cl.TaskStatus.DONE
                                        elif task_status == "failed":
                                            status_enum = cl.TaskStatus.FAILED
                                        elif task_status == "ready":
                                            status_enum = cl.TaskStatus.READY
                                        
                                        # Create and add the task
                                        task_obj = cl.Task(title=task_name, status=status_enum, icon=task_icon)
                                        task_obj.forId = update_message.id  # Link the task to the message
                                        await task_list.add_task(task_obj)
                                    
                                    # Send the task list to update the UI
                                    await task_list.send()
                                    
                                    logger.info(f"Updated task in task list: {task_name} to {task_status}")
                                else:
                                    logger.warning("No task list found to update task")
                                    # Create a new task list
                                    task_list = cl.TaskList(title="Processing Tasks")
                                    
                                    # Create a message for this task
                                    task_message = await cl.Message(content=f"**{task_name}**: {task_status.capitalize()}").send()
                                    
                                    # Convert string status to TaskStatus enum
                                    status_enum = cl.TaskStatus.RUNNING
                                    if task_status == "done":
                                        status_enum = cl.TaskStatus.DONE
                                    elif task_status == "failed":
                                        status_enum = cl.TaskStatus.FAILED
                                    elif task_status == "ready":
                                        status_enum = cl.TaskStatus.READY
                                    
                                    # Create and add the task
                                    task_obj = cl.Task(title=task_name, status=status_enum, icon=task_icon)
                                    task_obj.forId = task_message.id  # Link the task to the message
                                    await task_list.add_task(task_obj)
                                    
                                    # Send the task list to display it
                                    await task_list.send()
                                    
                                    # Store the task list in the user session
                                    cl.user_session.set("current_task_list", task_list)
                                    cl.user_session.set("current_tasks", {task_name: {"status": task_status, "icon": task_icon}})
                                    
                                    logger.info(f"Created new task list and added task: {task_name}")
                            except Exception as e:
                                logger.error(f"Error updating task in task list: {str(e)}")
                                # Fallback: Send as a regular message
                                msg = cl.Message(content=f"**Task Update**: {update.get('name', 'Task')} ({update.get('status', 'running')})")
                                await msg.send()
                        
                        elif update_type == "animated_progress":
                            # Handle animated progress
                            try:
                                steps = update.get("steps", [])
                                delay = update.get("delay", 0.5)
                                await animated_progress(title, content, steps, delay)
                                logger.info(f"Sent animated progress with {len(steps)} steps")
                            except Exception as e:
                                logger.error(f"Error sending animated progress: {str(e)}")
                                # Fallback: Send as a regular message
                                steps = update.get("steps", [])
                                steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)])
                                msg = cl.Message(content=f"**{title}**\n{content}\n\n{steps_text}")
                                await msg.send()
                        
                        elif update_type == "important_alert":
                            # Handle important alert
                            try:
                                await important_alert(title, content, icon)
                                logger.info(f"Sent important alert: {title}")
                            except Exception as e:
                                logger.error(f"Error sending important alert: {str(e)}")
                                # Fallback: Send as a regular message
                                msg = cl.Message(content=f"**IMPORTANT ALERT: {title}**\n{content}")
                                await msg.send()
                        
                        elif update_type == "notification_alert":
                            # Handle notification alert
                            try:
                                await notification_alert(title, content, icon)
                                logger.info(f"Sent notification alert: {title}")
                            except Exception as e:
                                logger.error(f"Error sending notification alert: {str(e)}")
                                # Fallback: Send as a regular message
                                msg = cl.Message(content=f"**NOTIFICATION: {title}**\n{content}")
                                await msg.send()
                        
                        elif update_type == "system_alert":
                            # Handle system alert
                            try:
                                await system_alert(title, content, icon)
                                logger.info(f"Sent system alert: {title}")
                            except Exception as e:
                                logger.error(f"Error sending system alert: {str(e)}")
                                # Fallback: Send as a regular message
                                msg = cl.Message(content=f"**SYSTEM ALERT: {title}**\n{content}")
                                await msg.send()
                        
                        elif update_type == "success":
                            # Handle success status
                            try:
                                await success_status(title, content, icon)
                                logger.info(f"Sent success status: {title}")
                            except Exception as e:
                                logger.error(f"Error sending success status: {str(e)}")
                                # Fallback: Send as a regular message
                                msg = cl.Message(content=f"**✅ SUCCESS: {title}**\n{content}")
                                await msg.send()
                        
                        elif update_type == "warning":
                            # Handle warning status
                            try:
                                await warning_status(title, content, icon)
                                logger.info(f"Sent warning status: {title}")
                            except Exception as e:
                                logger.error(f"Error sending warning status: {str(e)}")
                                # Fallback: Send as a regular message
                                msg = cl.Message(content=f"**⚠️ WARNING: {title}**\n{content}")
                                await msg.send()
                        
                        elif update_type == "error":
                            # Handle error status
                            try:
                                await error_status(title, content, icon)
                                logger.info(f"Sent error status: {title}")
                            except Exception as e:
                                logger.error(f"Error sending error status: {str(e)}")
                                # Fallback: Send as a regular message
                                msg = cl.Message(content=f"**❌ ERROR: {title}**\n{content}")
                                await msg.send()
                        
                        elif update_type == "info":
                            # Handle info status
                            try:
                                await info_status(title, content, icon)
                                logger.info(f"Sent info status: {title}")
                            except Exception as e:
                                logger.error(f"Error sending info status: {str(e)}")
                                # Fallback: Send as a regular message
                                msg = cl.Message(content=f"**ℹ️ INFO: {title}**\n{content}")
                                await msg.send()
                        
                        elif update_type == "email":
                            # Handle email status
                            try:
                                await email_status(title, content, icon)
                                logger.info(f"Sent email status: {title}")
                            except Exception as e:
                                logger.error(f"Error sending email status: {str(e)}")
                                # Fallback: Send as a regular message
                                msg = cl.Message(content=f"**📧 EMAIL: {title}**\n{content}")
                                await msg.send()
                        
                        elif update_type == "calendar":
                            # Handle calendar status
                            try:
                                await calendar_status(title, content, icon)
                                logger.info(f"Sent calendar status: {title}")
                            except Exception as e:
                                logger.error(f"Error sending calendar status: {str(e)}")
                                # Fallback: Send as a regular message
                                msg = cl.Message(content=f"**📅 CALENDAR: {title}**\n{content}")
                                await msg.send()
                        
                        elif update_type == "web-search":
                            # Handle web search status
                            try:
                                await web_search_status(title, content, icon)
                                logger.info(f"Sent web search status: {title}")
                            except Exception as e:
                                logger.error(f"Error sending web search status: {str(e)}")
                                # Fallback: Send as a regular message
                                msg = cl.Message(content=f"**🔍 WEB SEARCH: {title}**\n{content}")
                                await msg.send()
                        
                        elif update_type == "file-system":
                            # Handle file system status
                            try:
                                await file_system_status(title, content, icon)
                                logger.info(f"Sent file system status: {title}")
                            except Exception as e:
                                logger.error(f"Error sending file system status: {str(e)}")
                                # Fallback: Send as a regular message
                                msg = cl.Message(content=f"**📁 FILE SYSTEM: {title}**\n{content}")
                                await msg.send()
                        
                        elif update_type == "database":
                            # Handle database status
                            try:
                                await database_status(title, content, icon)
                                logger.info(f"Sent database status: {title}")
                            except Exception as e:
                                logger.error(f"Error sending database status: {str(e)}")
                                # Fallback: Send as a regular message
                                msg = cl.Message(content=f"**🗄️ DATABASE: {title}**\n{content}")
                                await msg.send()
                        
                        elif update_type == "api":
                            # Handle API status
                            try:
                                await api_status(title, content, icon)
                                logger.info(f"Sent API status: {title}")
                            except Exception as e:
                                logger.error(f"Error sending API status: {str(e)}")
                                # Fallback: Send as a regular message
                                msg = cl.Message(content=f"**🔌 API: {title}**\n{content}")
                                await msg.send()
                        
                        else:
                            # For other status types, use a custom element
                            try:
                                element = cl.CustomElement(
                                    name="StatusUpdate",
                                    props={
                                        "type": update_type,
                                        "title": title,
                                        "message": content,
                                        "icon": icon
                                    }
                                )
                                msg = cl.Message(content="", elements=[element])
                                await msg.send()
                                logger.info(f"Sent custom status update: {update_type}")
                            except Exception as e:
                                logger.error(f"Error sending custom status update: {str(e)}")
                                # Fallback: Send as a regular message
                                msg = cl.Message(content=f"**{update_type.upper()}: {title}**\n{content}")
                                await msg.send()
                        
                        logger.info(f"Successfully processed status update: {update}")
                    except Exception as e:
                        logger.error(f"Error processing status update: {str(e)}", exc_info=True)
                        # Don't try to send an error message as it might fail for the same reason
            except Exception as e:
                logger.error(f"Error in status update processing loop: {str(e)}", exc_info=True)
            
            # Sleep to avoid high CPU usage
            await asyncio.sleep(0.1)
        
        logger.info("Status update processing task stopped")
    
    # Start the background task
    asyncio.create_task(process_status_updates())
    logger.info("Started background task to process status updates")
    
    # Generate a unique session ID
    session_id = str(uuid.uuid4())
    cl.user_session.set("session_id", session_id)
    print(f"Session ID: {session_id}")
    logger.info(f"Starting new chat session with ID: {session_id}")
    
    # Get the selected chat profile from the user session
    profile_name = cl.user_session.get("chat_profile")
    print(f"Selected chat profile from session: {profile_name}")
    logger.info(f"Selected chat profile from session: {profile_name}")
    
    # Get all available profiles
    profiles = chat_profiles()
    print(f"Available profiles: {[p.name for p in profiles]}")
    logger.info(f"Available profiles: {[p.name for p in profiles]}")
    
    # Find the matching profile
    profile_data = None
    
    # If a profile name is provided, find the matching profile
    if profile_name:
        profile_data = next((p for p in profiles if p.name == profile_name), None)
        
        if not profile_data:
            logger.warning(f"No matching profile found for name: {profile_name}")
            
            # Find the default profile
            profile_data = next((p for p in profiles if hasattr(p, 'default') and p.default), None)
            
            if profile_data:
                logger.info(f"Using default profile: {profile_data.name}")
                # Update the profile name in the session
                cl.user_session.set("chat_profile", profile_data.name)
            else:
                # Use the first profile as a fallback
                profile_data = profiles[0] if profiles else None
                if profile_data:
                    logger.info(f"Using first profile as fallback: {profile_data.name}")
                    # Update the profile name in the session
                    cl.user_session.set("chat_profile", profile_data.name)
        else:
            logger.info(f"Found matching profile: {profile_data.name}")
    else:
        # No profile name provided, use the default profile
        profile_data = next((p for p in profiles if hasattr(p, 'default') and p.default), None)
        
        if profile_data:
            logger.info(f"Using default profile: {profile_data.name}")
            # Update the profile name in the session
            cl.user_session.set("chat_profile", profile_data.name)
        else:
            # Use the first profile as a fallback
            profile_data = profiles[0] if profiles else None
            if profile_data:
                logger.info(f"Using first profile as fallback: {profile_data.name}")
                # Update the profile name in the session
                cl.user_session.set("chat_profile", profile_data.name)
    
    # Get the callback data from the profile
    profile_settings = {}
    if profile_data and hasattr(profile_data, 'on_select') and callable(profile_data.on_select):
        profile_settings = profile_data.on_select()
        logger.info(f"Profile on_select returned: {profile_settings}")
    else:
        if profile_data:
            logger.warning(f"Profile {profile_data.name} does not have an on_select method")
        else:
            logger.warning("No valid profile data found")
    
    # Set the provider and model from the profile
    provider = profile_settings.get("provider", config.DEFAULT_PROVIDER)
    model_id = profile_settings.get("model_id", config.DEFAULT_MODEL)
    
    # Store the provider and model in the user session
    cl.user_session.set("provider", provider)
    cl.user_session.set("model", model_id)
    logger.info(f"Using provider: {provider}, model: {model_id}")
    
    # Initialize conversation history
    cl.user_session.set("conversation_history", [])
    
    # Send a welcome message
    model_name = "Unknown Model"
    if provider in config.PROVIDER_MODELS:
        for model_config in config.PROVIDER_MODELS[provider]:
            if model_config["id"] == model_id:
                model_name = model_config["name"]
                break
    
    # Remove the system notification about the selected profile
    # Send only the welcome message
    await cl.Message(
        content=f"Hello! I'm your personal assistant powered by {model_name}. How can I help you today?",
        author="Assistant"
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    """
    Handle incoming messages from the user.
    
    This function is called when a user sends a message.
    It processes the message and sends it to n8n for processing.
    
    Args:
        message: The incoming message from the user
    """
    try:
        print(f"Received message: {message.content}")
        
        # Get the session ID
        session_id = cl.user_session.get("session_id")
        if not session_id:
            session_id = str(uuid.uuid4())
            cl.user_session.set("session_id", session_id)
            print(f"Created new session ID: {session_id}")
            logger.info(f"Created new session ID: {session_id}")
        
        # Get the current chat profile from the user session
        current_profile_name = cl.user_session.get("chat_profile")
        print(f"Current chat profile from session: {current_profile_name}")
        logger.info(f"Current chat profile from session: {current_profile_name}")
        
        # Get all available profiles
        profiles = chat_profiles()
        print(f"Available profiles: {[p.name for p in profiles]}")
        logger.info(f"Available profiles: {[p.name for p in profiles]}")
        
        # Find the matching profile
        selected_profile = None
        if current_profile_name:
            selected_profile = next((p for p in profiles if p.name == current_profile_name), None)
            if selected_profile:
                print(f"Found matching profile: {selected_profile.name}")
                logger.info(f"Found matching profile: {selected_profile.name}")
            else:
                print(f"No matching profile found for name: {current_profile_name}")
                logger.warning(f"No matching profile found for name: {current_profile_name}")
        
        # Get the provider and model from the user session
        provider = cl.user_session.get("provider")
        model_id = cl.user_session.get("model")
        
        # If we have a selected profile, update the provider and model
        if selected_profile and hasattr(selected_profile, 'on_select') and callable(selected_profile.on_select):
            profile_settings = selected_profile.on_select()
            if profile_settings and isinstance(profile_settings, dict):
                provider = profile_settings.get("provider", provider)
                model_id = profile_settings.get("model_id", model_id)
                print(f"Selected profile with provider: {provider}, model_id: {model_id}")
                logger.info(f"Selected profile with provider: {provider}, model_id: {model_id}")
                print(f"Profile on_select returned: {profile_settings}")
                logger.info(f"Profile on_select returned: {profile_settings}")
                
                # Update the session with the new provider and model
                cl.user_session.set("provider", provider)
                cl.user_session.set("model", model_id)
                print(f"Updated provider to {provider} and model to {model_id}")
                logger.info(f"Updated provider to {provider} and model to {model_id}")
        
        # Check if the message is a model command
        if message.content.startswith("/model"):
            try:
                # Parse the model command
                parts = message.content.split()
                if len(parts) < 2:
                    await cl.Message(
                        content="Please specify a model name. Example: /model gpt-4",
                        author="System"
                    ).send()
                    return
                
                model_name = parts[1]
                
                # Find the profile that matches the model name
                matching_profile = None
                for profile in profiles:
                    if model_name.lower() in profile.name.lower():
                        matching_profile = profile
                        break
                
                if not matching_profile:
                    await cl.Message(
                        content=f"No model found with name: {model_name}",
                        author="System"
                    ).send()
                    return
                
                # Update the session with the new profile
                cl.user_session.set("chat_profile", matching_profile.name)
                
                # Get the provider and model from the profile
                if hasattr(matching_profile, 'on_select') and callable(matching_profile.on_select):
                    profile_settings = matching_profile.on_select()
                    if profile_settings and isinstance(profile_settings, dict):
                        provider = profile_settings.get("provider", provider)
                        model_id = profile_settings.get("model_id", model_id)
                        
                        # Update the session with the new provider and model
                        cl.user_session.set("provider", provider)
                        cl.user_session.set("model", model_id)
                
                await cl.Message(
                    content=f"Switched to model: {matching_profile.name}",
                    author="System"
                ).send()
                return
            except Exception as e:
                logger.error(f"Error processing model command: {str(e)}")
                await cl.Message(
                    content=f"Error changing model: {str(e)}",
                    author="System"
                ).send()
                return
        
        # Double-check that we have valid provider and model_id
        if not provider or not model_id:
            logger.warning(f"Missing provider ({provider}) or model_id ({model_id}). Using defaults.")
            provider = config.DEFAULT_PROVIDER
            model_id = config.DEFAULT_MODEL
            
            # Update the session with the defaults
            cl.user_session.set("provider", provider)
            cl.user_session.set("model", model_id)
        
        # Prepare the request payload for n8n
        payload = {
            "chatInput": message.content,
            "sessionID": session_id,
            "provider": provider,
            "model": model_id,  # This is the model ID that n8n expects
            "temperature": 0.7,
            "max_tokens": 2048
        }
        
        # Log the payload for verification
        logger.info(f"Sending payload to n8n: {json.dumps(payload, indent=2)}")
        print(f"Current session settings - provider: {provider}, model: {model_id}")
        logger.info(f"Current session settings - provider: {provider}, model: {model_id}")
        
        # Create a simple "thinking" message instead of a task list
        thinking_msg = cl.Message(content="Thinking...", author="Assistant")
        await thinking_msg.send()
        
        # Measure response time
        start_time = time.time()
        
        # Make the API call to n8n
        try:
            # Make the request to n8n
            response = make_n8n_request(payload)
            
            # Calculate and log response time
            end_time = time.time()
            response_time = end_time - start_time
            logger.info(f"n8n response received in {response_time:.2f} seconds")
            
            # Remove the thinking message
            await thinking_msg.remove()
            
            # Process the response
            if response:
                # Check for agent actions in the response
                if isinstance(response, dict) and "actions" in response:
                    actions = response["actions"]
                    for action in actions:
                        action_type = action.get("type", "").lower()
                        action_status = action.get("status", "").lower()
                        action_message = action.get("message", "")
                        
                        # Show appropriate status update based on action type
                        if action_type == "web_search":
                            await web_search_status("Web Search", action_message)
                        elif action_type == "email":
                            await email_status("Email Action", action_message)
                        elif action_type == "calendar":
                            await calendar_status("Calendar Action", action_message)
                        elif action_type == "file_system":
                            await file_system_status("File System Action", action_message)
                        elif action_type == "database":
                            await database_status("Database Action", action_message)
                        elif action_type == "api":
                            await api_status("API Action", action_message)
                        
                        # Show appropriate status update based on action status
                        if action_status == "success":
                            await success_status(f"{action_type.title()} Success", action_message)
                        elif action_status == "warning":
                            await warning_status(f"{action_type.title()} Warning", action_message)
                        elif action_status == "error":
                            await error_status(f"{action_type.title()} Error", action_message)
                        elif action_status == "info":
                            await info_status(f"{action_type.title()} Info", action_message)
                
                # Process the main response
                if isinstance(response, list) and len(response) > 0:
                    for item in response:
                        if isinstance(item, dict):
                            # Extract the output text
                            output = item.get("output", "")
                            
                            # Extract any elements (images, files, etc.)
                            elements = item.get("elements", [])
                            
                            # Create a message with the output and elements
                            if output or elements:
                                await cl.Message(
                                    content=output,
                                    elements=elements,
                                    author="Assistant"
                                ).send()
                            
                            # Extract and process any metadata
                            metadata = item.get("metadata", {})
                            if metadata:
                                # Process any specific metadata fields here
                                pass
                        else:
                            # If the item is not a dict, just send it as a string
                            await cl.Message(content=str(item), author="Assistant").send()
                elif isinstance(response, dict):
                    # Extract the output text
                    output = response.get("output", "")
                    
                    # Extract any elements (images, files, etc.)
                    elements = response.get("elements", [])
                    
                    # Create a message with the output and elements
                    if output or elements:
                        await cl.Message(
                            content=output,
                            elements=elements,
                            author="Assistant"
                        ).send()
                else:
                    # If the response is not a list or dict, just send it as a string
                    await cl.Message(content=str(response), author="Assistant").send()
            else:
                # Handle empty response
                await cl.Message(
                    content="I'm sorry, I didn't receive a response from the backend. Please try again.",
                    author="System"
                ).send()
        except Exception as e:
            logger.error(f"Error making n8n request: {str(e)}", exc_info=True)
            
            # Remove the thinking message
            await thinking_msg.remove()
            
            # Send an error message
            await cl.Message(
                content=f"I'm sorry, there was an error processing your request: {str(e)}",
                author="System",
                type="error"
            ).send()
    except Exception as e:
        logger.error(f"Error in on_message: {str(e)}", exc_info=True)
        
        # Send an error message
        await cl.Message(
            content=f"I'm sorry, there was an error processing your message: {str(e)}",
            author="System",
            type="error"
        ).send()

def make_n8n_request(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Make a request to the n8n webhook.
    
    Args:
        payload: The payload to send to n8n
        
    Returns:
        The parsed response from n8n
    """
    try:
        # Log the original payload for debugging
        print(f"Original payload to n8n: {json.dumps(payload, indent=2)}")
        logger.info(f"Original payload to n8n: {json.dumps(payload, indent=2)}")
        
        # Ensure the provider and model are correctly set
        if not payload.get("provider"):
            print("Provider missing in payload. Using default provider.")
            logger.warning("Provider missing in payload. Using default provider.")
            payload["provider"] = config.DEFAULT_PROVIDER
        
        if not payload.get("model"):
            print("Model missing in payload. Using default model.")
            logger.warning("Model missing in payload. Using default model.")
            payload["model"] = config.DEFAULT_MODEL
        
        # Get the current provider and model from the payload
        provider = payload.get("provider")
        model = payload.get("model")
        
        # Log the provider and model for debugging
        print(f"Final payload provider: {provider}, model: {model}")
        logger.info(f"Final payload provider: {provider}, model: {model}")
        print(f"Full payload being sent to n8n: {json.dumps(payload, indent=2)}")
        logger.info(f"Full payload being sent to n8n: {json.dumps(payload, indent=2)}")
        
        # Make the POST request to the n8n webhook
        response = requests.post(
            config.N8N_WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=config.REQUEST_TIMEOUT
        )
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Parse the response
        try:
            response_data = response.json()
            logger.info(f"Received response from n8n: {json.dumps(response_data, indent=2)}")
            return response_data
        except json.JSONDecodeError:
            logger.error(f"Failed to parse response as JSON: {response.text}")
            raise ValueError(f"Invalid JSON response from n8n: {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to n8n failed: {str(e)}")
        raise RuntimeError(f"Failed to communicate with n8n: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in make_n8n_request: {str(e)}")
        raise RuntimeError(f"Unexpected error: {str(e)}")

@cl.on_chat_end
async def on_chat_end():
    """
    Clean up when the chat session ends.
    
    This function is called when a chat session ends.
    It cleans up any resources used by the chat session.
    """
    # Stop the background task
    cl.user_session.set("process_status_updates", False)
    logger.info("Stopped background task for processing status updates")

@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.User]:
    """Authenticate a user with username and password."""
    if username == "admin" and password == "admin":
        return cl.User(identifier="admin", metadata={"role": "admin"})
    return None

if __name__ == "__main__":
    # This block will be executed when running the script directly
    pass 