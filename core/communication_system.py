"""
Communication & Coordination System
Manages inter-agent communication, task tracking, and progress monitoring.
"""

import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import logging

from core.agent_framework import BaseAIAgent, AgentRole, MessageType, Priority, Task, Message, communication_hub

logger = logging.getLogger(__name__)

class ProjectStatus(Enum):
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

@dataclass
class Project:
    id: str
    name: str
    description: str
    owner: str
    status: ProjectStatus
    priority: Priority
    start_date: datetime
    target_date: datetime
    completion_date: Optional[datetime] = None
    budget: Optional[float] = None
    stakeholders: List[str] = None
    tasks: List[str] = None
    dependencies: List[str] = None
    success_metrics: List[str] = None
    created_at: datetime = None
    updated_at: datetime = None

@dataclass
class Workflow:
    id: str
    name: str
    description: str
    steps: List[Dict[str, Any]]
    triggers: List[str]
    conditions: List[str]
    outputs: List[str]
    created_by: str
    created_at: datetime
    is_active: bool = True

class WorkflowEngine:
    """Manages automated workflows between agents."""
    
    def __init__(self):
        self.workflows: Dict[str, Workflow] = {}
        self.active_executions: Dict[str, Dict[str, Any]] = {}
    
    def register_workflow(self, workflow: Workflow):
        """Register a new workflow."""
        self.workflows[workflow.id] = workflow
        logger.info(f"Registered workflow: {workflow.name}")
    
    async def trigger_workflow(self, workflow_id: str, trigger_data: Dict[str, Any]) -> str:
        """Trigger a workflow execution."""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.workflows[workflow_id]
        execution_id = str(uuid.uuid4())
        
        execution = {
            "id": execution_id,
            "workflow_id": workflow_id,
            "status": "running",
            "current_step": 0,
            "start_time": datetime.now(),
            "trigger_data": trigger_data,
            "step_results": []
        }
        
        self.active_executions[execution_id] = execution
        await self.execute_workflow(execution_id)
        return execution_id
    
    async def execute_workflow(self, execution_id: str):
        """Execute workflow steps."""
        execution = self.active_executions[execution_id]
        workflow = self.workflows[execution["workflow_id"]]
        
        for i, step in enumerate(workflow.steps):
            execution["current_step"] = i
            result = await self.execute_step(step, execution)
            execution["step_results"].append(result)
            
            if not result.get("success", False):
                execution["status"] = "failed"
                logger.error(f"Workflow {workflow.name} failed at step {i}")
                return
        
        execution["status"] = "completed"
        execution["end_time"] = datetime.now()
        logger.info(f"Workflow {workflow.name} completed successfully")
    
    async def execute_step(self, step: Dict[str, Any], execution: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow step."""
        step_type = step.get("type")
        
        if step_type == "send_message":
            return await self.execute_send_message_step(step, execution)
        elif step_type == "create_task":
            return await self.execute_create_task_step(step, execution)
        elif step_type == "wait_for_completion":
            return await self.execute_wait_step(step, execution)
        elif step_type == "conditional":
            return await self.execute_conditional_step(step, execution)
        else:
            logger.warning(f"Unknown step type: {step_type}")
            return {"success": False, "error": f"Unknown step type: {step_type}"}
    
    async def execute_send_message_step(self, step: Dict[str, Any], execution: Dict[str, Any]) -> Dict[str, Any]:
        """Execute send message step."""
        try:
            message = Message(
                id=str(uuid.uuid4()),
                sender=step.get("sender", "workflow_engine"),
                recipient=step.get("recipient"),
                message_type=MessageType(step.get("message_type")),
                content=step.get("content", {}),
                priority=Priority(step.get("priority", Priority.MEDIUM.value)),
                timestamp=datetime.now()
            )

            await communication_hub.route_message(message)
            return {"success": True, "message_id": message.id}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def execute_create_task_step(self, step: Dict[str, Any], execution: Dict[str, Any]) -> Dict[str, Any]:
        """Execute create task step."""
        try:
            task_data = step.get("task_data", {})
            # In a real implementation, this would create a task in the project manager
            return {"success": True, "task_created": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def execute_wait_step(self, step: Dict[str, Any], execution: Dict[str, Any]) -> Dict[str, Any]:
        """Execute wait step."""
        try:
            wait_time = step.get("timeout", 60)  # Default 60 seconds
            # For demo purposes, we'll just simulate the wait
            await asyncio.sleep(min(wait_time, 1))  # Max 1 second for demo
            return {"success": True, "waited": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def execute_conditional_step(self, step: Dict[str, Any], execution: Dict[str, Any]) -> Dict[str, Any]:
        """Execute conditional step."""
        try:
            condition = step.get("condition", True)
            # For demo purposes, we'll assume conditions are met
            return {"success": True, "condition_met": condition}
        except Exception as e:
            return {"success": False, "error": str(e)}

class ProjectManager:
    """Manages projects and coordinates work across agents."""
    
    def __init__(self):
        self.projects: Dict[str, Project] = {}
        self.tasks: Dict[str, Task] = {}
        self.project_templates: Dict[str, Dict[str, Any]] = {}
    
    def create_project(self, project_data: Dict[str, Any]) -> Project:
        """Create a new project."""
        # Convert string priority to enum
        priority_str = project_data.get("priority", "medium")
        if isinstance(priority_str, str):
            priority_map = {
                "low": Priority.LOW,
                "medium": Priority.MEDIUM,
                "high": Priority.HIGH,
                "urgent": Priority.URGENT
            }
            priority = priority_map.get(priority_str.lower(), Priority.MEDIUM)
        else:
            priority = priority_str

        project = Project(
            id=str(uuid.uuid4()),
            name=project_data["name"],
            description=project_data["description"],
            owner=project_data["owner"],
            status=ProjectStatus.PLANNING,
            priority=priority,
            start_date=datetime.fromisoformat(project_data["start_date"]),
            target_date=datetime.fromisoformat(project_data["target_date"]),
            budget=project_data.get("budget"),
            stakeholders=project_data.get("stakeholders", []),
            tasks=[],
            dependencies=project_data.get("dependencies", []),
            success_metrics=project_data.get("success_metrics", []),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self.projects[project.id] = project
        logger.info(f"Created project: {project.name}")
        return project
    
    async def create_project_from_template(self, template_name: str, project_data: Dict[str, Any]) -> Project:
        """Create project from template."""
        if template_name not in self.project_templates:
            raise ValueError(f"Template {template_name} not found")
        
        template = self.project_templates[template_name]
        
        # Merge template data with provided data
        merged_data = {**template, **project_data}
        project = self.create_project(merged_data)
        
        # Create tasks from template
        for task_template in template.get("task_templates", []):
            await self.create_task_from_template(project.id, task_template)
        
        return project
    
    async def create_task_from_template(self, project_id: str, task_template: Dict[str, Any]) -> Task:
        """Create task from template."""
        # Convert string priority to enum
        priority_str = task_template.get("priority", "medium")
        if isinstance(priority_str, str):
            priority_map = {
                "low": Priority.LOW,
                "medium": Priority.MEDIUM,
                "high": Priority.HIGH,
                "urgent": Priority.URGENT
            }
            priority = priority_map.get(priority_str.lower(), Priority.MEDIUM)
        else:
            priority = priority_str

        task = Task(
            id=str(uuid.uuid4()),
            title=task_template["title"],
            description=task_template["description"],
            assigned_to=task_template.get("assigned_to"),
            created_by="project_manager",
            priority=priority,
            status=TaskStatus.PENDING.value,
            dependencies=task_template.get("dependencies", []),
            deliverables=task_template.get("deliverables", []),
            deadline=datetime.now() + timedelta(days=task_template.get("duration_days", 7)),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self.tasks[task.id] = task
        
        # Add task to project
        if project_id in self.projects:
            self.projects[project_id].tasks.append(task.id)
        
        # Assign task to agent
        if task.assigned_to:
            await self.assign_task_to_agent(task.id, task.assigned_to)
        
        return task
    
    async def assign_task_to_agent(self, task_id: str, agent_id: str):
        """Assign task to an agent."""
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        # Send task assignment message
        message = Message(
            id=str(uuid.uuid4()),
            sender="project_manager",
            recipient=agent_id,
            message_type=MessageType.TASK_ASSIGNMENT,
            content=asdict(task),
            priority=task.priority,
            timestamp=datetime.now(),
            requires_response=True
        )
        
        await communication_hub.route_message(message)
        logger.info(f"Assigned task {task.title} to {agent_id}")

class StandupManager:
    """Manages daily standup meetings and status updates."""
    
    def __init__(self):
        self.standup_schedule = {}
        self.standup_reports = {}
    
    async def conduct_daily_standup(self) -> Dict[str, Any]:
        """Conduct daily standup with all agents."""
        standup_report = {
            "date": datetime.now().date().isoformat(),
            "participants": [],
            "summary": {},
            "blockers": [],
            "action_items": []
        }
        
        # Collect reports from all agents
        for agent_id, agent in communication_hub.agents.items():
            if agent.is_active:
                agent_report = await agent.daily_standup()
                standup_report["participants"].append(agent_id)
                standup_report["summary"][agent_id] = agent_report
                
                # Collect blockers
                blockers = agent_report.get("blockers", [])
                for blocker in blockers:
                    standup_report["blockers"].append({
                        "agent": agent_id,
                        "blocker": blocker
                    })
        
        # Generate action items for blockers
        standup_report["action_items"] = await self.generate_action_items(standup_report["blockers"])
        
        # Store report
        self.standup_reports[standup_report["date"]] = standup_report
        
        # Send summary to leadership
        await self.send_standup_summary(standup_report)
        
        return standup_report
    
    async def generate_action_items(self, blockers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate action items to resolve blockers."""
        action_items = []
        
        for blocker in blockers:
            action_item = {
                "id": str(uuid.uuid4()),
                "description": f"Resolve blocker: {blocker['blocker']}",
                "assigned_to": "operations_manager",
                "priority": Priority.HIGH,
                "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
                "related_agent": blocker["agent"]
            }
            action_items.append(action_item)
        
        return action_items
    
    async def send_standup_summary(self, standup_report: Dict[str, Any]):
        """Send standup summary to leadership team."""
        leadership_roles = [AgentRole.CEO, AgentRole.CTO, AgentRole.CMO, AgentRole.CFO, AgentRole.CHRO]
        
        for role in leadership_roles:
            agent_id = f"{role.value}_001"
            if agent_id in communication_hub.agents:
                message = Message(
                    id=str(uuid.uuid4()),
                    sender="standup_manager",
                    recipient=agent_id,
                    message_type=MessageType.STATUS_UPDATE,
                    content={"standup_report": standup_report},
                    priority=Priority.MEDIUM,
                    timestamp=datetime.now()
                )
                await communication_hub.route_message(message)

class PerformanceMonitor:
    """Monitors agent and system performance."""
    
    def __init__(self):
        self.performance_metrics = {}
        self.alerts = []
    
    async def collect_performance_metrics(self) -> Dict[str, Any]:
        """Collect performance metrics from all agents."""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "system_metrics": await self.collect_system_metrics(),
            "agent_metrics": await self.collect_agent_metrics(),
            "project_metrics": await self.collect_project_metrics(),
            "communication_metrics": await self.collect_communication_metrics()
        }
        
        # Store metrics
        self.performance_metrics[metrics["timestamp"]] = metrics
        
        # Check for alerts
        await self.check_performance_alerts(metrics)
        
        return metrics
    
    async def collect_system_metrics(self) -> Dict[str, Any]:
        """Collect system-level metrics."""
        return {
            "total_agents": len(communication_hub.agents),
            "active_agents": len([a for a in communication_hub.agents.values() if a.is_active]),
            "message_queue_size": len(communication_hub.message_queue),
            "system_uptime": "99.9%",
            "response_time_avg": "1.2 seconds"
        }
    
    async def collect_agent_metrics(self) -> Dict[str, Any]:
        """Collect agent-specific metrics."""
        agent_metrics = {}
        
        for agent_id, agent in communication_hub.agents.items():
            agent_metrics[agent_id] = {
                "status": agent.get_status(),
                "task_completion_rate": "95%",
                "average_response_time": "2.1 seconds",
                "quality_score": "4.3/5.0",
                "collaboration_score": "4.5/5.0"
            }
        
        return agent_metrics

# Global instances
workflow_engine = WorkflowEngine()
project_manager = ProjectManager()
standup_manager = StandupManager()
performance_monitor = PerformanceMonitor()
