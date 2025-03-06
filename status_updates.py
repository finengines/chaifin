"""
Status Updates Module for Chainlit UI

This module provides helper functions for creating visually distinct status updates,
progress indicators, and alerts in the Chainlit UI.
"""

import chainlit as cl
from typing import Optional, Dict, Any, List, Union
import asyncio
import logging

# ===== AGENT ACTION STATUS UPDATES =====

async def email_status(title: str, message: str, icon: str = "mail") -> cl.Message:
    """
    Display an email agent status update.
    
    Args:
        title: The title of the status update
        message: The message content
        icon: Lucide icon name (default: "mail")
        
    Returns:
        The sent message object
    """
    element = cl.CustomElement(
        name="StatusUpdate",
        props={
            "type": "email",
            "icon": icon,
            "title": title,
            "message": message
        }
    )
    msg = cl.Message(content="", elements=[element])
    return await msg.send()

async def calendar_status(title: str, message: str, icon: str = "calendar") -> cl.Message:
    """
    Display a calendar agent status update.
    
    Args:
        title: The title of the status update
        message: The message content
        icon: Lucide icon name (default: "calendar")
        
    Returns:
        The sent message object
    """
    element = cl.CustomElement(
        name="StatusUpdate",
        props={
            "type": "calendar",
            "icon": icon,
            "title": title,
            "message": message
        }
    )
    msg = cl.Message(content="", elements=[element])
    return await msg.send()

async def web_search_status(title: str, message: str, icon: str = "search") -> cl.Message:
    """
    Display a web search agent status update.
    
    Args:
        title: The title of the status update
        message: The message content
        icon: Lucide icon name (default: "search")
        
    Returns:
        The sent message object
    """
    element = cl.CustomElement(
        name="StatusUpdate",
        props={
            "type": "web-search",
            "icon": icon,
            "title": title,
            "message": message
        }
    )
    msg = cl.Message(content="", elements=[element])
    return await msg.send()

async def file_system_status(title: str, message: str, icon: str = "folder") -> cl.Message:
    """
    Display a file system agent status update.
    
    Args:
        title: The title of the status update
        message: The message content
        icon: Lucide icon name (default: "folder")
        
    Returns:
        The sent message object
    """
    element = cl.CustomElement(
        name="StatusUpdate",
        props={
            "type": "file-system",
            "icon": icon,
            "title": title,
            "message": message
        }
    )
    msg = cl.Message(content="", elements=[element])
    return await msg.send()

async def database_status(title: str, message: str, icon: str = "database") -> cl.Message:
    """
    Display a database agent status update.
    
    Args:
        title: The title of the status update
        message: The message content
        icon: Lucide icon name (default: "database")
        
    Returns:
        The sent message object
    """
    element = cl.CustomElement(
        name="StatusUpdate",
        props={
            "type": "database",
            "icon": icon,
            "title": title,
            "message": message
        }
    )
    msg = cl.Message(content="", elements=[element])
    return await msg.send()

async def api_status(title: str, message: str, icon: str = "code") -> cl.Message:
    """
    Display an API agent status update.
    
    Args:
        title: The title of the status update
        message: The message content
        icon: Lucide icon name (default: "code")
        
    Returns:
        The sent message object
    """
    element = cl.CustomElement(
        name="StatusUpdate",
        props={
            "type": "api",
            "icon": icon,
            "title": title,
            "message": message
        }
    )
    msg = cl.Message(content="", elements=[element])
    return await msg.send()

# ===== PROGRESS STATUS UPDATES =====

async def progress_status(title: str, message: str, progress: Optional[int] = None, icon: str = "loader") -> cl.Message:
    """
    Display a progress status update.
    
    Args:
        title: The title of the status update
        message: The message content
        progress: Optional progress percentage (0-100)
        icon: Lucide icon name (default: "loader")
        
    Returns:
        The sent message object
    """
    element = cl.CustomElement(
        name="StatusUpdate",
        props={
            "type": "progress",
            "icon": icon,
            "title": title,
            "message": message,
            "progress": progress
        }
    )
    msg = cl.Message(content="", elements=[element])
    return await msg.send()

