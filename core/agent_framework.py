"""
Core AI Agent Framework
Provides base classes and communication infrastructure for all AI agents in the company.
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessageType(Enum):
    TASK_ASSIGNMENT = "task_assignment"
    STATUS_UPDATE = "status_update"
    COLLABORATION_REQUEST = "collaboration_request"
    DECISION_REQUEST = "decision_request"
    INFORMATION_SHARE = "information_share"
    ESCALATION = "escalation"

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

@dataclass
class Message:
    id: str
    sender: str
    recipient: str
    message_type: MessageType
    content: Dict[str, Any]
    priority: Priority
    timestamp: datetime
    requires_response: bool = False
    deadline: Optional[datetime] = None

@dataclass
class Task:
    id: str
    title: str
    description: str
    assigned_to: str
    created_by: str
    priority: Priority
    status: str = "pending"
    dependencies: List[str] = None
    deliverables: List[str] = None
    deadline: Optional[datetime] = None
    created_at: datetime = None
    updated_at: datetime = None

class AgentRole(Enum):
    # Executive
    CEO = "ceo"
    CTO = "cto"
    CMO = "cmo"
    CFO = "cfo"
    CHRO = "chro"
    
    # Product Development
    PRODUCT_MANAGER = "product_manager"
    LEAD_ENGINEER = "lead_engineer"
    FRONTEND_ENGINEER = "frontend_engineer"
    BACKEND_ENGINEER = "backend_engineer"
    DEVOPS_ENGINEER = "devops_engineer"
    QA_ENGINEER = "qa_engineer"
    UX_DESIGNER = "ux_designer"
    UI_DESIGNER = "ui_designer"
    
    # Marketing & Sales
    MARKETING_MANAGER = "marketing_manager"
    CONTENT_CREATOR = "content_creator"
    SOCIAL_MEDIA_MANAGER = "social_media_manager"
    SEO_SPECIALIST = "seo_specialist"
    SALES_MANAGER = "sales_manager"
    CUSTOMER_SUCCESS = "customer_success"
    
    # Operations
    OPERATIONS_MANAGER = "operations_manager"
    FINANCE_ANALYST = "finance_analyst"
    LEGAL_ADVISOR = "legal_advisor"
    DATA_ANALYST = "data_analyst"
    SECURITY_SPECIALIST = "security_specialist"

class BaseAIAgent:
    """Base class for all AI agents in the company."""
    
    def __init__(self, agent_id: str, role: AgentRole, name: str):
        self.agent_id = agent_id
        self.role = role
        self.name = name
        self.inbox: List[Message] = []
        self.outbox: List[Message] = []
        self.tasks: List[Task] = []
        self.knowledge_base: Dict[str, Any] = {}
        self.is_active = True
        self.last_activity = datetime.now()
        
        # Communication system
        self.message_handlers: Dict[MessageType, Callable] = {
            MessageType.TASK_ASSIGNMENT: self.handle_task_assignment,
            MessageType.STATUS_UPDATE: self.handle_status_update,
            MessageType.COLLABORATION_REQUEST: self.handle_collaboration_request,
            MessageType.DECISION_REQUEST: self.handle_decision_request,
            MessageType.INFORMATION_SHARE: self.handle_information_share,
            MessageType.ESCALATION: self.handle_escalation,
        }
    
    async def process_messages(self):
        """Process all pending messages in inbox."""
        while self.inbox:
            message = self.inbox.pop(0)
            await self.handle_message(message)
    
    async def handle_message(self, message: Message):
        """Route message to appropriate handler."""
        handler = self.message_handlers.get(message.message_type)
        if handler:
            await handler(message)
        else:
            logger.warning(f"No handler for message type: {message.message_type}")
    
    async def send_message(self, recipient: str, message_type: MessageType, 
                          content: Dict[str, Any], priority: Priority = Priority.MEDIUM,
                          requires_response: bool = False, deadline: Optional[datetime] = None):
        """Send a message to another agent."""
        message = Message(
            id=str(uuid.uuid4()),
            sender=self.agent_id,
            recipient=recipient,
            message_type=message_type,
            content=content,
            priority=priority,
            timestamp=datetime.now(),
            requires_response=requires_response,
            deadline=deadline
        )
        
        self.outbox.append(message)
        # In a real implementation, this would use a message queue
        await self.deliver_message(message)
    
    async def deliver_message(self, message: Message):
        """Deliver message to recipient (placeholder for message queue)."""
        # This would integrate with Redis/RabbitMQ in production
        logger.info(f"Message sent from {message.sender} to {message.recipient}: {message.message_type}")
    
    # Message handlers (to be overridden by specific agent types)
    async def handle_task_assignment(self, message: Message):
        """Handle task assignment messages."""
        task_data = message.content
        task = Task(**task_data)
        self.tasks.append(task)
        logger.info(f"{self.name} received task: {task.title}")
    
    async def handle_status_update(self, message: Message):
        """Handle status update messages."""
        logger.info(f"{self.name} received status update from {message.sender}")
    
    async def handle_collaboration_request(self, message: Message):
        """Handle collaboration requests."""
        logger.info(f"{self.name} received collaboration request from {message.sender}")
    
    async def handle_decision_request(self, message: Message):
        """Handle decision requests."""
        logger.info(f"{self.name} received decision request from {message.sender}")
    
    async def handle_information_share(self, message: Message):
        """Handle information sharing."""
        info = message.content
        self.knowledge_base.update(info)
        logger.info(f"{self.name} received information update")
    
    async def handle_escalation(self, message: Message):
        """Handle escalation messages."""
        logger.info(f"{self.name} received escalation from {message.sender}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status."""
        return {
            "agent_id": self.agent_id,
            "role": self.role.value,
            "name": self.name,
            "is_active": self.is_active,
            "last_activity": self.last_activity.isoformat(),
            "pending_messages": len(self.inbox),
            "active_tasks": len([t for t in self.tasks if t.status == "in_progress"]),
            "completed_tasks": len([t for t in self.tasks if t.status == "completed"])
        }
    
    async def daily_standup(self) -> Dict[str, Any]:
        """Generate daily standup report."""
        return {
            "agent": self.name,
            "role": self.role.value,
            "yesterday": self.get_yesterday_accomplishments(),
            "today": self.get_today_plans(),
            "blockers": self.get_current_blockers()
        }
    
    def get_yesterday_accomplishments(self) -> List[str]:
        """Get yesterday's accomplishments (to be overridden)."""
        return ["Processed messages", "Updated knowledge base"]
    
    def get_today_plans(self) -> List[str]:
        """Get today's plans (to be overridden)."""
        return ["Continue assigned tasks", "Collaborate with team"]
    
    def get_current_blockers(self) -> List[str]:
        """Get current blockers (to be overridden)."""
        return []

