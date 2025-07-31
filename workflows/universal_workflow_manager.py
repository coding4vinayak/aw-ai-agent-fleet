"""
Universal Business Workflow Manager
Handles any type of business workflow - restaurants, software, manufacturing, etc.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
import os
import uuid

class UniversalWorkflowManager:
    def __init__(self):
        self.workflow_templates = self._load_workflow_templates()
        
    def _load_workflow_templates(self) -> Dict[str, Any]:
        """Load predefined workflow templates for different business types"""
        return {
            "tea_brand_india": {
                "name": "Tea Brand Launch (India)",
                "description": "Complete workflow to establish tea brand in Indian market",
                "industry": "Food & Beverage",
                "duration_weeks": 48,
                "phases": [
                    {
                        "name": "Market Research & Analysis",
                        "duration_weeks": 4,
                        "agents": ["market_researcher", "business_analyst", "finance_analyst"],
                        "tasks": [
                            {"title": "Market Size Analysis", "agent": "market_researcher", "hours": 40},
                            {"title": "Competitor Research", "agent": "market_researcher", "hours": 32},
                            {"title": "Business Plan", "agent": "business_analyst", "hours": 60},
                            {"title": "Financial Projections", "agent": "finance_analyst", "hours": 24}
                        ]
                    },
                    {
                        "name": "Product Development",
                        "duration_weeks": 6,
                        "agents": ["product_manager", "supply_chain_manager", "quality_manager"],
                        "tasks": [
                            {"title": "Tea Sourcing Strategy", "agent": "supply_chain_manager", "hours": 48},
                            {"title": "Blend Development", "agent": "product_manager", "hours": 56},
                            {"title": "Quality Standards", "agent": "quality_manager", "hours": 32},
                            {"title": "Packaging Design", "agent": "product_manager", "hours": 40}
                        ]
                    }
                ]
            },
            
            "restaurant_launch": {
                "name": "Restaurant Launch",
                "description": "Complete workflow to open a new restaurant",
                "industry": "Food Service",
                "duration_weeks": 32,
                "phases": [
                    {
                        "name": "Concept & Planning",
                        "duration_weeks": 6,
                        "agents": ["business_analyst", "chef", "interior_designer"],
                        "tasks": [
                            {"title": "Market Research", "agent": "business_analyst", "hours": 40},
                            {"title": "Menu Development", "agent": "chef", "hours": 60},
                            {"title": "Restaurant Design", "agent": "interior_designer", "hours": 80},
                            {"title": "Financial Planning", "agent": "business_analyst", "hours": 32}
                        ]
                    },
                    {
                        "name": "Legal & Permits",
                        "duration_weeks": 8,
                        "agents": ["legal_advisor", "compliance_manager"],
                        "tasks": [
                            {"title": "Business License", "agent": "legal_advisor", "hours": 16},
                            {"title": "Food License", "agent": "compliance_manager", "hours": 24},
                            {"title": "Liquor License", "agent": "legal_advisor", "hours": 32},
                            {"title": "Fire Safety Clearance", "agent": "compliance_manager", "hours": 16}
                        ]
                    },
                    {
                        "name": "Setup & Launch",
                        "duration_weeks": 12,
                        "agents": ["operations_manager", "marketing_manager", "chef"],
                        "tasks": [
                            {"title": "Kitchen Setup", "agent": "operations_manager", "hours": 120},
                            {"title": "Staff Hiring", "agent": "operations_manager", "hours": 80},
                            {"title": "Marketing Campaign", "agent": "marketing_manager", "hours": 60},
                            {"title": "Soft Opening", "agent": "chef", "hours": 40}
                        ]
                    }
                ]
            },
            
            "saas_product_launch": {
                "name": "SaaS Product Launch",
                "description": "Complete workflow to develop and launch SaaS product",
                "industry": "Technology",
                "duration_weeks": 40,
                "phases": [
                    {
                        "name": "Product Planning",
                        "duration_weeks": 8,
                        "agents": ["product_manager", "ux_designer", "market_researcher"],
                        "tasks": [
                            {"title": "Market Validation", "agent": "market_researcher", "hours": 60},
                            {"title": "Product Requirements", "agent": "product_manager", "hours": 80},
                            {"title": "User Experience Design", "agent": "ux_designer", "hours": 120},
                            {"title": "Technical Architecture", "agent": "product_manager", "hours": 40}
                        ]
                    },
                    {
                        "name": "Development",
                        "duration_weeks": 20,
                        "agents": ["senior_engineer", "frontend_developer", "backend_developer"],
                        "tasks": [
                            {"title": "Backend Development", "agent": "backend_developer", "hours": 320},
                            {"title": "Frontend Development", "agent": "frontend_developer", "hours": 280},
                            {"title": "API Integration", "agent": "senior_engineer", "hours": 160},
                            {"title": "Testing & QA", "agent": "senior_engineer", "hours": 120}
                        ]
                    },
                    {
                        "name": "Launch & Marketing",
                        "duration_weeks": 12,
                        "agents": ["marketing_manager", "sales_manager", "customer_success"],
                        "tasks": [
                            {"title": "Go-to-Market Strategy", "agent": "marketing_manager", "hours": 80},
                            {"title": "Sales Process Setup", "agent": "sales_manager", "hours": 60},
                            {"title": "Customer Onboarding", "agent": "customer_success", "hours": 40},
                            {"title": "Launch Campaign", "agent": "marketing_manager", "hours": 100}
                        ]
                    }
                ]
            },
            
            "manufacturing_setup": {
                "name": "Manufacturing Unit Setup",
                "description": "Complete workflow to establish manufacturing facility",
                "industry": "Manufacturing",
                "duration_weeks": 52,
                "phases": [
                    {
                        "name": "Feasibility & Planning",
                        "duration_weeks": 12,
                        "agents": ["industrial_engineer", "business_analyst", "finance_analyst"],
                        "tasks": [
                            {"title": "Feasibility Study", "agent": "industrial_engineer", "hours": 80},
                            {"title": "Location Analysis", "agent": "business_analyst", "hours": 60},
                            {"title": "Investment Planning", "agent": "finance_analyst", "hours": 40},
                            {"title": "Technology Selection", "agent": "industrial_engineer", "hours": 100}
                        ]
                    },
                    {
                        "name": "Legal & Approvals",
                        "duration_weeks": 16,
                        "agents": ["legal_advisor", "compliance_manager", "environmental_consultant"],
                        "tasks": [
                            {"title": "Industrial License", "agent": "legal_advisor", "hours": 32},
                            {"title": "Environmental Clearance", "agent": "environmental_consultant", "hours": 80},
                            {"title": "Pollution Control Board", "agent": "compliance_manager", "hours": 40},
                            {"title": "Factory License", "agent": "legal_advisor", "hours": 24}
                        ]
                    },
                    {
                        "name": "Setup & Operations",
                        "duration_weeks": 24,
                        "agents": ["operations_manager", "quality_manager", "safety_manager"],
                        "tasks": [
                            {"title": "Facility Construction", "agent": "operations_manager", "hours": 200},
                            {"title": "Equipment Installation", "agent": "operations_manager", "hours": 160},
                            {"title": "Quality Systems", "agent": "quality_manager", "hours": 80},
                            {"title": "Safety Protocols", "agent": "safety_manager", "hours": 60}
                        ]
                    }
                ]
            },
            
            "ecommerce_store": {
                "name": "E-commerce Store Launch",
                "description": "Complete workflow to launch online store",
                "industry": "E-commerce",
                "duration_weeks": 24,
                "phases": [
                    {
                        "name": "Planning & Strategy",
                        "duration_weeks": 6,
                        "agents": ["business_analyst", "market_researcher", "product_manager"],
                        "tasks": [
                            {"title": "Market Research", "agent": "market_researcher", "hours": 40},
                            {"title": "Product Selection", "agent": "product_manager", "hours": 60},
                            {"title": "Business Model", "agent": "business_analyst", "hours": 32},
                            {"title": "Competitive Analysis", "agent": "market_researcher", "hours": 24}
                        ]
                    },
                    {
                        "name": "Platform Development",
                        "duration_weeks": 10,
                        "agents": ["web_developer", "ux_designer", "payment_specialist"],
                        "tasks": [
                            {"title": "Website Development", "agent": "web_developer", "hours": 120},
                            {"title": "User Experience Design", "agent": "ux_designer", "hours": 80},
                            {"title": "Payment Integration", "agent": "payment_specialist", "hours": 40},
                            {"title": "Mobile Optimization", "agent": "web_developer", "hours": 60}
                        ]
                    },
                    {
                        "name": "Launch & Marketing",
                        "duration_weeks": 8,
                        "agents": ["digital_marketer", "content_creator", "seo_specialist"],
                        "tasks": [
                            {"title": "SEO Optimization", "agent": "seo_specialist", "hours": 60},
                            {"title": "Content Creation", "agent": "content_creator", "hours": 80},
                            {"title": "Digital Marketing", "agent": "digital_marketer", "hours": 100},
                            {"title": "Launch Campaign", "agent": "digital_marketer", "hours": 40}
                        ]
                    }
                ]
            }
        }
    
    def create_custom_workflow(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a custom workflow from user input"""
        workflow_id = str(uuid.uuid4())
        
        workflow = {
            "workflow_id": workflow_id,
            "name": workflow_data.get("name", "Custom Workflow"),
            "description": workflow_data.get("description", ""),
            "industry": workflow_data.get("industry", "General"),
            "created_date": datetime.now().isoformat(),
            "status": "created",
            "phases": workflow_data.get("phases", []),
            "total_duration_weeks": sum(phase.get("duration_weeks", 0) for phase in workflow_data.get("phases", [])),
            "total_tasks": sum(len(phase.get("tasks", [])) for phase in workflow_data.get("phases", []))
        }
        
        # Save workflow
        os.makedirs("data/workflows", exist_ok=True)
        with open(f"data/workflows/{workflow_id}.json", 'w') as f:
            json.dump(workflow, f, indent=2)
        
        return {
            "success": True,
            "workflow_id": workflow_id,
            "message": f"Custom workflow '{workflow['name']}' created successfully",
            "workflow": workflow
        }
    
    def start_workflow_from_template(self, template_name: str, customizations: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Start a workflow from a predefined template"""
        if template_name not in self.workflow_templates:
            return {"success": False, "error": f"Template '{template_name}' not found"}
        
        template = self.workflow_templates[template_name].copy()
        workflow_id = str(uuid.uuid4())
        
        # Apply customizations if provided
        if customizations:
            template.update(customizations)
        
        workflow = {
            "workflow_id": workflow_id,
            "template_name": template_name,
            "name": template["name"],
            "description": template["description"],
            "industry": template["industry"],
            "created_date": datetime.now().isoformat(),
            "start_date": datetime.now().isoformat(),
            "status": "active",
            "current_phase": 1,
            "phases": template["phases"],
            "total_duration_weeks": template["duration_weeks"],
            "estimated_completion": (datetime.now() + timedelta(weeks=template["duration_weeks"])).isoformat(),
            "total_tasks": sum(len(phase.get("tasks", [])) for phase in template["phases"])
        }
        
        # Save workflow
        os.makedirs("data/workflows", exist_ok=True)
        with open(f"data/workflows/{workflow_id}.json", 'w') as f:
            json.dump(workflow, f, indent=2)
        
        return {
            "success": True,
            "workflow_id": workflow_id,
            "message": f"Workflow '{workflow['name']}' started successfully",
            "workflow": workflow
        }
    
    def get_available_templates(self) -> List[Dict[str, Any]]:
        """Get list of available workflow templates"""
        templates = []
        for template_id, template in self.workflow_templates.items():
            templates.append({
                "template_id": template_id,
                "name": template["name"],
                "description": template["description"],
                "industry": template["industry"],
                "duration_weeks": template["duration_weeks"],
                "total_phases": len(template["phases"]),
                "total_tasks": sum(len(phase.get("tasks", [])) for phase in template["phases"])
            })
        return templates
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get current status of any workflow"""
        try:
            with open(f"data/workflows/{workflow_id}.json", 'r') as f:
                workflow = json.load(f)
            
            # Calculate progress
            total_tasks = workflow.get("total_tasks", 0)
            completed_tasks = 0  # In real implementation, track completed tasks
            
            return {
                "workflow_id": workflow_id,
                "name": workflow["name"],
                "industry": workflow["industry"],
                "status": workflow["status"],
                "current_phase": workflow.get("current_phase", 1),
                "total_phases": len(workflow["phases"]),
                "progress_percentage": round((completed_tasks / total_tasks) * 100, 2) if total_tasks > 0 else 0,
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "start_date": workflow.get("start_date"),
                "estimated_completion": workflow.get("estimated_completion")
            }
        except FileNotFoundError:
            return {"error": "Workflow not found"}
    
    def get_current_phase_tasks(self, workflow_id: str) -> List[Dict[str, Any]]:
        """Get tasks for current phase of any workflow"""
        try:
            with open(f"data/workflows/{workflow_id}.json", 'r') as f:
                workflow = json.load(f)
            
            current_phase = workflow.get("current_phase", 1)
            if current_phase <= len(workflow["phases"]):
                phase = workflow["phases"][current_phase - 1]
                return phase.get("tasks", [])
            return []
        except FileNotFoundError:
            return []
    
    def assign_task_to_agent(self, workflow_id: str, task_id: str, agent_id: str) -> Dict[str, Any]:
        """Assign a task to an AI agent"""
        try:
            with open(f"data/workflows/{workflow_id}.json", 'r') as f:
                workflow = json.load(f)
            
            # Find and update task
            for phase in workflow["phases"]:
                for task in phase.get("tasks", []):
                    if task.get("task_id") == task_id or task.get("title") == task_id:
                        task["assigned_agent"] = agent_id
                        task["assigned_date"] = datetime.now().isoformat()
                        task["status"] = "assigned"
                        break
            
            # Save updated workflow
            with open(f"data/workflows/{workflow_id}.json", 'w') as f:
                json.dump(workflow, f, indent=2)
            
            return {
                "success": True,
                "message": f"Task assigned to agent {agent_id}",
                "workflow_id": workflow_id,
                "task_id": task_id,
                "agent_id": agent_id
            }
        except FileNotFoundError:
            return {"success": False, "error": "Workflow not found"}
