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
        message: The alert message
        icon: Lucide icon name (default: "alert-circle")
        
    Returns:
        The sent message object
    """
    element = cl.CustomElement(
        name="AlertNotification",
        props={
            "type": "important",
            "title": title,
            "message": message
        }
    )
    msg = cl.Message(content="", elements=[element])
    return await msg.send()

async def notification_alert(title: str, message: str, icon: str = "bell") -> cl.Message:
    """
    Display a notification alert.
    
    Args:
        title: The title of the alert
        message: The alert message
        icon: Lucide icon name (default: "bell")
        
    Returns:
        The sent message object
    """
    element = cl.CustomElement(
        name="AlertNotification",
        props={
            "type": "notification",
            "title": title,
            "message": message
        }
    )
    msg = cl.Message(content="", elements=[element])
    return await msg.send()

async def system_alert(title: str, message: str, icon: str = "info") -> cl.Message:
    """
    Display a system alert notification.
    
    Args:
        title: The title of the alert
        message: The alert message
        icon: Lucide icon name (default: "info")
        
    Returns:
        The sent message object
    """
    element = cl.CustomElement(
        name="AlertNotification",
        props={
            "type": "system",
            "title": title,
            "message": message
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
    A styled task list for displaying multiple tasks with status indicators.
    """
    
    def __init__(self, title: str = "Processing Tasks", **kwargs):
        """
        Initialize a new styled task list.
        
        Args:
            title: The title of the task list
            **kwargs: Additional keyword arguments to pass to the TaskList constructor
        """
        self.title = title
        self.tasks = {}
        self.task_list = cl.TaskList(title=self.title)
    
    async def create(self) -> None:
        """Create and display the task list."""
        await self.task_list.send()
    
    async def add_task(self, name: str, status: str = "running", icon: Optional[str] = None) -> cl.Task:
        """
        Add a task to the list.
        
        Args:
            name: The name of the task
            status: The status of the task (running, done, error)
            icon: Optional icon name
            
        Returns:
            The created task object
        """
        # Convert string status to TaskStatus enum
        task_status = self._get_task_status(status)
        
        # Create and add the task
        task = cl.Task(title=name, status=task_status, icon=icon)
        await self.task_list.add_task(task)
        
        # Store the task for later reference
        self.tasks[name] = task
        
        return task
    
    async def update_task(self, name: str, status: str, icon: Optional[str] = None) -> None:
        """
        Update the status of a task.
        
        Args:
            name: The name of the task
            status: The new status (running, done, error)
            icon: Optional new icon name
        """
        if name in self.tasks:
            task = self.tasks[name]
            task.status = self._get_task_status(status)
            if icon:
                task.icon = icon
            await self.task_list.update()
    
    def _get_task_status(self, status: str) -> cl.TaskStatus:
        """Convert string status to TaskStatus enum."""
        status = status.lower()
        if status == "done":
            return cl.TaskStatus.DONE
        elif status == "error":
            return cl.TaskStatus.FAILED
        else:
            return cl.TaskStatus.RUNNING

# ===== TOAST NOTIFICATIONS =====

async def show_toast(message: str, type: str = "info", duration: int = 3000) -> None:
    """
    Show a toast notification.
    
    Args:
        message: The notification message
        type: The type of notification (info, success, warning, error)
        duration: Duration in milliseconds
    """
    try:
        # In Chainlit 2.2.1, toast notifications can be sent using the notify method
        # or by creating a message with a specific type
        
        # Method 1: Using cl.notify
        await cl.notify(
            message=message,
            type=type,
            duration=duration
        )
        
        # Method 2: As a fallback, also try sending as a regular message with toast class
        # This creates a custom element that mimics a toast notification
        element = cl.CustomElement(
            name="Toast",
            props={
                "message": message,
                "type": type,
                "duration": duration
            }
        )
        
        # Create a message with the toast element
        msg = cl.Message(content="", elements=[element])
        await msg.send()
        
        logging.info(f"Toast notification sent: {message}")
    except Exception as e:
        logging.error(f"Error sending toast notification: {str(e)}")
        
        # Fallback method if the above methods fail
        try:
            # Create a simple message with the toast content
            msg = cl.Message(content=f"**{type.upper()}**: {message}")
            await msg.send()
            logging.info(f"Sent fallback toast message: {message}")
        except Exception as e2:
            logging.error(f"Error sending fallback toast message: {str(e2)}") 