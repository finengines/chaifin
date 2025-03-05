"""
Direct Task List Test

This script tests the task list functionality directly using the Chainlit API.
"""

import asyncio
import chainlit as cl
from status_updates import StyledTaskList
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("direct-task-list-test")

async def test_direct_task_list():
    """Test creating a task list directly using the Chainlit API"""
    logger.info("Testing direct task list creation...")
    
    # Create a task list
    task_list = cl.TaskList(title="Direct Test Tasks")
    await task_list.send()
    
    # Add tasks
    task1 = cl.Task(title="Task 1", status=cl.TaskStatus.RUNNING)
    await task_list.add_task(task1)
    
    task2 = cl.Task(title="Task 2", status=cl.TaskStatus.RUNNING)
    await task_list.add_task(task2)
    
    task3 = cl.Task(title="Task 3", status=cl.TaskStatus.RUNNING)
    await task_list.add_task(task3)
    
    # Update tasks
    task1.status = cl.TaskStatus.DONE
    await task_list.update()
    
    task2.status = cl.TaskStatus.DONE
    await task_list.update()
    
    task3.status = cl.TaskStatus.DONE
    await task_list.update()
    
    logger.info("Direct task list test completed")

async def test_styled_task_list():
    """Test creating a styled task list"""
    logger.info("Testing styled task list creation...")
    
    # Create a styled task list
    task_list = StyledTaskList(title="Styled Test Tasks")
    await task_list.create()
    
    # Add tasks
    await task_list.add_task("Styled Task 1", "running")
    await task_list.add_task("Styled Task 2", "running")
    await task_list.add_task("Styled Task 3", "running")
    
    # Update tasks
    await task_list.update_task("Styled Task 1", "done")
    await task_list.update_task("Styled Task 2", "done")
    await task_list.update_task("Styled Task 3", "done")
    
    logger.info("Styled task list test completed")

@cl.on_message
async def on_message(message: cl.Message):
    """Handle user messages"""
    if message.content.lower() == "test direct task list":
        await test_direct_task_list()
    elif message.content.lower() == "test styled task list":
        await test_styled_task_list()
    else:
        await cl.Message(content="Send 'test direct task list' or 'test styled task list' to run the tests").send() 