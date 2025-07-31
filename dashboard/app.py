"""
AI Company Dashboard
Web interface for monitoring all AI agents and their work.
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import json
from typing import Dict, List, Any

from core.agent_framework import communication_hub
from core.communication_system import project_manager, standup_manager, performance_monitor
from core.task_coordinator import task_coordinator
from core.llm_integration import llm_manager
from core.data_manager import data_manager
from config.settings import settings, LLMConfig, LLMProvider, AgentConfig, IntegrationConfig

app = Flask(__name__)

@app.route('/')
def dashboard():
    """Main dashboard page."""
    return render_template('dashboard.html')

@app.route('/tasks')
def task_interface():
    """Task assignment interface page."""
    return render_template('task_interface.html')

@app.route('/settings')
def settings_interface():
    """Settings management interface page."""
    return render_template('settings.html')

@app.route('/workflows')
def workflow_manager_interface():
    """Universal workflow manager interface page."""
    return render_template('workflow_manager.html')

@app.route('/api/settings/llm-configs')
def get_llm_configs():
    """Get all LLM configurations."""
    try:
        configs = {}
        for name, config in settings.llm_configs.items():
            configs[name] = {
                "provider": config.provider.value,
                "model_name": config.model_name,
                "temperature": config.temperature,
                "max_tokens": config.max_tokens,
                "timeout": config.timeout,
                "has_api_key": bool(config.api_key)
            }
        return jsonify({"configs": configs})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/settings/llm-configs', methods=['POST'])
def add_llm_config():
    """Add new LLM configuration."""
    try:
        data = request.json
        config = LLMConfig(
            provider=LLMProvider(data['provider']),
            model_name=data['model_name'],
            api_key=data.get('api_key'),
            api_base=data.get('api_base'),
            temperature=data.get('temperature', 0.7),
            max_tokens=data.get('max_tokens', 4000),
            timeout=data.get('timeout', 30)
        )

        settings.add_llm_config(data['name'], config)
        return jsonify({"success": True, "message": "LLM config added successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/settings/test-llm/<config_name>')
async def test_llm_config(config_name):
    """Test LLM configuration."""
    try:
        result = await llm_manager.test_connection(config_name)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/agents')
def agents_management():
    """Agent management interface."""
    return render_template('agents.html')

@app.route('/templates')
def templates_interface():
    """Template selection interface."""
    return render_template('templates.html')

@app.route('/api/agents')
def get_agents():
    """Get all configured agents."""
    try:
        agents = []

        # If no agents configured, create some test agents
        if not settings.agent_configs:
            from config.settings import AgentConfig

            # Create test agents
            test_agents = [
                AgentConfig(
                    agent_id="test_ceo_001",
                    name="Sarah Chen - CEO",
                    role="startup_ceo",
                    llm_config="openai_gpt4",
                    temperature=0.7,
                    memory_enabled=True,
                    tools_enabled=["web_search", "calculator"]
                ),
                AgentConfig(
                    agent_id="test_engineer_001",
                    name="Alex Rodriguez - Senior Engineer",
                    role="senior_engineer",
                    llm_config="openai_gpt4",
                    temperature=0.6,
                    memory_enabled=True,
                    tools_enabled=["web_search", "code_analysis"]
                ),
                AgentConfig(
                    agent_id="test_designer_001",
                    name="Maya Patel - UI Designer",
                    role="ui_designer",
                    llm_config="openai_gpt4",
                    temperature=0.8,
                    memory_enabled=True,
                    tools_enabled=["web_search", "design_tools"]
                )
            ]

            for config in test_agents:
                settings.add_agent_config(config)

        for agent_id, config in settings.agent_configs.items():
            agents.append({
                "id": agent_id,
                "name": config.name,
                "role": config.role,
                "llm_config": config.llm_config,
                "temperature": config.temperature,
                "memory_enabled": config.memory_enabled,
                "tools_enabled": config.tools_enabled if hasattr(config, 'tools_enabled') else [],
                "status": "active"
            })
        return jsonify({"agents": agents})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/templates/agents')
def get_agent_templates():
    """Get all available agent templates."""
    try:
        from templates.agent_templates import agent_templates

        categories = agent_templates.get_templates_by_category()
        templates = {}

        for category, template_list in categories.items():
            templates[category] = []
            for template_name in template_list:
                try:
                    template = agent_templates.get_template(template_name)
                    templates[category].append({
                        "id": template_name,
                        "name": template["name"],
                        "role": template["role"],
                        "description": template["system_prompt"][:200] + "...",
                        "temperature": template["temperature"],
                        "tools": template["tools_enabled"]
                    })
                except Exception as e:
                    print(f"Error loading template {template_name}: {e}")

        return jsonify({"templates": templates})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/templates/scenarios')
def get_business_scenarios():
    """Get all available business scenarios."""
    try:
        from templates.business_scenarios import business_scenarios

        categories = business_scenarios.get_scenarios_by_category()
        scenarios = {}

        for category, scenario_list in categories.items():
            scenarios[category] = []
            for scenario_name in scenario_list:
                try:
                    scenario = business_scenarios.get_scenario(scenario_name)
                    scenarios[category].append({
                        "id": scenario_name,
                        "name": scenario["name"],
                        "description": scenario["description"],
                        "team_size": scenario["team_size"],
                        "agents": [agent["name"] for agent in scenario["agents"]],
                        "common_tasks": scenario.get("common_tasks", [])[:3],
                        "key_metrics": scenario.get("key_metrics", [])[:3]
                    })
                except Exception as e:
                    print(f"Error loading scenario {scenario_name}: {e}")

        return jsonify({"scenarios": scenarios})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/agents/create', methods=['POST'])
def create_agent():
    """Create a new agent from template."""
    try:
        data = request.json
        template_name = data.get('template')
        agent_name = data.get('name')
        custom_name = data.get('custom_name')

        from templates.agent_templates import agent_templates

        # Generate unique agent ID
        import uuid
        agent_id = f"{template_name}_{str(uuid.uuid4())[:8]}"

        # Create agent config from template
        config = agent_templates.create_agent_from_template(
            template_name,
            agent_id,
            custom_name or agent_name
        )

        # Add to settings
        settings.add_agent_config(config)

        return jsonify({
            "success": True,
            "message": f"Agent '{config.name}' created successfully",
            "agent": {
                "id": config.agent_id,
                "name": config.name,
                "role": config.role
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/scenarios/deploy', methods=['POST'])
def deploy_scenario():
    """Deploy a complete business scenario."""
    try:
        data = request.json
        scenario_name = data.get('scenario')
        custom_prefix = data.get('prefix', '')

        from templates.business_scenarios import business_scenarios

        # Create team from scenario
        team_configs = business_scenarios.create_scenario_team(scenario_name, custom_prefix)

        # Add all agents to settings
        created_agents = []
        for team_member in team_configs:
            config = team_member["config"]
            settings.add_agent_config(config)
            created_agents.append({
                "id": config.agent_id,
                "name": config.name,
                "role": config.role
            })

        # Save scenario info
        scenario_info = business_scenarios.get_scenario(scenario_name)

        return jsonify({
            "success": True,
            "message": f"Deployed {scenario_info['name']} with {len(created_agents)} agents",
            "scenario": scenario_info['name'],
            "agents": created_agents
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/assign-user-task', methods=['POST'])
async def assign_user_task():
    """Assign a new task from user input."""
    try:
        task_data = request.json
        task_description = task_data.get('description')
        priority = task_data.get('priority', 'medium')
        deadline = task_data.get('deadline')

        if not task_description:
            return jsonify({"error": "Task description is required"}), 400

        # Process task through coordinator
        result = await task_coordinator.process_user_task(task_description, priority, deadline)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/task-status/<task_id>')
async def get_task_status_api(task_id):
    """Get task status via API."""
    try:
        status = await task_coordinator.get_task_status(task_id)
        return jsonify(status)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/active-tasks')
def get_active_tasks():
    """Get all active tasks."""
    try:
        # Return mock data for now since we don't have async support
        tasks = [
            {
                "id": "task_001",
                "title": "Setup AI Company Infrastructure",
                "status": "in_progress",
                "assigned_to": "System",
                "priority": "high",
                "progress": 85
            },
            {
                "id": "task_002",
                "title": "Deploy Agent Templates",
                "status": "completed",
                "assigned_to": "Template System",
                "priority": "medium",
                "progress": 100
            }
        ]
        return jsonify({"tasks": tasks})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/company-status')
def get_company_status():
    """Get overall company status."""
    try:
        status = communication_hub.get_company_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/api/projects')
def get_projects():
    """Get all projects and their status."""
    try:
        projects = []
        for project_id, project in project_manager.projects.items():
            project_data = {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "status": project.status.value,
                "priority": project.priority.value,
                "owner": project.owner,
                "start_date": project.start_date.isoformat(),
                "target_date": project.target_date.isoformat(),
                "completion_date": project.completion_date.isoformat() if project.completion_date else None,
                "progress": calculate_project_progress(project),
                "task_count": len(project.tasks) if project.tasks else 0,
                "stakeholders": project.stakeholders or []
            }
            projects.append(project_data)
        
        return jsonify({"projects": projects})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks')
def get_tasks():
    """Get all tasks and their status."""
    try:
        tasks = []
        for task_id, task in project_manager.tasks.items():
            task_data = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority.value,
                "assigned_to": task.assigned_to,
                "created_by": task.created_by,
                "deadline": task.deadline.isoformat() if task.deadline else None,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "days_until_deadline": get_days_until_deadline(task.deadline) if task.deadline else None
            }
            tasks.append(task_data)
        
        return jsonify({"tasks": tasks})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/standup-reports')
def get_standup_reports():
    """Get recent standup reports."""
    try:
        # Get last 7 days of standup reports
        reports = []
        for date, report in list(standup_manager.standup_reports.items())[-7:]:
            report_summary = {
                "date": date,
                "participant_count": len(report["participants"]),
                "blocker_count": len(report["blockers"]),
                "action_item_count": len(report["action_items"]),
                "blockers": report["blockers"][:3],  # Show top 3 blockers
                "top_accomplishments": get_top_accomplishments(report["summary"])
            }
            reports.append(report_summary)
        
        return jsonify({"reports": reports})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/performance-metrics')
def get_performance_metrics():
    """Get performance metrics."""
    try:
        # Get latest performance metrics
        latest_metrics = list(performance_monitor.performance_metrics.values())[-1] if performance_monitor.performance_metrics else {}
        
        # Calculate trends
        metrics_with_trends = {
            "current": latest_metrics,
            "trends": calculate_performance_trends(),
            "alerts": performance_monitor.alerts[-10:]  # Last 10 alerts
        }
        
        return jsonify(metrics_with_trends)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/agent/<agent_id>')
def get_agent_details(agent_id):
    """Get detailed information about a specific agent."""
    try:
        agent = communication_hub.agents.get(agent_id)
        if not agent:
            return jsonify({"error": "Agent not found"}), 404
        
        agent_details = {
            "basic_info": agent.get_status(),
            "recent_tasks": get_agent_recent_tasks(agent_id),
            "recent_messages": get_agent_recent_messages(agent_id),
            "performance_metrics": get_agent_performance_metrics(agent_id),
            "collaboration_network": get_agent_collaboration_network(agent_id)
        }
        
        return jsonify(agent_details)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/project/<project_id>')
def get_project_details(project_id):
    """Get detailed information about a specific project."""
    try:
        project = project_manager.projects.get(project_id)
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        project_details = {
            "basic_info": {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "status": project.status.value,
                "priority": project.priority.value,
                "owner": project.owner,
                "start_date": project.start_date.isoformat(),
                "target_date": project.target_date.isoformat(),
                "budget": project.budget,
                "stakeholders": project.stakeholders
            },
            "tasks": get_project_tasks(project_id),
            "timeline": generate_project_timeline(project),
            "progress": calculate_detailed_project_progress(project),
            "risks": identify_project_risks(project)
        }
        
        return jsonify(project_details)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/create-project', methods=['POST'])
def create_project():
    """Create a new project."""
    try:
        project_data = request.json
        project = project_manager.create_project(project_data)
        
        return jsonify({
            "success": True,
            "project_id": project.id,
            "message": f"Project '{project.name}' created successfully"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/assign-task', methods=['POST'])
def assign_task():
    """Assign a task to an agent."""
    try:
        task_data = request.json
        task_id = task_data.get('task_id')
        agent_id = task_data.get('agent_id')

        # Update task assignment
        task = project_manager.tasks.get(task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404

        task.assigned_to = agent_id
        task.updated_at = datetime.now()

        # Note: In a real implementation, this would use an async task queue
        # For now, we'll just update the task assignment

        return jsonify({
            "success": True,
            "message": f"Task assigned to {agent_id}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Helper functions
def get_relative_time(timestamp):
    """Get relative time string."""
    if not timestamp:
        return "Unknown"
    
    now = datetime.now()
    diff = now - timestamp
    
    if diff.days > 0:
        return f"{diff.days} days ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hours ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minutes ago"
    else:
        return "Just now"

def calculate_project_progress(project):
    """Calculate project progress percentage."""
    if not project.tasks:
        return 0
    
    completed_tasks = 0
    for task_id in project.tasks:
        task = project_manager.tasks.get(task_id)
        if task and task.status == "completed":
            completed_tasks += 1
    
    return int((completed_tasks / len(project.tasks)) * 100)

def get_days_until_deadline(deadline):
    """Get days until deadline."""
    if not deadline:
        return None
    
    now = datetime.now()
    diff = deadline - now
    return diff.days

def get_top_accomplishments(summary):
    """Extract top accomplishments from standup summary."""
    accomplishments = []
    for agent_id, report in summary.items():
        yesterday = report.get("yesterday", [])
        accomplishments.extend(yesterday[:2])  # Top 2 from each agent
    
    return accomplishments[:5]  # Return top 5 overall

def calculate_performance_trends():
    """Calculate performance trends."""
    # This would analyze historical data to show trends
    return {
        "agent_productivity": "+5%",
        "task_completion_rate": "+2%",
        "response_time": "-10%",
        "collaboration_score": "+8%"
    }

def get_agent_recent_tasks(agent_id):
    """Get recent tasks for an agent."""
    recent_tasks = []
    for task_id, task in project_manager.tasks.items():
        if task.assigned_to == agent_id:
            recent_tasks.append({
                "id": task.id,
                "title": task.title,
                "status": task.status,
                "deadline": task.deadline.isoformat() if task.deadline else None
            })
    
    return recent_tasks[-5:]  # Last 5 tasks

def get_agent_recent_messages(agent_id):
    """Get recent messages for an agent."""
    # This would query message history
    return [
        {"type": "task_assignment", "from": "project_manager", "time": "2 hours ago"},
        {"type": "collaboration_request", "from": "frontend_eng_001", "time": "4 hours ago"},
        {"type": "status_update", "to": "ceo_001", "time": "1 day ago"}
    ]

def get_agent_performance_metrics(agent_id):
    """Get performance metrics for an agent."""
    return {
        "task_completion_rate": "95%",
        "average_response_time": "2.1 seconds",
        "quality_score": "4.3/5.0",
        "collaboration_score": "4.5/5.0",
        "innovation_score": "4.0/5.0"
    }

def get_agent_collaboration_network(agent_id):
    """Get collaboration network for an agent."""
    return [
        {"agent": "product_manager_001", "interactions": 45, "type": "frequent"},
        {"agent": "backend_eng_001", "interactions": 32, "type": "regular"},
        {"agent": "ux_designer_001", "interactions": 18, "type": "occasional"}
    ]

def get_project_tasks(project_id):
    """Get tasks for a project."""
    project = project_manager.projects.get(project_id)
    if not project or not project.tasks:
        return []
    
    tasks = []
    for task_id in project.tasks:
        task = project_manager.tasks.get(task_id)
        if task:
            tasks.append({
                "id": task.id,
                "title": task.title,
                "status": task.status,
                "assigned_to": task.assigned_to,
                "deadline": task.deadline.isoformat() if task.deadline else None
            })
    
    return tasks

def generate_project_timeline(project):
    """Generate project timeline."""
    return {
        "start_date": project.start_date.isoformat(),
        "target_date": project.target_date.isoformat(),
        "milestones": [
            {"name": "Planning Complete", "date": "2024-02-15", "status": "completed"},
            {"name": "Development Start", "date": "2024-02-20", "status": "completed"},
            {"name": "Alpha Release", "date": "2024-03-15", "status": "in_progress"},
            {"name": "Beta Release", "date": "2024-04-01", "status": "pending"},
            {"name": "Production Launch", "date": "2024-04-15", "status": "pending"}
        ]
    }

def calculate_detailed_project_progress(project):
    """Calculate detailed project progress."""
    return {
        "overall": calculate_project_progress(project),
        "by_phase": {
            "planning": 100,
            "development": 65,
            "testing": 30,
            "deployment": 0
        },
        "by_team": {
            "engineering": 70,
            "design": 85,
            "qa": 45,
            "marketing": 20
        }
    }

def identify_project_risks(project):
    """Identify project risks."""
    return [
        {"type": "schedule", "description": "Potential delay in API development", "severity": "medium"},
        {"type": "resource", "description": "Designer availability conflict", "severity": "low"},
        {"type": "technical", "description": "Third-party integration complexity", "severity": "high"}
    ]

@app.route('/api/agents/<agent_id>', methods=['PUT'])
def update_agent(agent_id):
    """Update an agent."""
    try:
        if agent_id not in settings.agent_configs:
            return jsonify({"error": "Agent not found"}), 404

        data = request.json
        config = settings.agent_configs[agent_id]

        # Update the agent configuration
        if 'name' in data:
            config.name = data['name']
        if 'temperature' in data:
            config.temperature = data['temperature']
        if 'memory_enabled' in data:
            config.memory_enabled = data['memory_enabled']

        return jsonify({
            "success": True,
            "message": f"Agent {agent_id} updated successfully"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/agents/<agent_id>', methods=['DELETE'])
def delete_agent(agent_id):
    """Delete an agent."""
    try:
        if agent_id in settings.agent_configs:
            del settings.agent_configs[agent_id]
            return jsonify({
                "success": True,
                "message": f"Agent {agent_id} deleted successfully"
            })
        else:
            return jsonify({"error": "Agent not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Workflow Management Endpoints
@app.route('/api/workflows/tea-brand/start', methods=['POST'])
def start_tea_brand_workflow():
    """Start the tea brand launch workflow"""
    try:
        from workflows.tea_brand_workflow import TeaBrandWorkflowManager

        workflow_manager = TeaBrandWorkflowManager()
        result = workflow_manager.start_workflow()

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/workflows/tea-brand/status/<workflow_id>')
def get_tea_brand_workflow_status(workflow_id):
    """Get tea brand workflow status"""
    try:
        from workflows.tea_brand_workflow import TeaBrandWorkflowManager

        workflow_manager = TeaBrandWorkflowManager()
        workflow_manager.workflow_id = workflow_id
        status = workflow_manager.get_workflow_status()

        return jsonify(status)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/workflows/tea-brand/tasks/<workflow_id>')
def get_tea_brand_current_tasks(workflow_id):
    """Get current phase tasks for tea brand workflow"""
    try:
        from workflows.tea_brand_workflow import TeaBrandWorkflowManager

        workflow_manager = TeaBrandWorkflowManager()
        workflow_manager.workflow_id = workflow_id
        tasks = workflow_manager.get_current_phase_tasks()

        return jsonify({"tasks": tasks})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks/execute', methods=['POST'])
def execute_task():
    """Execute a task using AI agent"""
    try:
        from managers.task_execution_manager import TaskExecutionManager
        import asyncio

        data = request.json
        task_id = data.get('task_id')
        agent_id = data.get('agent_id')
        task_details = data.get('task_details')

        if not all([task_id, agent_id, task_details]):
            return jsonify({"error": "Missing required fields"}), 400

        task_manager = TaskExecutionManager()

        # Run async task execution
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            task_manager.execute_task(task_id, agent_id, task_details)
        )
        loop.close()

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks/reports')
def get_all_task_reports():
    """Get all generated task reports"""
    try:
        from managers.task_execution_manager import TaskExecutionManager

        task_manager = TaskExecutionManager()
        reports = task_manager.get_all_reports()

        return jsonify({"reports": reports})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/workflows/tea-brand/report/<workflow_id>/<int:phase_id>')
def get_phase_report(workflow_id, phase_id):
    """Get comprehensive report for a workflow phase"""
    try:
        from workflows.tea_brand_workflow import TeaBrandWorkflowManager

        workflow_manager = TeaBrandWorkflowManager()
        workflow_manager.workflow_id = workflow_id
        report = workflow_manager.generate_phase_report(phase_id)

        return jsonify(report)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Tea Brand Workflow Interface
@app.route('/tea-brand-workflow')
def tea_brand_workflow_interface():
    """Tea brand workflow management interface"""
    return render_template('tea_brand_workflow.html')

# Universal Workflow Management Endpoints
@app.route('/api/workflow-templates')
def get_workflow_templates():
    """Get all available workflow templates"""
    try:
        from workflows.universal_workflow_manager import UniversalWorkflowManager

        workflow_manager = UniversalWorkflowManager()
        templates = workflow_manager.get_available_templates()

        return jsonify({"templates": templates})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/workflows/start-template', methods=['POST'])
def start_workflow_from_template():
    """Start a workflow from template"""
    try:
        from workflows.universal_workflow_manager import UniversalWorkflowManager

        data = request.json
        template_id = data.get('template_id')
        customizations = data.get('customizations', {})

        workflow_manager = UniversalWorkflowManager()
        result = workflow_manager.start_workflow_from_template(template_id, customizations)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/workflows/create-custom', methods=['POST'])
def create_custom_workflow():
    """Create a custom workflow"""
    try:
        from workflows.universal_workflow_manager import UniversalWorkflowManager

        workflow_data = request.json
        workflow_manager = UniversalWorkflowManager()
        result = workflow_manager.create_custom_workflow(workflow_data)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/workflows/<workflow_id>/status')
def get_workflow_status(workflow_id):
    """Get workflow status"""
    try:
        from workflows.universal_workflow_manager import UniversalWorkflowManager

        workflow_manager = UniversalWorkflowManager()
        status = workflow_manager.get_workflow_status(workflow_id)

        return jsonify(status)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/workflows/<workflow_id>/tasks')
def get_workflow_current_tasks(workflow_id):
    """Get current phase tasks for workflow"""
    try:
        from workflows.universal_workflow_manager import UniversalWorkflowManager

        workflow_manager = UniversalWorkflowManager()
        tasks = workflow_manager.get_current_phase_tasks(workflow_id)

        return jsonify({"tasks": tasks})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks/execute-universal', methods=['POST'])
def execute_universal_task():
    """Execute any type of business task using AI agent"""
    try:
        from managers.task_execution_manager import UniversalTaskExecutionManager
        import asyncio

        data = request.json
        task_id = data.get('task_id')
        agent_id = data.get('agent_id')
        task_details = data.get('task_details')

        if not all([task_id, agent_id, task_details]):
            return jsonify({"error": "Missing required fields"}), 400

        task_manager = UniversalTaskExecutionManager()

        # Run async task execution
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            task_manager.execute_task(task_id, agent_id, task_details)
        )
        loop.close()

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/workflows/<workflow_id>/assign-task', methods=['POST'])
def assign_workflow_task():
    """Assign a workflow task to an agent"""
    try:
        from workflows.universal_workflow_manager import UniversalWorkflowManager

        data = request.json
        task_id = data.get('task_id')
        agent_id = data.get('agent_id')

        workflow_manager = UniversalWorkflowManager()
        result = workflow_manager.assign_task_to_agent(workflow_id, task_id, agent_id)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
