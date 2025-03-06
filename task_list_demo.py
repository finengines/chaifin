"""
Task List Demo

This file demonstrates how to use task lists correctly in a Chainlit application.
Task lists should display on the right side of the chat interface.
"""

import chainlit as cl
from status_updates import StyledTaskList
import asyncio
import time

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
    
    # Final message
    await cl.Message(
        content="# Task List Demo Complete\nThe task list should have displayed correctly on the right side of the chat interface."
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    """
    Handle user messages by demonstrating the StyledTaskList.
    """
    # Create a styled task list
    styled_task_list = StyledTaskList(title="Processing Your Request")
    await styled_task_list.create()
    
    # Add initial tasks
    await styled_task_list.add_task("Understanding request", "running")
    await styled_task_list.add_task("Retrieving information", "ready")
    await styled_task_list.add_task("Generating response", "ready")
    
    # Simulate processing
    await cl.Message(content=f"Processing your request: '{message.content}'").send()
    
    # Update task statuses
    await asyncio.sleep(1.5)
    await styled_task_list.update_task("Understanding request", "done")
    
    await asyncio.sleep(1)
    await styled_task_list.update_task("Retrieving information", "running")
    
    await asyncio.sleep(2)
    await styled_task_list.update_task("Retrieving information", "done")
    
    await asyncio.sleep(1)
    await styled_task_list.update_task("Generating response", "running")
    
    await asyncio.sleep(2)
    await styled_task_list.update_task("Generating response", "done")
    
    # Send the response
    await cl.Message(
        content=f"I've processed your request: '{message.content}'\n\nThis is a demo of how task lists should display on the right side of the chat interface."
    ).send() 