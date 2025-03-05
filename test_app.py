"""
Test App for Task List Functionality

This is a simple Chainlit app to test the task list functionality.
"""

import chainlit as cl
import time
import asyncio

@cl.on_chat_start
async def on_chat_start():
    """Initialize the chat session"""
    await cl.Message(content="Welcome to the Task List Test App! Type 'test task list' to test the task list functionality.").send()

@cl.on_message
async def on_message(message: cl.Message):
    """Handle user messages"""
    if message.content.lower() == "test task list":
        await test_task_list()
    else:
        await cl.Message(content="Type 'test task list' to test the task list functionality.").send()

async def test_task_list():
    """Test the task list functionality"""
    # Create a task list
    task_list = cl.TaskList(title="Test Tasks")
    await task_list.send()
    
    # Add tasks
    task1 = cl.Task(title="Loading Data", status=cl.TaskStatus.RUNNING)
    await task_list.add_task(task1)
    await asyncio.sleep(1)
    
    task2 = cl.Task(title="Processing Information", status=cl.TaskStatus.RUNNING)
    await task_list.add_task(task2)
    await asyncio.sleep(1)
    
    task3 = cl.Task(title="Generating Results", status=cl.TaskStatus.RUNNING)
    await task_list.add_task(task3)
    await asyncio.sleep(1)
    
    # Update tasks
    task1.status = cl.TaskStatus.DONE
    await task_list.update()
    await asyncio.sleep(1)
    
    task2.status = cl.TaskStatus.DONE
    await task_list.update()
    await asyncio.sleep(1)
    
    task3.status = cl.TaskStatus.DONE
    await task_list.update()
    
    # Send a completion message
    await cl.Message(content="Task list test completed successfully!").send() 