async def success_status(title: str, message: str, icon: str = "check-circle") -> cl.Message:
    """
    Display a success status update.
    
    Args:
        title: The title of the status update
        message: The message content
        icon: Lucide icon name (default: "check-circle")
        
    Returns:
        The sent message object
    """
    element = cl.CustomElement(
        name="StatusUpdate",
        props={
            "type": "success",
            "icon": icon,
            "title": title,
            "message": message
        }
    )
    msg = cl.Message(content="", elements=[element])
    return await msg.send()

async def warning_status(title: str, message: str, icon: str = "alert-triangle") -> cl.Message:
    """
    Display a warning status update.
    
    Args:
        title: The title of the status update
        message: The message content
        icon: Lucide icon name (default: "alert-triangle")
        
    Returns:
        The sent message object
    """
    element = cl.CustomElement(
        name="StatusUpdate",
        props={
            "type": "warning",
            "icon": icon,
            "title": title,
            "message": message
        }
    )
    msg = cl.Message(content="", elements=[element])
    return await msg.send()

async def error_status(title: str, message: str, icon: str = "alert-circle") -> cl.Message:
    """
    Display an error status update.
    
    Args:
        title: The title of the status update
        message: The message content
        icon: Lucide icon name (default: "alert-circle")
        
    Returns:
        The sent message object
    """
    element = cl.CustomElement(
        name="StatusUpdate",
        props={
            "type": "error",
            "icon": icon,
            "title": title,
            "message": message
        }
    )
    msg = cl.Message(content="", elements=[element])
    return await msg.send()

async def info_status(title: str, message: str, icon: str = "info") -> cl.Message:
    """
    Display an info status update.
    
    Args:
        title: The title of the status update
        message: The message content
        icon: Lucide icon name (default: "info")
        
    Returns:
        The sent message object
    """
    element = cl.CustomElement(
        name="StatusUpdate",
        props={
            "type": "info",
            "icon": icon,
            "title": title,
            "message": message
        }
    )
    msg = cl.Message(content="", elements=[element])
    return await msg.send()

# ===== ALERT STATUS UPDATES =====

async def important_alert(title: str, message: str, icon: str = "alert-circle") -> cl.Message:
    """
    Display an important alert notification.
    
    Args:
        title: The title of the alert
        message: The message content
        icon: Lucide icon name (default: "alert-circle")
        
    Returns:
        The sent message object
    """
    element = cl.CustomElement(
        name="AlertNotification",
        props={
            "type": "important",
            "title": title,
            "content": message,
            "icon": icon
        }
    )
    msg = cl.Message(content="", elements=[element])
    return await msg.send()

async def notification_alert(title: str, message: str, icon: str = "bell") -> cl.Message:
    """
    Display a notification alert.
    
    Args:
        title: The title of the alert
        message: The message content
        icon: Lucide icon name (default: "bell")
        
    Returns:
        The sent message object
    """
    element = cl.CustomElement(
        name="AlertNotification",
        props={
            "type": "notification",
            "title": title,
            "content": message,
            "icon": icon
        }
    )
    msg = cl.Message(content="", elements=[element])
    return await msg.send()

async def system_alert(title: str, message: str, icon: str = "info") -> cl.Message:
    """
    Display a system alert notification.
    
    Args:
        title: The title of the alert
        message: The message content
        icon: Lucide icon name (default: "info")
        
    Returns:
        The sent message object
    """
    element = cl.CustomElement(
        name="AlertNotification",
        props={
            "type": "system",
            "title": title,
            "content": message,
            "icon": icon
        }
    )
    msg = cl.Message(content="", elements=[element])
    return await msg.send()

# ===== ANIMATED PROGRESS =====

