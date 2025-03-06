"""
Task List Example

This file demonstrates how to use task lists correctly in a Chainlit application,
following the official documentation at https://docs.chainlit.io/api-reference/elements/tasklist
"""

import chainlit as cl
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
    
    # Create the TaskList
    task_list = cl.TaskList(title="Processing Tasks")
    
    # Create tasks with correct TaskStatus values
    task1 = cl.Task(title="Task 1: Data Loading", status=cl.TaskStatus.RUNNING)
    task2 = cl.Task(title="Task 2: Processing", status=cl.TaskStatus.READY)
    task3 = cl.Task(title="Task 3: Analysis", status=cl.TaskStatus.READY)
    
    # Add tasks to the list
    await task_list.add_task(task1)
    await task_list.add_task(task2)
    await task_list.add_task(task3)
    
    # Optional: link a message to each task to allow task navigation in the chat history
    message1 = await cl.Message(content="Started loading data").send()
    task1.forId = message1.id
    
    # Send the task list to display it
    await task_list.send()
    
    # Simulate task progress
    await cl.Message(content="Simulating task progress...").send()
    
    # Update Task 1 to complete
    await asyncio.sleep(2)
    task1.status = cl.TaskStatus.DONE
    await task_list.send()
    
    # Start Task 2
    message2 = await cl.Message(content="Processing data...").send()
    task2.forId = message2.id
    task2.status = cl.TaskStatus.RUNNING
    await task_list.send()
    
    # Complete Task 2
    await asyncio.sleep(2)
    task2.status = cl.TaskStatus.DONE
    await task_list.send()
    
    # Start and complete Task 3
    message3 = await cl.Message(content="Analyzing results...").send()
    task3.forId = message3.id
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
    Handle user messages by demonstrating a new task list.
    """
    # Create a new task list for this user message
    task_list = cl.TaskList(title="Processing Your Request")
    
    # Create tasks
    task1 = cl.Task(title="Understanding request", status=cl.TaskStatus.RUNNING)
    task2 = cl.Task(title="Retrieving information", status=cl.TaskStatus.READY)
    task3 = cl.Task(title="Generating response", status=cl.TaskStatus.READY)
    
    # Add tasks to the list
    await task_list.add_task(task1)
    await task_list.add_task(task2)
    await task_list.add_task(task3)
    
    # Link messages to tasks
    msg1 = await cl.Message(content=f"Processing your request: '{message.content}'").send()
    task1.forId = msg1.id
    
    # Send the task list to display it
    await task_list.send()
    
    # Simulate processing
    await asyncio.sleep(1.5)
    task1.status = cl.TaskStatus.DONE
    await task_list.send()
    
    msg2 = await cl.Message(content="Retrieving relevant information...").send()
    task2.forId = msg2.id
    task2.status = cl.TaskStatus.RUNNING
    await task_list.send()
    
    await asyncio.sleep(2)
    task2.status = cl.TaskStatus.DONE
    await task_list.send()
    
    msg3 = await cl.Message(content="Generating response...").send()
    task3.forId = msg3.id
    task3.status = cl.TaskStatus.RUNNING
    await task_list.send()
    
    await asyncio.sleep(2)
    task3.status = cl.TaskStatus.DONE
    await task_list.send()
    
    # Send the response
    await cl.Message(
        content=f"I've processed your request: '{message.content}'\n\nThis is a demo of how task lists should display on the right side of the chat interface."
    ).send() 