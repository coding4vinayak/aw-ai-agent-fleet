"""
Basic functionality tests for the AI Company system.
"""

import pytest
import asyncio
from datetime import datetime, timedelta

from core.agent_framework import BaseAIAgent, AgentRole, MessageType, Priority, Task, Message, communication_hub
from core.communication_system import project_manager, workflow_engine, ProjectStatus
from agents.executive_agents import CEOAgent, CTOAgent
from agents.product_development_agents import ProductManagerAgent

class TestAgentFramework:
    """Test the core agent framework functionality."""
    
    def test_agent_creation(self):
        """Test creating a basic AI agent."""
        agent = BaseAIAgent("test_001", AgentRole.CEO, "Test Agent")
        
        assert agent.agent_id == "test_001"
        assert agent.role == AgentRole.CEO
        assert agent.name == "Test Agent"
        assert agent.is_active == True
        assert len(agent.inbox) == 0
        assert len(agent.outbox) == 0
        assert len(agent.tasks) == 0
    
    def test_agent_status(self):
        """Test agent status reporting."""
        agent = BaseAIAgent("test_002", AgentRole.CTO, "Test CTO")
        status = agent.get_status()
        
        assert status["agent_id"] == "test_002"
        assert status["role"] == "cto"
        assert status["name"] == "Test CTO"
        assert status["is_active"] == True
        assert status["pending_messages"] == 0
        assert status["active_tasks"] == 0
        assert status["completed_tasks"] == 0
    
    @pytest.mark.asyncio
    async def test_message_handling(self):
        """Test message sending and handling."""
        sender = BaseAIAgent("sender_001", AgentRole.CEO, "Sender")
        recipient = BaseAIAgent("recipient_001", AgentRole.CTO, "Recipient")
        
        # Register agents
        communication_hub.register_agent(sender)
        communication_hub.register_agent(recipient)
        
        # Send message
        await sender.send_message(
            recipient="recipient_001",
            message_type=MessageType.TASK_ASSIGNMENT,
            content={"task": "Test task"},
            priority=Priority.HIGH
        )
        
        # Check message was sent
        assert len(sender.outbox) == 1
        
        # Process messages
        await recipient.process_messages()
        
        # Verify message was processed
        assert len(recipient.inbox) == 0  # Should be empty after processing

class TestExecutiveAgents:
    """Test executive AI agents."""
    
    @pytest.mark.asyncio
    async def test_ceo_decision_making(self):
        """Test CEO decision-making process."""
        ceo = CEOAgent()
        
        decision_context = {
            "proposal": "Launch new product",
            "investment": "$1M",
            "timeline": "6 months",
            "expected_roi": "200%"
        }
        
        decision = await ceo.make_strategic_decision(decision_context)
        
        assert "decision_id" in decision
        assert "decision" in decision
        assert "rationale" in decision
        assert "next_steps" in decision
        assert "success_metrics" in decision
        assert decision["context"] == decision_context
    
    @pytest.mark.asyncio
    async def test_cto_technology_evaluation(self):
        """Test CTO technology evaluation."""
        cto = CTOAgent()
        
        tech_proposal = {
            "name": "New Framework",
            "use_case": "Web development",
            "benefits": ["Faster development", "Better performance"]
        }
        
        evaluation = await cto.evaluate_technology(tech_proposal)
        
        assert "technology" in evaluation
        assert "technical_assessment" in evaluation
        assert "cost_analysis" in evaluation
        assert "risk_assessment" in evaluation
        assert "recommendation" in evaluation
        assert evaluation["technology"] == "New Framework"

class TestProductDevelopmentAgents:
    """Test product development AI agents."""
    
    @pytest.mark.asyncio
    async def test_product_manager_requirements(self):
        """Test Product Manager requirements creation."""
        pm = ProductManagerAgent()
        
        product_idea = {
            "name": "Test Product",
            "description": "A test product for validation",
            "target_market": "Developers"
        }
        
        prd = await pm.create_product_requirements(product_idea)
        
        assert "product_name" in prd
        assert "overview" in prd
        assert "user_personas" in prd
        assert "user_stories" in prd
        assert "functional_requirements" in prd
        assert prd["product_name"] == "Test Product"
        assert len(prd["user_stories"]) > 0

