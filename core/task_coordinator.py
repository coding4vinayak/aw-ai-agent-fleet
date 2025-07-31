"""
Intelligent Task Coordinator
Automatically assigns tasks to appropriate AI agents and coordinates their execution.
"""

import asyncio
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import re
import logging

from core.agent_framework import BaseAIAgent, AgentRole, MessageType, Priority, communication_hub
from core.communication_system import project_manager, workflow_engine

logger = logging.getLogger(__name__)

class TaskCoordinator:
    """Intelligent coordinator that assigns tasks to appropriate agents."""
    
    def __init__(self):
        self.task_patterns = {
            # Product Development Tasks
            r'(create|build|develop|implement|code|program).*?(app|application|software|system|platform|website|api)': [
                AgentRole.PRODUCT_MANAGER, AgentRole.LEAD_ENGINEER, 
                AgentRole.FRONTEND_ENGINEER, AgentRole.BACKEND_ENGINEER
            ],
            r'(design|ui|ux|interface|wireframe|mockup|prototype)': [
                AgentRole.UX_DESIGNER, AgentRole.UI_DESIGNER, AgentRole.PRODUCT_MANAGER
            ],
            r'(test|qa|quality|bug|testing)': [
                AgentRole.QA_ENGINEER, AgentRole.LEAD_ENGINEER
            ],
            
            # Marketing Tasks
            r'(market|marketing|campaign|promote|advertise|social media|content|blog|seo)': [
                AgentRole.CMO, AgentRole.MARKETING_MANAGER, AgentRole.CONTENT_CREATOR,
                AgentRole.SOCIAL_MEDIA_MANAGER, AgentRole.SEO_SPECIALIST
            ],
            r'(sales|sell|lead|customer|prospect|revenue)': [
                AgentRole.SALES_MANAGER, AgentRole.CUSTOMER_SUCCESS, AgentRole.CMO
            ],
            
            # Financial Tasks
            r'(budget|finance|financial|cost|money|revenue|profit|investment)': [
                AgentRole.CFO, AgentRole.FINANCE_ANALYST
            ],
            
            # Operations Tasks
            r'(process|operation|optimize|efficiency|workflow|procedure)': [
                AgentRole.OPERATIONS_MANAGER, AgentRole.CHRO
            ],
            r'(security|secure|protect|vulnerability|risk)': [
                AgentRole.SECURITY_SPECIALIST, AgentRole.LEGAL_ADVISOR
            ],
            r'(data|analytics|analysis|metrics|report)': [
                AgentRole.DATA_ANALYST, AgentRole.FINANCE_ANALYST
            ],
            r'(legal|compliance|contract|terms|policy)': [
                AgentRole.LEGAL_ADVISOR, AgentRole.CHRO
            ],
            
            # Strategic Tasks
            r'(strategy|strategic|plan|planning|vision|roadmap|decision)': [
                AgentRole.CEO, AgentRole.CTO, AgentRole.CMO, AgentRole.CFO
            ],
            r'(hire|hiring|team|staff|employee|hr|human resources)': [
                AgentRole.CHRO, AgentRole.CEO
            ]
        }
        
        self.active_tasks = {}
        self.task_history = []
    
    async def process_user_task(self, task_description: str, priority: str = "medium", 
                               deadline: Optional[str] = None) -> Dict[str, Any]:
        """Process a user task and coordinate AI agents to complete it."""
        
        task_id = str(uuid.uuid4())
        
        # Analyze task and determine required agents
        analysis = await self.analyze_task(task_description)
        
        # Create execution plan
        execution_plan = await self.create_execution_plan(analysis, priority, deadline)
        
        # Create project and tasks
        project = await self.create_project_for_task(task_description, execution_plan, task_id)
        
        # Assign tasks to agents
        assignments = await self.assign_tasks_to_agents(execution_plan, project.id)
        
        # Start execution
        execution_id = await self.start_task_execution(task_id, assignments)
        
        # Track task
        self.active_tasks[task_id] = {
            "description": task_description,
            "analysis": analysis,
            "execution_plan": execution_plan,
            "project_id": project.id,
            "assignments": assignments,
            "execution_id": execution_id,
            "status": "in_progress",
            "created_at": datetime.now(),
            "deadline": deadline
        }
        
        return {
            "task_id": task_id,
            "status": "accepted",
            "message": f"Task assigned to {len(analysis['required_agents'])} agents",
            "agents_assigned": [agent.value for agent in analysis['required_agents']],
            "estimated_completion": execution_plan['estimated_completion'],
            "execution_plan": execution_plan['phases']
        }
    
    async def analyze_task(self, task_description: str) -> Dict[str, Any]:
        """Analyze task description to determine required agents and complexity."""
        
        task_lower = task_description.lower()
        required_agents = set()
        task_type = "general"
        complexity = "medium"
        
        # Pattern matching to identify required agents
        for pattern, agents in self.task_patterns.items():
            if re.search(pattern, task_lower):
                required_agents.update(agents)
                if "develop" in pattern or "build" in pattern:
                    task_type = "development"
                    complexity = "high"
                elif "market" in pattern:
                    task_type = "marketing"
                elif "strategy" in pattern:
                    task_type = "strategic"
                    complexity = "high"
        
        # If no specific patterns match, assign to CEO for delegation
        if not required_agents:
            required_agents.add(AgentRole.CEO)
            task_type = "general"
        
        # Always include CEO for strategic oversight on complex tasks
        if complexity == "high":
            required_agents.add(AgentRole.CEO)
        
        # Determine estimated duration based on complexity and agents
        agent_count = len(required_agents)
        if complexity == "high":
            estimated_hours = agent_count * 8
        elif complexity == "medium":
            estimated_hours = agent_count * 4
        else:
            estimated_hours = agent_count * 2
        
        return {
            "task_type": task_type,
            "complexity": complexity,
            "required_agents": list(required_agents),
            "estimated_hours": estimated_hours,
            "keywords": self.extract_keywords(task_description)
        }
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract key words from task description."""
        # Simple keyword extraction
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [w for w in words if len(w) > 3 and w not in ['this', 'that', 'with', 'from', 'they', 'have', 'will', 'been', 'were']]
        return keywords[:10]  # Top 10 keywords
    
    async def create_execution_plan(self, analysis: Dict[str, Any], priority: str, deadline: Optional[str]) -> Dict[str, Any]:
        """Create detailed execution plan for the task."""
        
        complexity = analysis['complexity']
        agent_count = len(analysis['required_agents'])
        
        # Determine phases based on task type
        if analysis['task_type'] == "development":
            phases = [
                {"name": "Requirements Analysis", "duration": "1-2 days", "agents": ["product_manager"]},
                {"name": "Technical Design", "duration": "2-3 days", "agents": ["lead_engineer", "ux_designer"]},
                {"name": "Implementation", "duration": "5-10 days", "agents": ["frontend_engineer", "backend_engineer"]},
                {"name": "Testing & QA", "duration": "2-3 days", "agents": ["qa_engineer"]},
                {"name": "Deployment", "duration": "1 day", "agents": ["devops_engineer"]}
            ]
        elif analysis['task_type'] == "marketing":
            phases = [
                {"name": "Strategy Development", "duration": "1-2 days", "agents": ["cmo", "marketing_manager"]},
                {"name": "Content Creation", "duration": "3-5 days", "agents": ["content_creator", "ui_designer"]},
                {"name": "Campaign Setup", "duration": "2-3 days", "agents": ["marketing_manager", "social_media_manager"]},
                {"name": "Launch & Monitor", "duration": "ongoing", "agents": ["marketing_manager", "data_analyst"]}
            ]
        elif analysis['task_type'] == "strategic":
            phases = [
                {"name": "Analysis & Research", "duration": "2-3 days", "agents": ["ceo", "data_analyst"]},
                {"name": "Strategy Formulation", "duration": "2-3 days", "agents": ["ceo", "cto", "cmo", "cfo"]},
                {"name": "Implementation Planning", "duration": "1-2 days", "agents": ["operations_manager"]},
                {"name": "Execution", "duration": "varies", "agents": ["all_relevant"]}
            ]
        else:
            phases = [
                {"name": "Task Analysis", "duration": "1 day", "agents": ["ceo"]},
                {"name": "Resource Assignment", "duration": "1 day", "agents": ["chro"]},
                {"name": "Execution", "duration": "2-5 days", "agents": ["assigned_agents"]},
                {"name": "Review & Completion", "duration": "1 day", "agents": ["ceo"]}
            ]
        
        # Calculate estimated completion
        base_days = len(phases) * 2 if complexity == "high" else len(phases)
        estimated_completion = datetime.now() + timedelta(days=base_days)
        
        return {
            "phases": phases,
            "estimated_completion": estimated_completion.isoformat(),
            "priority": priority,
            "complexity": complexity,
            "resource_requirements": f"{agent_count} agents, {analysis['estimated_hours']} hours"
        }
    
    async def create_project_for_task(self, task_description: str, execution_plan: Dict[str, Any], task_id: str) -> Any:
        """Create a project for the user task."""
        
        project_data = {
            "name": f"User Task: {task_description[:50]}...",
            "description": task_description,
            "owner": "task_coordinator",
            "priority": execution_plan["priority"],
            "start_date": datetime.now().isoformat(),
            "target_date": execution_plan["estimated_completion"],
            "stakeholders": ["task_coordinator", "ceo_001"],
            "success_metrics": ["Task completed successfully", "User satisfaction achieved"]
        }
        
        project = project_manager.create_project(project_data)
        return project
    
    async def assign_tasks_to_agents(self, execution_plan: Dict[str, Any], project_id: str) -> List[Dict[str, Any]]:
        """Assign specific tasks to agents based on execution plan."""
        
        assignments = []
        
        for i, phase in enumerate(execution_plan["phases"]):
            task_data = {
                "title": phase["name"],
                "description": f"Complete {phase['name']} phase of the user task",
                "priority": execution_plan["priority"],
                "duration_days": 2,
                "phase_order": i + 1
            }
            
            # Assign to first available agent type mentioned in phase
            if phase["agents"] and phase["agents"][0] != "all_relevant":
                agent_role = phase["agents"][0]
                agent_id = f"{agent_role}_001"
                
                task = await project_manager.create_task_from_template(project_id, task_data)
                
                assignments.append({
                    "task_id": task.id,
                    "agent_id": agent_id,
                    "phase": phase["name"],
                    "status": "assigned"
                })
        
        return assignments
    
    async def start_task_execution(self, task_id: str, assignments: List[Dict[str, Any]]) -> str:
        """Start executing the task with assigned agents."""
        
        # Create workflow for task execution
        workflow_steps = []
        
        for assignment in assignments:
            workflow_steps.append({
                "type": "send_message",
                "sender": "task_coordinator",
                "recipient": assignment["agent_id"],
                "message_type": "task_assignment",
                "content": {
                    "task_id": assignment["task_id"],
                    "phase": assignment["phase"],
                    "user_task_id": task_id
                },
                "priority": "high"
            })
        
        # Register and trigger workflow
        from core.communication_system import Workflow
        workflow = Workflow(
            id=f"user_task_{task_id}",
            name=f"User Task Execution {task_id[:8]}",
            description="Automated execution of user-assigned task",
            steps=workflow_steps,
            triggers=["task_coordinator"],
            conditions=["agents_available"],
            outputs=["completed_task"],
            created_by="task_coordinator",
            created_at=datetime.now()
        )
        
        workflow_engine.register_workflow(workflow)
        execution_id = await workflow_engine.trigger_workflow(workflow.id, {"task_id": task_id})
        
        return execution_id
    
    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get current status of a task."""
        
        if task_id not in self.active_tasks:
            return {"error": "Task not found"}
        
        task = self.active_tasks[task_id]
        
        # Check progress of assigned agents
        progress = []
        for assignment in task["assignments"]:
            agent_id = assignment["agent_id"]
            if agent_id in communication_hub.agents:
                agent = communication_hub.agents[agent_id]
                agent_status = agent.get_status()
                progress.append({
                    "agent": agent_status["name"],
                    "phase": assignment["phase"],
                    "status": assignment["status"],
                    "active_tasks": agent_status["active_tasks"]
                })
        
        return {
            "task_id": task_id,
            "description": task["description"],
            "status": task["status"],
            "progress": progress,
            "created_at": task["created_at"].isoformat(),
            "estimated_completion": task["execution_plan"]["estimated_completion"]
        }
    
    async def list_active_tasks(self) -> List[Dict[str, Any]]:
        """List all active tasks."""
        
        active = []
        for task_id, task in self.active_tasks.items():
            active.append({
                "task_id": task_id,
                "description": task["description"][:100] + "..." if len(task["description"]) > 100 else task["description"],
                "status": task["status"],
                "agents_count": len(task["assignments"]),
                "created_at": task["created_at"].isoformat()
            })
        
        return active
    
    async def complete_task(self, task_id: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Mark a task as completed."""
        
        if task_id in self.active_tasks:
            self.active_tasks[task_id]["status"] = "completed"
            self.active_tasks[task_id]["completed_at"] = datetime.now()
            self.active_tasks[task_id]["result"] = result
            
            # Move to history
            self.task_history.append(self.active_tasks[task_id])
            del self.active_tasks[task_id]
            
            return {"status": "completed", "message": "Task marked as completed"}
        
        return {"error": "Task not found"}

# Global task coordinator instance
task_coordinator = TaskCoordinator()