class CommunicationHub:
    """Central communication hub for all agents."""
    
    def __init__(self):
        self.agents: Dict[str, BaseAIAgent] = {}
        self.message_queue: List[Message] = []
        self.global_knowledge_base: Dict[str, Any] = {}
    
    def register_agent(self, agent: BaseAIAgent):
        """Register an agent with the communication hub."""
        self.agents[agent.agent_id] = agent
        logger.info(f"Registered agent: {agent.name} ({agent.role.value})")
    
    async def route_message(self, message: Message):
        """Route message to the appropriate agent."""
        recipient = self.agents.get(message.recipient)
        if recipient:
            recipient.inbox.append(message)
        else:
            logger.error(f"Recipient not found: {message.recipient}")
    
    async def broadcast_message(self, sender: str, message_type: MessageType, 
                               content: Dict[str, Any], priority: Priority = Priority.MEDIUM):
        """Broadcast message to all agents."""
        for agent_id, agent in self.agents.items():
            if agent_id != sender:
                message = Message(
                    id=str(uuid.uuid4()),
                    sender=sender,
                    recipient=agent_id,
                    message_type=message_type,
                    content=content,
                    priority=priority,
                    timestamp=datetime.now()
                )
                await self.route_message(message)
    
    def get_company_status(self) -> Dict[str, Any]:
        """Get overall company status."""
        return {
            "total_agents": len(self.agents),
            "active_agents": len([a for a in self.agents.values() if a.is_active]),
            "agents": [agent.get_status() for agent in self.agents.values()]
        }

# Global communication hub instance
communication_hub = CommunicationHub()
