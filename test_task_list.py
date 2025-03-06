"""
Test file to verify that task lists are displaying correctly on the right side of the chat interface.
"""

import chainlit as cl
from status_updates import StyledTaskList
import asyncio

@cl.on_chat_start
async def on_chat_start():
    """
    Initialize the chat and demonstrate task list functionality.
    """
    # Welcome message
    await cl.Message(
        content="# Task List Demo\nThis demo shows how task lists should display on the right side of the chat interface."
    ).send()
    
    # Create a standard Chainlit task list
    await cl.Message(content="Creating a standard Chainlit task list...").send()
    
    # Create the TaskList
    task_list = cl.TaskList(title="Standard Task List")
    
    # Create tasks with correct TaskStatus values
    # Note: In Chainlit 2.2.0+, the valid TaskStatus values are READY, RUNNING, DONE, and FAILED
    task1 = cl.Task(title="Task 1: Data Loading", status=cl.TaskStatus.RUNNING)
    task2 = cl.Task(title="Task 2: Processing", status=cl.TaskStatus.READY)
    task3 = cl.Task(title="Task 3: Analysis", status=cl.TaskStatus.READY)
    
    # Add tasks to the list
    await task_list.add_task(task1)
    await task_list.add_task(task2)
    await task_list.add_task(task3)
    
    # Send the task list to display it
    await task_list.send()
    
    # Simulate task progress
    await cl.Message(content="Simulating task progress...").send()
    
    # Update Task 1 to complete
    await asyncio.sleep(2)
    task1.status = cl.TaskStatus.DONE
    await task_list.send()
    
    # Start Task 2
    await asyncio.sleep(1)
    task2.status = cl.TaskStatus.RUNNING
    await task_list.send()
    
    # Complete Task 2
    await asyncio.sleep(2)
    task2.status = cl.TaskStatus.DONE
    await task_list.send()
    
    # Start and complete Task 3
    await asyncio.sleep(1)
    task3.status = cl.TaskStatus.RUNNING
    await task_list.send()
    
    await asyncio.sleep(2)
    task3.status = cl.TaskStatus.DONE
    await task_list.send()
    
    # Now test the StyledTaskList
    await cl.Message(content="Now testing the StyledTaskList implementation...").send()
    
    # Create a styled task list
    styled_task_list = StyledTaskList(title="Styled Task List")
    await styled_task_list.create()
    
    # Add tasks
    await styled_task_list.add_task("Styled Task 1: Initialize", "running")
    await asyncio.sleep(1)
    await styled_task_list.add_task("Styled Task 2: Process Data", "ready")
    await asyncio.sleep(1)
    await styled_task_list.add_task("Styled Task 3: Generate Results", "ready")
    
    # Update tasks
    await asyncio.sleep(2)
    await styled_task_list.update_task("Styled Task 1: Initialize", "done")
    
    await asyncio.sleep(1)
    await styled_task_list.update_task("Styled Task 2: Process Data", "running")
    
    await asyncio.sleep(2)
    await styled_task_list.update_task("Styled Task 2: Process Data", "done")
    
    await asyncio.sleep(1)
    await styled_task_list.update_task("Styled Task 3: Generate Results", "running")
    
    await asyncio.sleep(2)
    await styled_task_list.update_task("Styled Task 3: Generate Results", "done")
    
    # Final message
    await cl.Message(
        content="# Task List Demo Complete\nBoth standard and styled task lists should have displayed correctly on the right side of the chat interface."
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    """
    Handle user messages.
    """
    await cl.Message(
        content=f"You said: {message.content}\n\nThis is a test app to demonstrate task lists. Please restart the app to see the task list demo again."
    ).send() 