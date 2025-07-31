"""
Interactive Task Assignment Interface
User-friendly interface for assigning tasks to AI agents.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any

from core.task_coordinator import task_coordinator
from core.agent_framework import communication_hub
from workflows.product_launch_demo import ProductLaunchDemo

class TaskInterface:
    """Interactive interface for task assignment and management."""
    
    def __init__(self):
        self.demo = ProductLaunchDemo()
        self.is_initialized = False
    
    async def initialize_company(self):
        """Initialize the AI company if not already done."""
        if not self.is_initialized:
            print("🚀 Initializing AI Company...")
            await self.demo.initialize_company()
            self.is_initialized = True
            print("✅ AI Company ready for tasks!")
    
    async def process_task(self, task_description: str, priority: str = "medium", deadline: str = None) -> Dict[str, Any]:
        """Process a user task through the AI company."""
        
        await self.initialize_company()
        
        print(f"\n📋 Processing Task: {task_description}")
        print("=" * 60)
        
        # Assign task to AI agents
        result = await task_coordinator.process_user_task(task_description, priority, deadline)
        
        print(f"✅ Task Accepted!")
        print(f"📊 Task ID: {result['task_id']}")
        print(f"👥 Agents Assigned: {len(result['agents_assigned'])}")
        print(f"🎯 Estimated Completion: {result['estimated_completion']}")
        
        print(f"\n🤖 Assigned Agents:")
        for agent in result['agents_assigned']:
            print(f"   • {agent.replace('_', ' ').title()}")
        
        print(f"\n📈 Execution Plan:")
        for i, phase in enumerate(result['execution_plan'], 1):
            print(f"   {i}. {phase['name']} ({phase['duration']})")
        
        return result
    
    async def check_task_status(self, task_id: str) -> Dict[str, Any]:
        """Check the status of a specific task."""
        
        status = await task_coordinator.get_task_status(task_id)
        
        if "error" in status:
            print(f"❌ {status['error']}")
            return status
        
        print(f"\n📊 Task Status: {task_id}")
        print("=" * 40)
        print(f"Description: {status['description']}")
        print(f"Status: {status['status'].upper()}")
        print(f"Created: {status['created_at']}")
        print(f"Est. Completion: {status['estimated_completion']}")
        
        print(f"\n👥 Agent Progress:")
        for progress in status['progress']:
            print(f"   • {progress['agent']}: {progress['phase']} - {progress['status']}")
        
        return status
    
    async def list_active_tasks(self) -> list:
        """List all active tasks."""
        
        tasks = await task_coordinator.list_active_tasks()
        
        if not tasks:
            print("📝 No active tasks")
            return []
        
        print(f"\n📋 Active Tasks ({len(tasks)}):")
        print("=" * 50)
        
        for task in tasks:
            print(f"🆔 {task['task_id'][:8]}... - {task['description']}")
            print(f"   Status: {task['status']} | Agents: {task['agents_count']} | Created: {task['created_at']}")
            print()
        
        return tasks
    
    async def get_company_status(self) -> Dict[str, Any]:
        """Get overall company status."""
        
        await self.initialize_company()
        
        status = communication_hub.get_company_status()
        
        print(f"\n🏢 AI Company Status:")
        print("=" * 30)
        print(f"Total Agents: {status['total_agents']}")
        print(f"Active Agents: {status['active_agents']}")
        
        print(f"\n👥 Agent Details:")
        for agent_status in status['agents']:
            name = agent_status['name']
            role = agent_status['role'].replace('_', ' ').title()
            active = "🟢" if agent_status['is_active'] else "🔴"
            tasks = agent_status['active_tasks']
            print(f"   {active} {name} ({role}) - {tasks} active tasks")
        
        return status

async def interactive_mode():
    """Run interactive task assignment mode."""
    
    interface = TaskInterface()
    
    print("🤖 AI Company - Interactive Task Assignment")
    print("=" * 50)
    print("Commands:")
    print("  task <description>     - Assign a new task")
    print("  status <task_id>       - Check task status")
    print("  list                   - List active tasks")
    print("  company                - Show company status")
    print("  help                   - Show this help")
    print("  exit                   - Exit interface")
    print()
    
    while True:
        try:
            command = input("ai-company> ").strip()
            
            if command.lower() in ['exit', 'quit']:
                print("👋 Goodbye!")
                break
            
            elif command.lower() == 'help':
                print("\nAvailable commands:")
                print("  task <description>     - Assign a new task")
                print("  status <task_id>       - Check task status") 
                print("  list                   - List active tasks")
                print("  company                - Show company status")
                print("  help                   - Show this help")
                print("  exit                   - Exit interface")
            
            elif command.lower().startswith('task '):
                task_desc = command[5:].strip()
                if task_desc:
                    await interface.process_task(task_desc)
                else:
                    print("❌ Please provide a task description")
            
            elif command.lower().startswith('status '):
                task_id = command[7:].strip()
                if task_id:
                    await interface.check_task_status(task_id)
                else:
                    print("❌ Please provide a task ID")
            
            elif command.lower() == 'list':
                await interface.list_active_tasks()
            
            elif command.lower() == 'company':
                await interface.get_company_status()
            
            elif command.strip() == '':
                continue
            
            else:
                print(f"❌ Unknown command: {command}")
                print("Type 'help' for available commands")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

async def quick_demo():
    """Run a quick demo of task assignment."""
    
    interface = TaskInterface()
    
    print("🎯 Quick Task Assignment Demo")
    print("=" * 40)
    
    # Demo tasks
    demo_tasks = [
        "Create a mobile app for task management",
        "Design a marketing campaign for our new product",
        "Analyze our financial performance and create a budget",
        "Develop a security audit for our systems",
        "Create a hiring plan for expanding our engineering team"
    ]
    
    results = []
    
    for task in demo_tasks:
        print(f"\n📋 Assigning: {task}")
        result = await interface.process_task(task)
        results.append(result)
        
        # Small delay for demo effect
        await asyncio.sleep(1)
    
    print(f"\n🎉 Demo Complete!")
    print(f"✅ Successfully assigned {len(results)} tasks")
    
    # Show active tasks
    await interface.list_active_tasks()
    
    return results

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        asyncio.run(quick_demo())
    else:
        asyncio.run(interactive_mode())
