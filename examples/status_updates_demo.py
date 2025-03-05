"""
Status Updates Demo for Chainlit UI

This demo showcases all the different types of status updates, progress indicators,
and alerts available in the status_updates module.
"""

import chainlit as cl
import asyncio
from status_updates import (
    # Agent action status updates
    email_status,
    calendar_status,
    web_search_status,
    file_system_status,
    database_status,
    api_status,
    
    # Progress status updates
    progress_status,
    success_status,
    warning_status,
    error_status,
    info_status,
    
    # Alert status updates
    important_alert,
    notification_alert,
    system_alert,
    
    # Animated progress
    animated_progress,
    
    # Task list
    StyledTaskList,
    
    # Toast notifications
    show_toast
)

@cl.on_chat_start
async def on_chat_start():
    # Welcome message
    await cl.Message(
        content="# Status Updates Demo\n\nThis demo showcases all the different types of status updates, progress indicators, and alerts available in the status_updates module.\n\nType one of the following commands to see the demo:\n\n- `agent`: Show agent action status updates\n- `progress`: Show progress status updates\n- `alerts`: Show alert status updates\n- `animated`: Show animated progress\n- `tasklist`: Show styled task list\n- `toast`: Show toast notifications\n- `all`: Show all demos"
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    command = message.content.lower().strip()
    
    if command == "agent":
        await show_agent_demos()
    elif command == "progress":
        await show_progress_demos()
    elif command == "alerts":
        await show_alert_demos()
    elif command == "animated":
        await show_animated_demo()
    elif command == "tasklist":
        await show_tasklist_demo()
    elif command == "toast":
        await show_toast_demo()
    elif command == "all":
        await cl.Message(content="Running all demos...").send()
        await show_agent_demos()
        await show_progress_demos()
        await show_alert_demos()
        await show_animated_demo()
        await show_tasklist_demo()
        await show_toast_demo()
    else:
        await cl.Message(content="Unknown command. Please try one of the following: `agent`, `progress`, `alerts`, `animated`, `tasklist`, `toast`, or `all`.").send()

async def show_agent_demos():
    """Show all agent action status updates."""
    await cl.Message(content="## Agent Action Status Updates").send()
    
    await email_status(
        "Email Processing", 
        "Sending email to john@example.com with subject 'Meeting Agenda'"
    )
    
    await calendar_status(
        "Calendar Update", 
        "Adding meeting with Marketing team on Friday at 2:00 PM"
    )
    
    await web_search_status(
        "Web Search", 
        "Searching for information about 'machine learning frameworks'"
    )
    
    await file_system_status(
        "File System Operation", 
        "Saving document to /documents/reports/q2_summary.pdf"
    )
    
    await database_status(
        "Database Query", 
        "Retrieving customer records from CRM database"
    )
    
    await api_status(
        "API Request", 
        "Calling weather API to get forecast for New York"
    )

async def show_progress_demos():
    """Show all progress status updates."""
    await cl.Message(content="## Progress Status Updates").send()
    
    await progress_status(
        "Data Processing", 
        "Processing large dataset...", 
        progress=25
    )
    
    await success_status(
        "Operation Complete", 
        "Successfully processed all files"
    )
    
    await warning_status(
        "Warning", 
        "Low disk space detected (15% remaining)"
    )
    
    await error_status(
        "Error", 
        "Failed to connect to database server"
    )
    
    await info_status(
        "Information", 
        "System maintenance scheduled for tomorrow at 2:00 AM"
    )

async def show_alert_demos():
    """Show all alert status updates."""
    await cl.Message(content="## Alert Status Updates").send()
    
    await important_alert(
        "Critical Alert", 
        "System resources are running low. Please close unnecessary applications."
    )
    
    await notification_alert(
        "New Message", 
        "You have 3 new messages in your inbox"
    )
    
    await system_alert(
        "System Update", 
        "A new version of the software is available (v2.1.4)"
    )

async def show_animated_demo():
    """Show animated progress demo."""
    await cl.Message(content="## Animated Progress Demo").send()
    
    steps = [
        "Initializing data processing...",
        "Loading dataset from source...",
        "Preprocessing data...",
        "Applying transformations...",
        "Validating results...",
        "Saving processed data..."
    ]
    
    await animated_progress("Data Processing", "Starting data processing...", steps, delay=1.0)

async def show_tasklist_demo():
    """Show styled task list demo."""
    await cl.Message(content="## Styled Task List Demo").send()
    
    # Create a task list
    task_list = StyledTaskList("Processing User Request")
    
    # Add initial tasks
    await task_list.add_task("Analyzing request", "running")
    await task_list.add_task("Retrieving data", "running")
    await task_list.add_task("Processing results", "running")
    await task_list.add_task("Generating response", "running")
    
    # Update tasks with delays to simulate progress
    await asyncio.sleep(1)
    await task_list.update_task("Analyzing request", "done")
    
    await asyncio.sleep(1)
    await task_list.update_task("Retrieving data", "done")
    
    await asyncio.sleep(1)
    await task_list.update_task("Processing results", "done")
    
    await asyncio.sleep(1)
    await task_list.update_task("Generating response", "done")
    
    await success_status("Task List Demo", "All tasks completed successfully")

async def show_toast_demo():
    """Show toast notification demo."""
    await cl.Message(content="## Toast Notification Demo").send()
    
    await show_toast("This is an info toast notification", "info")
    await asyncio.sleep(1)
    
    await show_toast("This is a success toast notification", "success")
    await asyncio.sleep(1)
    
    await show_toast("This is a warning toast notification", "warning")
    await asyncio.sleep(1)
    
    await show_toast("This is an error toast notification", "error")
    
    await cl.Message(content="Toast notifications displayed").send()

if __name__ == "__main__":
    # This file can be run directly with: chainlit run status_updates_demo.py
    pass 