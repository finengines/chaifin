"""
Diagnose Task List

This script tests the StyledTaskList class to ensure it works correctly.
"""

import asyncio
import logging
import traceback
import importlib
import inspect
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("diagnose-task-list")

async def test_styled_task_list():
    """Test the StyledTaskList class"""
    logger.info("Testing StyledTaskList class...")
    
    try:
        # Import the required modules
        status_updates = importlib.import_module("status_updates")
        cl = importlib.import_module("chainlit")
        
        # Check if StyledTaskList exists
        if not hasattr(status_updates, "StyledTaskList"):
            logger.error("StyledTaskList class not found in status_updates module")
            return False
        
        # Get the StyledTaskList class
        StyledTaskList = getattr(status_updates, "StyledTaskList")
        
        # Check the __init__ method signature
        init_sig = inspect.signature(StyledTaskList.__init__)
        logger.info(f"StyledTaskList.__init__ signature: {init_sig}")
        
        # Check the add_task method signature
        add_task_sig = inspect.signature(StyledTaskList.add_task)
        logger.info(f"StyledTaskList.add_task signature: {add_task_sig}")
        
        # Check the update_task method signature
        update_task_sig = inspect.signature(StyledTaskList.update_task)
        logger.info(f"StyledTaskList.update_task signature: {update_task_sig}")
        
        # Create a mock chainlit context
        class MockChainlitContext:
            def __init__(self):
                self.user_session = {}
            
            def set(self, key, value):
                self.user_session[key] = value
            
            def get(self, key, default=None):
                return self.user_session.get(key, default)
        
        # Create a mock task list
        class MockTaskList:
            def __init__(self, title):
                self.title = title
                self.tasks = []
            
            async def send(self):
                logger.info(f"Sending task list: {self.title}")
                return self
            
            async def add_task(self, task):
                logger.info(f"Adding task: {task.title}")
                self.tasks.append(task)
                return task
            
            async def update(self):
                logger.info(f"Updating task list: {self.title}")
                return self
        
        # Create a mock task
        class MockTask:
            def __init__(self, title, status, icon=None):
                self.title = title
                self.status = status
                self.icon = icon
        
        # Monkey patch chainlit for testing
        cl.TaskList = MockTaskList
        cl.Task = MockTask
        cl.TaskStatus = type('TaskStatus', (), {
            'RUNNING': 'running',
            'DONE': 'done',
            'FAILED': 'failed'
        })
        cl.user_session = MockChainlitContext()
        
        # Test creating a task list
        logger.info("Creating task list...")
        task_list = StyledTaskList(title="Test Task List")
        
        # Test creating the task list
        logger.info("Sending task list...")
        await task_list.create()
        
        # Test adding a task
        logger.info("Adding task...")
        task = await task_list.add_task("Test Task", "running")
        
        # Check if the task was returned
        if task is None:
            logger.error("add_task did not return a task object")
            return False
        
        logger.info(f"Task returned: {task}")
        
        # Test updating a task
        logger.info("Updating task...")
        await task_list.update_task("Test Task", "done")
        
        logger.info("All tests passed!")
        return True
    
    except Exception as e:
        logger.error(f"Error testing StyledTaskList: {str(e)}")
        logger.error(traceback.format_exc())
        return False

async def main():
    """Run the diagnostic tests"""
    success = await test_styled_task_list()
    return success

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        success = loop.run_until_complete(main())
        if success:
            logger.info("All tests passed!")
            exit(0)
        else:
            logger.error("Some tests failed!")
            exit(1)
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}")
        logger.error(traceback.format_exc())
        exit(1) 