"""
Simple Task Assignment Script
Quick way to assign tasks to the AI company from command line.
"""

import asyncio
import sys
from task_interface import TaskInterface

async def main():
    """Main function to handle task assignment."""
    
    if len(sys.argv) < 2:
        print("🤖 AI Company Task Assignment")
        print("=" * 40)
        print("Usage:")
        print("  py assign_task.py \"<task description>\"")
        print("  py assign_task.py demo")
        print("  py assign_task.py interactive")
        print()
        print("Examples:")
        print("  py assign_task.py \"Create a mobile app for task management\"")
        print("  py assign_task.py \"Design a marketing campaign for our product\"")
        print("  py assign_task.py \"Analyze our financial performance\"")
        return
    
    interface = TaskInterface()
    
    if sys.argv[1].lower() == "demo":
        # Run quick demo
        from task_interface import quick_demo
        await quick_demo()
    
    elif sys.argv[1].lower() == "interactive":
        # Run interactive mode
        from task_interface import interactive_mode
        await interactive_mode()
    
    else:
        # Single task assignment
        task_description = " ".join(sys.argv[1:])
        
        print("🤖 AI Company Task Assignment")
        print("=" * 50)
        
        try:
            result = await interface.process_task(task_description)
            
            print(f"\n🎉 Task successfully assigned!")
            print(f"📋 Task ID: {result['task_id']}")
            print(f"⏰ You can check status later with:")
            print(f"   py assign_task.py status {result['task_id']}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
