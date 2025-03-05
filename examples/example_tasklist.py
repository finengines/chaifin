import chainlit as cl
import time
import asyncio
from typing import List, Dict, Any

# Simulated data processing function
async def process_data(data: List[Dict[str, Any]], progress_callback=None):
    total_items = len(data)
    processed = 0
    
    results = []
    for item in data:
        # Simulate processing time
        await asyncio.sleep(0.5)
        
        # Process the item (in a real app, this would do actual work)
        result = {
            "id": item["id"],
            "name": item["name"],
            "processed": True,
            "score": len(item["name"]) * 5  # Just a dummy calculation
        }
        results.append(result)
        
        # Update progress
        processed += 1
        if progress_callback:
            progress_callback(processed / total_items * 100)
    
    return results

# Example data
sample_data = [
    {"id": 1, "name": "Document 1", "content": "Sample content 1"},
    {"id": 2, "name": "Document 2", "content": "Sample content 2"},
    {"id": 3, "name": "Document 3", "content": "Sample content 3"},
    {"id": 4, "name": "Document 4", "content": "Sample content 4"},
    {"id": 5, "name": "Document 5", "content": "Sample content 5"},
]

@cl.on_chat_start
async def start():
    # Send a welcome message
    await cl.Message(
        content="Welcome! I can demonstrate progress tracking with TaskList. Type 'start' to begin processing."
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    if message.content.lower() == "start":
        # Create a TaskList to track progress
        task_list = cl.TaskList(status="Initializing...")
        await task_list.send()
        
        # Add tasks for each processing step
        data_loading_task = cl.Task(title="Loading data", status=cl.TaskStatus.RUNNING)
        await task_list.add_task(data_loading_task)
        
        processing_task = cl.Task(title="Processing documents")
        await task_list.add_task(processing_task)
        
        analysis_task = cl.Task(title="Analyzing results")
        await task_list.add_task(analysis_task)
        
        summary_task = cl.Task(title="Generating summary")
        await task_list.add_task(summary_task)
        
        # Step 1: Loading data
        await cl.Message(content="Step 1: Loading data...").send()
        await asyncio.sleep(1)  # Simulate loading time
        data_loading_task.status = cl.TaskStatus.DONE
        task_list.status = "Loading complete"
        await task_list.send()
        
        # Step 2: Processing documents
        processing_task.status = cl.TaskStatus.RUNNING
        task_list.status = "Processing documents..."
        await task_list.send()
        
        # Create a message to show progress
        progress_msg = cl.Message(content="Processing: 0%")
        await progress_msg.send()
        
        # Process the data with progress updates
        async def update_progress(percentage):
            await progress_msg.update(content=f"Processing: {percentage:.0f}%")
            
        results = await process_data(sample_data, update_progress)
        
        processing_task.status = cl.TaskStatus.DONE
        task_list.status = "Processing complete"
        await task_list.send()
        
        # Step 3: Analyzing results
        analysis_task.status = cl.TaskStatus.RUNNING
        task_list.status = "Analyzing results..."
        await task_list.send()
        
        await cl.Message(content="Step 3: Analyzing results...").send()
        await asyncio.sleep(1.5)  # Simulate analysis time
        
        # Calculate some statistics (in a real app, this would be more meaningful)
        avg_score = sum(item["score"] for item in results) / len(results)
        
        analysis_task.status = cl.TaskStatus.DONE
        task_list.status = "Analysis complete"
        await task_list.send()
        
        # Step 4: Generate summary
        summary_task.status = cl.TaskStatus.RUNNING
        task_list.status = "Generating summary..."
        await task_list.send()
        
        await cl.Message(content="Step 4: Generating summary...").send()
        await asyncio.sleep(1)  # Simulate summary generation
        
        # Create a summary message
        summary = f"""
## Processing Summary

- **Documents Processed**: {len(results)}
- **Average Score**: {avg_score:.1f}
- **Processing Time**: {len(results) * 0.5:.1f} seconds

### Results:

| ID | Document | Score |
|----|----------|-------|
"""
        
        for item in results:
            summary += f"| {item['id']} | {item['name']} | {item['score']} |\n"
        
        summary_task.status = cl.TaskStatus.DONE
        task_list.status = "Complete"
        await task_list.send()
        
        # Send the final summary
        await cl.Message(content=summary).send()
        
        # Add action buttons for next steps
        actions = [
            cl.Action(name="restart", label="Process Again", icon="refresh-cw"),
            cl.Action(name="export", label="Export Results", icon="download")
        ]
        
        await cl.Message(
            content="Processing complete! What would you like to do next?",
            actions=actions
        ).send()
    
    elif message.content.lower() == "help":
        await cl.Message(
            content="""
## Available Commands

- **start**: Begin the data processing demonstration with TaskList progress tracking
- **help**: Show this help message
"""
        ).send()
    
    else:
        await cl.Message(
            content="I'm a TaskList demonstration bot. Type 'start' to see progress tracking in action, or 'help' for available commands."
        ).send()

@cl.action_callback("restart")
async def on_restart(action):
    await cl.Message(content="Restarting the process. Type 'start' to begin again.").send()

@cl.action_callback("export")
async def on_export(action):
    # In a real app, this would generate and provide a download link
    await cl.Message(content="Results would be exported here in a real application.").send()

if __name__ == "__main__":
    # This file can be run directly with: chainlit run example_tasklist.py
    pass 