class TestCommunicationSystem:
    """Test the communication and coordination system."""
    
    def test_project_creation(self):
        """Test project creation."""
        project_data = {
            "name": "Test Project",
            "description": "A test project",
            "owner": "pm_001",
            "priority": "high",
            "start_date": datetime.now().isoformat(),
            "target_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "stakeholders": ["ceo_001", "cto_001"]
        }
        
        project = project_manager.create_project(project_data)
        
        assert project.name == "Test Project"
        assert project.status == ProjectStatus.PLANNING
        assert project.owner == "pm_001"
        assert len(project.stakeholders) == 2
        assert project.id in project_manager.projects
    
    @pytest.mark.asyncio
    async def test_task_creation(self):
        """Test task creation and assignment."""
        # First create a project
        project_data = {
            "name": "Task Test Project",
            "description": "Project for testing tasks",
            "owner": "pm_001",
            "priority": "medium",
            "start_date": datetime.now().isoformat(),
            "target_date": (datetime.now() + timedelta(days=30)).isoformat()
        }
        
        project = project_manager.create_project(project_data)
        
        # Create task template
        task_template = {
            "title": "Test Task",
            "description": "A test task",
            "assigned_to": "dev_001",
            "priority": "high",
            "duration_days": 5
        }
        
        task = await project_manager.create_task_from_template(project.id, task_template)
        
        assert task.title == "Test Task"
        assert task.assigned_to == "dev_001"
        assert task.id in project_manager.tasks
        assert task.id in project.tasks

class TestWorkflowEngine:
    """Test the workflow engine."""
    
    def test_workflow_registration(self):
        """Test workflow registration."""
        from core.communication_system import Workflow
        
        workflow = Workflow(
            id="test_workflow_001",
            name="Test Workflow",
            description="A test workflow",
            steps=[
                {
                    "type": "send_message",
                    "sender": "test_sender",
                    "recipient": "test_recipient",
                    "message_type": "task_assignment",
                    "content": {"task": "Test task"}
                }
            ],
            triggers=["test_trigger"],
            conditions=["test_condition"],
            outputs=["test_output"],
            created_by="test_user",
            created_at=datetime.now()
        )
        
        workflow_engine.register_workflow(workflow)
        
        assert workflow.id in workflow_engine.workflows
        assert workflow_engine.workflows[workflow.id].name == "Test Workflow"

class TestIntegration:
    """Integration tests for the complete system."""
    
    @pytest.mark.asyncio
    async def test_agent_communication_flow(self):
        """Test complete communication flow between agents."""
        # Create agents
        ceo = CEOAgent()
        pm = ProductManagerAgent()
        
        # Register agents
        communication_hub.register_agent(ceo)
        communication_hub.register_agent(pm)
        
        # CEO sends task to PM
        await ceo.send_message(
            recipient="pm_001",
            message_type=MessageType.TASK_ASSIGNMENT,
            content={
                "task": "Create product requirements",
                "deadline": (datetime.now() + timedelta(days=7)).isoformat()
            },
            priority=Priority.HIGH,
            requires_response=True
        )
        
        # Process messages
        await pm.process_messages()
        
        # Verify task was received
        assert len(pm.tasks) == 1
        assert pm.tasks[0].title == "Create product requirements"
    
    def test_company_status(self):
        """Test overall company status reporting."""
        # Clear existing agents
        communication_hub.agents.clear()
        
        # Add test agents
        agents = [
            BaseAIAgent("test_001", AgentRole.CEO, "Test CEO"),
            BaseAIAgent("test_002", AgentRole.CTO, "Test CTO"),
            BaseAIAgent("test_003", AgentRole.PRODUCT_MANAGER, "Test PM")
        ]
        
        for agent in agents:
            communication_hub.register_agent(agent)
        
        status = communication_hub.get_company_status()
        
        assert status["total_agents"] == 3
        assert status["active_agents"] == 3
        assert len(status["agents"]) == 3

# Test fixtures and utilities
@pytest.fixture
def sample_agent():
    """Create a sample agent for testing."""
    return BaseAIAgent("sample_001", AgentRole.CEO, "Sample Agent")

@pytest.fixture
def sample_project_data():
    """Create sample project data for testing."""
    return {
        "name": "Sample Project",
        "description": "A sample project for testing",
        "owner": "pm_001",
        "priority": "medium",
        "start_date": datetime.now().isoformat(),
        "target_date": (datetime.now() + timedelta(days=30)).isoformat(),
        "stakeholders": ["ceo_001", "cto_001", "pm_001"]
    }

# Performance tests
class TestPerformance:
    """Performance tests for the system."""
    
    @pytest.mark.asyncio
    async def test_message_processing_performance(self):
        """Test message processing performance."""
        agent = BaseAIAgent("perf_test_001", AgentRole.CEO, "Performance Test Agent")
        
        # Add multiple messages
        start_time = datetime.now()
        
        for i in range(100):
            message = Message(
                id=f"msg_{i}",
                sender="test_sender",
                recipient="perf_test_001",
                message_type=MessageType.STATUS_UPDATE,
                content={"update": f"Status update {i}"},
                priority=Priority.MEDIUM,
                timestamp=datetime.now()
            )
            agent.inbox.append(message)
        
        # Process all messages
        await agent.process_messages()
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        # Should process 100 messages in less than 1 second
        assert processing_time < 1.0
        assert len(agent.inbox) == 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