async def animated_progress(title: str, message: str, steps: List[str], delay: float = 0.5) -> None:
    """
    Display an animated progress indicator that cycles through steps.
    
    Args:
        title: The title of the progress indicator
        message: The initial message
        steps: List of step messages to cycle through
        delay: Delay between steps in seconds (default: 0.5)
    """
    if not steps:
        return
    
    # Create the initial progress element
    element = cl.CustomElement(
        name="AnimatedProgress",
        props={
            "title": title,
            "message": message,
            "steps": steps,
            "progress": 0
        }
    )
    msg = cl.Message(content="", elements=[element])
    await msg.send()
    
    # Animate through the steps
    total_steps = len(steps)
    for i in range(1, total_steps + 1):
        progress = int((i / total_steps) * 100)
        element.props["progress"] = progress
        await element.update()
        if i < total_steps:
            await asyncio.sleep(delay)
    
    # Complete the animation
    await success_status(f"{title} Complete", "All steps completed successfully")

# ===== TASK LIST =====

class StyledTaskList:
    """
    A styled task list for displaying progress of multiple tasks.
    The TaskList will be displayed on the right side of the chat interface.
    """
    
    def __init__(self, title: str = "Processing Tasks", **kwargs):
        """
        Initialize a new styled task list.
        
        Args:
            title: The title of the task list
            **kwargs: Additional arguments to pass to the task list
        """
        self.title = title
        self.task_list = None
        self.tasks = {}
        self.kwargs = kwargs
    
    async def create(self) -> None:
        """Create the task list."""
        # Ensure the task list is created with the correct display settings
        # TaskList is a special element that should always be displayed on the right side
        self.task_list = cl.TaskList(title=self.title, **self.kwargs)
        # Send the task list to display it
        await self.task_list.send()
    
    async def add_task(self, name: str, status: str = "running", icon: Optional[str] = None) -> cl.Task:
        """
        Add a task to the task list.
        
        Args:
            name: The name of the task
            status: The status of the task (running, done, failed, ready)
            icon: Lucide icon name (optional)
            
        Returns:
            The created task
        """
        if self.task_list is None:
            await self.create()
        
        # Set default icons based on status if not provided
        if icon is None:
            if status == "running":
                icon = "loader"
            elif status == "done":
                icon = "check-circle"
            elif status == "failed":
                icon = "x-circle"
            elif status == "ready":
                icon = "clock"
        
        task = cl.Task(title=name, status=self._get_task_status(status), icon=icon)
        self.tasks[name] = task
        await self.task_list.add_task(task)
        
        # Ensure the task list is sent to update the UI
        await self.task_list.send()
        
        return task
    
    async def update_task(self, name: str, status: str, icon: Optional[str] = None) -> None:
        """
        Update a task in the task list.
        
        Args:
            name: The name of the task
            status: The new status of the task
            icon: Lucide icon name (optional)
        """
        if name in self.tasks:
            task = self.tasks[name]
            task.status = self._get_task_status(status)
            if icon:
                task.icon = icon
            
            # In newer Chainlit versions, Task objects don't have an update() method
            # Instead, we need to send the entire task list again to update the UI
            await self.task_list.send()
        else:
            # If task doesn't exist, create it
            await self.add_task(name, status, icon)
    
    def _get_task_status(self, status: str) -> cl.TaskStatus:
        """Convert string status to TaskStatus enum."""
        if status == "running":
            return cl.TaskStatus.RUNNING
        elif status == "done":
            return cl.TaskStatus.DONE
        elif status == "failed":
            return cl.TaskStatus.FAILED
        elif status == "ready":
            return cl.TaskStatus.READY
        else:
            # Default to READY for any other status
            return cl.TaskStatus.READY

# ===== TOAST NOTIFICATIONS =====

async def show_toast(message: str, type: str = "info", duration: int = 3000) -> None:
    """
    Display a toast notification.
    
    Args:
        message: The message to display
        type: The type of toast (info, success, warning, error)
        duration: Duration in milliseconds
        
    Returns:
        None
    """
    try:
        # Validate toast type
        valid_types = ["info", "success", "warning", "error"]
        if type not in valid_types:
            type = "info"
            
        # In this version of Chainlit, send_toast only accepts message and type
        await cl.context.emitter.send_toast(
            message=message,
            type=type
        )
        logging.info(f"Toast notification sent: {message} ({type})")
    except Exception as e:
        logging.error(f"Failed to send toast notification: {str(e)}")
        # Log the full exception for debugging
        import traceback
        logging.error(traceback.format_exc()) 