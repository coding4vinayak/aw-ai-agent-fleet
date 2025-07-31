"""
Business Scenario Templates
Pre-configured team setups for different business scenarios and use cases.
"""

from typing import Dict, List, Any
from templates.agent_templates import agent_templates

class BusinessScenarioManager:
    """Manager for creating complete teams from business scenario templates."""
    
    def __init__(self):
        self.scenarios = {
            # Startup Scenarios
            "tech_startup": self._tech_startup_scenario,
            "saas_startup": self._saas_startup_scenario,
            "ecommerce_startup": self._ecommerce_startup_scenario,
            "fintech_startup": self._fintech_startup_scenario,
            "healthtech_startup": self._healthtech_startup_scenario,
            
            # Product Development Scenarios
            "mobile_app_development": self._mobile_app_development_scenario,
            "web_platform_development": self._web_platform_development_scenario,
            "ai_product_development": self._ai_product_development_scenario,
            "enterprise_software": self._enterprise_software_scenario,
            
            # Marketing Scenarios
            "product_launch": self._product_launch_scenario,
            "digital_marketing_campaign": self._digital_marketing_campaign_scenario,
            "content_marketing": self._content_marketing_scenario,
            "growth_hacking": self._growth_hacking_scenario,
            
            # Enterprise Scenarios
            "digital_transformation": self._digital_transformation_scenario,
            "merger_acquisition": self._merger_acquisition_scenario,
            "international_expansion": self._international_expansion_scenario,
            "cost_optimization": self._cost_optimization_scenario,
            
            # Specialized Scenarios
            "ai_research_lab": self._ai_research_lab_scenario,
            "cybersecurity_team": self._cybersecurity_team_scenario,
            "data_analytics_team": self._data_analytics_team_scenario,
            "consulting_firm": self._consulting_firm_scenario,
        }
    
    def get_scenario(self, scenario_name: str) -> Dict[str, Any]:
        """Get complete team configuration from scenario."""
        if scenario_name not in self.scenarios:
            raise ValueError(f"Scenario '{scenario_name}' not found")
        
        return self.scenarios[scenario_name]()
    
    def list_scenarios(self) -> List[str]:
        """List all available scenarios."""
        return list(self.scenarios.keys())
    
    def get_scenarios_by_category(self) -> Dict[str, List[str]]:
        """Get scenarios organized by category."""
        return {
            "Startup": [
                "tech_startup", "saas_startup", "ecommerce_startup", 
                "fintech_startup", "healthtech_startup"
            ],
            "Product Development": [
                "mobile_app_development", "web_platform_development",
                "ai_product_development", "enterprise_software"
            ],
            "Marketing": [
                "product_launch", "digital_marketing_campaign",
                "content_marketing", "growth_hacking"
            ],
            "Enterprise": [
                "digital_transformation", "merger_acquisition",
                "international_expansion", "cost_optimization"
            ],
            "Specialized": [
                "ai_research_lab", "cybersecurity_team",
                "data_analytics_team", "consulting_firm"
            ]
        }
    
    # Startup Scenarios
    def _tech_startup_scenario(self) -> Dict[str, Any]:
        return {
            "name": "Tech Startup Team",
            "description": "Complete team for a technology startup from MVP to Series A",
            "team_size": 8,
            "agents": [
                {
                    "template": "startup_ceo",
                    "agent_id": "startup_ceo_001",
                    "name": "Alex Chen - Startup CEO"
                },
                {
                    "template": "tech_cto",
                    "agent_id": "startup_cto_001", 
                    "name": "Sarah Kim - Startup CTO"
                },
                {
                    "template": "product_manager",
                    "agent_id": "startup_pm_001",
                    "name": "Emma Thompson - Product Manager"
                },
                {
                    "template": "senior_engineer",
                    "agent_id": "startup_eng_001",
                    "name": "David Park - Lead Engineer"
                },
                {
                    "template": "frontend_specialist",
                    "agent_id": "startup_frontend_001",
                    "name": "Lisa Wang - Frontend Engineer"
                },
                {
                    "template": "digital_marketer",
                    "agent_id": "startup_marketing_001",
                    "name": "Rachel Green - Growth Marketer"
                },
                {
                    "template": "ux_researcher",
                    "agent_id": "startup_ux_001",
                    "name": "Jordan Smith - UX Designer"
                },
                {
                    "template": "business_analyst",
                    "agent_id": "startup_analyst_001",
                    "name": "Maya Patel - Business Analyst"
                }
            ],
            "common_tasks": [
                "Validate product-market fit for our MVP",
                "Create pitch deck for Series A fundraising",
                "Develop go-to-market strategy for new product",
                "Build scalable technical architecture",
                "Design user acquisition strategy"
            ],
            "key_metrics": [
                "Monthly Recurring Revenue (MRR)",
                "Customer Acquisition Cost (CAC)",
                "Product-Market Fit Score",
                "User Engagement Rate",
                "Burn Rate and Runway"
            ]
        }
    
    def _saas_startup_scenario(self) -> Dict[str, Any]:
        return {
            "name": "SaaS Startup Team",
            "description": "Specialized team for Software-as-a-Service startup",
            "team_size": 10,
            "agents": [
                {
                    "template": "startup_ceo",
                    "agent_id": "saas_ceo_001",
                    "name": "Alex Rodriguez - SaaS CEO"
                },
                {
                    "template": "tech_cto",
                    "agent_id": "saas_cto_001",
                    "name": "Priya Sharma - SaaS CTO"
                },
                {
                    "template": "product_manager",
                    "agent_id": "saas_pm_001",
                    "name": "Marcus Johnson - Product Manager"
                },
                {
                    "template": "backend_specialist",
                    "agent_id": "saas_backend_001",
                    "name": "Jennifer Liu - Backend Engineer"
                },
                {
                    "template": "frontend_specialist",
                    "agent_id": "saas_frontend_001",
                    "name": "Carlos Silva - Frontend Engineer"
                },
                {
                    "template": "cloud_architect",
                    "agent_id": "saas_cloud_001",
                    "name": "Maria Garcia - Cloud Architect"
                },
                {
                    "template": "digital_marketer",
                    "agent_id": "saas_marketing_001",
                    "name": "Kevin Liu - Growth Marketer"
                },
                {
                    "template": "sales_director",
                    "agent_id": "saas_sales_001",
                    "name": "Amanda Foster - Sales Director"
                },
                {
                    "template": "customer_success",
                    "agent_id": "saas_cs_001",
                    "name": "Nicole Davis - Customer Success"
                },
                {
                    "template": "data_scientist",
                    "agent_id": "saas_data_001",
                    "name": "Tyler Johnson - Data Analyst"
                }
            ],
            "common_tasks": [
                "Optimize SaaS metrics and reduce churn",
                "Build scalable multi-tenant architecture",
                "Create freemium to paid conversion strategy",
                "Implement customer success automation",
                "Design enterprise sales process"
            ],
            "key_metrics": [
                "Monthly Recurring Revenue (MRR)",
                "Churn Rate",
                "Customer Lifetime Value (CLV)",
                "Net Promoter Score (NPS)",
                "Annual Contract Value (ACV)"
            ]
        }
    
    # Product Development Scenarios
    def _mobile_app_development_scenario(self) -> Dict[str, Any]:
        return {
            "name": "Mobile App Development Team",
            "description": "Complete team for mobile app development (iOS & Android)",
            "team_size": 7,
            "agents": [
                {
                    "template": "product_manager",
                    "agent_id": "mobile_pm_001",
                    "name": "Emma Chen - Mobile Product Manager"
                },
                {
                    "template": "mobile_developer",
                    "agent_id": "mobile_ios_001",
                    "name": "David Kim - iOS Developer"
                },
                {
                    "template": "mobile_developer",
                    "agent_id": "mobile_android_001",
                    "name": "Sarah Park - Android Developer"
                },
                {
                    "template": "backend_specialist",
                    "agent_id": "mobile_backend_001",
                    "name": "Alex Thompson - Backend Engineer"
                },
                {
                    "template": "ui_designer",
                    "agent_id": "mobile_ui_001",
                    "name": "Lisa Rodriguez - UI Designer"
                },
                {
                    "template": "ux_researcher",
                    "agent_id": "mobile_ux_001",
                    "name": "Jordan Martinez - UX Researcher"
                },
                {
                    "template": "qa_specialist",
                    "agent_id": "mobile_qa_001",
                    "name": "Maya Singh - QA Engineer"
                }
            ],
            "common_tasks": [
                "Design mobile app user experience and interface",
                "Develop native iOS and Android applications",
                "Create backend API for mobile app",
                "Implement app store optimization strategy",
                "Set up mobile analytics and crash reporting"
            ],
            "key_metrics": [
                "App Store Rating",
                "Download Rate",
                "Daily/Monthly Active Users",
                "Session Duration",
                "Crash Rate"
            ]
        }
    
    def _ai_product_development_scenario(self) -> Dict[str, Any]:
        return {
            "name": "AI Product Development Team",
            "description": "Specialized team for AI/ML product development",
            "team_size": 8,
            "agents": [
                {
                    "template": "product_manager",
                    "agent_id": "ai_pm_001",
                    "name": "Dr. Priya Chen - AI Product Manager"
                },
                {
                    "template": "ai_researcher",
                    "agent_id": "ai_researcher_001",
                    "name": "Dr. Marcus Liu - AI Researcher"
                },
                {
                    "template": "data_scientist",
                    "agent_id": "ai_ds_001",
                    "name": "Jennifer Park - Data Scientist"
                },
                {
                    "template": "senior_engineer",
                    "agent_id": "ai_eng_001",
                    "name": "Alex Rodriguez - ML Engineer"
                },
                {
                    "template": "backend_specialist",
                    "agent_id": "ai_backend_001",
                    "name": "Sarah Kim - Backend Engineer"
                },
                {
                    "template": "cloud_architect",
                    "agent_id": "ai_cloud_001",
                    "name": "David Thompson - ML Infrastructure"
                },
                {
                    "template": "ux_researcher",
                    "agent_id": "ai_ux_001",
                    "name": "Emma Martinez - AI UX Designer"
                },
                {
                    "template": "business_analyst",
                    "agent_id": "ai_analyst_001",
                    "name": "Lisa Wang - AI Business Analyst"
                }
            ],
            "common_tasks": [
                "Develop machine learning models for product features",
                "Create AI-powered user experiences",
                "Build scalable ML infrastructure and pipelines",
                "Implement responsible AI practices and ethics",
                "Design AI product strategy and roadmap"
            ],
            "key_metrics": [
                "Model Accuracy",
                "Inference Latency",
                "Data Quality Score",
                "AI Feature Adoption",
                "Model Drift Detection"
            ]
        }
    
    # Marketing Scenarios
    def _product_launch_scenario(self) -> Dict[str, Any]:
        return {
            "name": "Product Launch Team",
            "description": "Complete team for major product launch campaign",
            "team_size": 8,
            "agents": [
                {
                    "template": "marketing_cmo",
                    "agent_id": "launch_cmo_001",
                    "name": "Rachel Thompson - CMO"
                },
                {
                    "template": "product_manager",
                    "agent_id": "launch_pm_001",
                    "name": "David Chen - Product Marketing Manager"
                },
                {
                    "template": "digital_marketer",
                    "agent_id": "launch_digital_001",
                    "name": "Sarah Martinez - Digital Marketing Manager"
                },
                {
                    "template": "content_strategist",
                    "agent_id": "launch_content_001",
                    "name": "Emma Rodriguez - Content Strategist"
                },
                {
                    "template": "social_media_expert",
                    "agent_id": "launch_social_001",
                    "name": "Alex Park - Social Media Manager"
                },
                {
                    "template": "brand_designer",
                    "agent_id": "launch_brand_001",
                    "name": "Lisa Kim - Brand Designer"
                },
                {
                    "template": "sales_director",
                    "agent_id": "launch_sales_001",
                    "name": "Marcus Johnson - Sales Director"
                },
                {
                    "template": "data_scientist",
                    "agent_id": "launch_analytics_001",
                    "name": "Priya Singh - Marketing Analyst"
                }
            ],
            "common_tasks": [
                "Create comprehensive product launch strategy",
                "Develop multi-channel marketing campaign",
                "Design launch event and PR strategy",
                "Build sales enablement materials",
                "Set up launch metrics and tracking"
            ],
            "key_metrics": [
                "Launch Awareness",
                "Lead Generation",
                "Conversion Rate",
                "Media Coverage",
                "Sales Pipeline"
            ]
        }
    
    # Enterprise Scenarios
    def _digital_transformation_scenario(self) -> Dict[str, Any]:
        return {
            "name": "Digital Transformation Team",
            "description": "Enterprise team for digital transformation initiatives",
            "team_size": 10,
            "agents": [
                {
                    "template": "enterprise_ceo",
                    "agent_id": "dt_ceo_001",
                    "name": "Jennifer Liu - Transformation CEO"
                },
                {
                    "template": "tech_cto",
                    "agent_id": "dt_cto_001",
                    "name": "Marcus Chen - Digital CTO"
                },
                {
                    "template": "business_analyst",
                    "agent_id": "dt_analyst_001",
                    "name": "Sarah Rodriguez - Business Analyst"
                },
                {
                    "template": "cloud_architect",
                    "agent_id": "dt_cloud_001",
                    "name": "Alex Thompson - Cloud Architect"
                },
                {
                    "template": "data_scientist",
                    "agent_id": "dt_data_001",
                    "name": "Priya Park - Data Strategist"
                },
                {
                    "template": "security_expert",
                    "agent_id": "dt_security_001",
                    "name": "David Kim - Security Architect"
                },
                {
                    "template": "project_manager",
                    "agent_id": "dt_pm_001",
                    "name": "Emma Martinez - Transformation PM"
                },
                {
                    "template": "hr_specialist",
                    "agent_id": "dt_hr_001",
                    "name": "Lisa Wang - Change Management"
                },
                {
                    "template": "finance_analyst",
                    "agent_id": "dt_finance_001",
                    "name": "Kevin Singh - Financial Analyst"
                },
                {
                    "template": "legal_advisor",
                    "agent_id": "dt_legal_001",
                    "name": "Rachel Johnson - Legal Advisor"
                }
            ],
            "common_tasks": [
                "Assess current digital maturity and gaps",
                "Create digital transformation roadmap",
                "Design cloud migration strategy",
                "Implement data governance framework",
                "Manage organizational change and training"
            ],
            "key_metrics": [
                "Digital Maturity Score",
                "Process Automation Rate",
                "Cloud Migration Progress",
                "Employee Digital Adoption",
                "ROI on Digital Investments"
            ]
        }
    
    def create_scenario_team(self, scenario_name: str, custom_prefix: str = None) -> List[Dict[str, Any]]:
        """Create a complete team from a scenario template."""
        scenario = self.get_scenario(scenario_name)
        team_configs = []
        
        for agent_config in scenario["agents"]:
            template_name = agent_config["template"]
            agent_id = agent_config["agent_id"]
            
            if custom_prefix:
                agent_id = f"{custom_prefix}_{agent_id}"
            
            config = agent_templates.create_agent_from_template(
                template_name, 
                agent_id, 
                agent_config["name"]
            )
            
            team_configs.append({
                "config": config,
                "template": template_name,
                "scenario_role": agent_config.get("scenario_role", "")
            })
        
        return team_configs

    # Add missing scenario methods
    def _ecommerce_startup_scenario(self) -> Dict[str, Any]:
        return {
            "name": "E-commerce Startup Team",
            "description": "Complete team for e-commerce startup",
            "team_size": 8,
            "agents": [
                {"template": "startup_ceo", "agent_id": "ecom_ceo_001", "name": "Alex Chen - E-commerce CEO"},
                {"template": "product_manager", "agent_id": "ecom_pm_001", "name": "Sarah Kim - Product Manager"},
                {"template": "digital_marketer", "agent_id": "ecom_marketing_001", "name": "Emma Thompson - Digital Marketer"},
                {"template": "frontend_specialist", "agent_id": "ecom_frontend_001", "name": "David Park - Frontend Engineer"},
                {"template": "backend_specialist", "agent_id": "ecom_backend_001", "name": "Lisa Wang - Backend Engineer"},
                {"template": "ui_designer", "agent_id": "ecom_designer_001", "name": "Jordan Smith - UI Designer"},
                {"template": "data_scientist", "agent_id": "ecom_data_001", "name": "Maya Patel - Data Analyst"},
                {"template": "customer_success", "agent_id": "ecom_cs_001", "name": "Rachel Green - Customer Success"}
            ],
            "common_tasks": ["Build e-commerce platform", "Create marketing campaigns", "Optimize conversion rates"],
            "key_metrics": ["Conversion Rate", "Average Order Value", "Customer Acquisition Cost"]
        }

    def _fintech_startup_scenario(self) -> Dict[str, Any]:
        return {
            "name": "FinTech Startup Team",
            "description": "Specialized team for financial technology startup",
            "team_size": 9,
            "agents": [
                {"template": "startup_ceo", "agent_id": "fintech_ceo_001", "name": "Alex Rodriguez - FinTech CEO"},
                {"template": "tech_cto", "agent_id": "fintech_cto_001", "name": "Priya Sharma - FinTech CTO"},
                {"template": "product_manager", "agent_id": "fintech_pm_001", "name": "Marcus Johnson - Product Manager"},
                {"template": "backend_specialist", "agent_id": "fintech_backend_001", "name": "Jennifer Liu - Backend Engineer"},
                {"template": "security_expert", "agent_id": "fintech_security_001", "name": "Carlos Silva - Security Expert"},
                {"template": "legal_advisor", "agent_id": "fintech_legal_001", "name": "Maria Garcia - Legal Advisor"},
                {"template": "finance_analyst", "agent_id": "fintech_finance_001", "name": "Kevin Liu - Finance Analyst"},
                {"template": "digital_marketer", "agent_id": "fintech_marketing_001", "name": "Amanda Foster - Digital Marketer"},
                {"template": "customer_success", "agent_id": "fintech_cs_001", "name": "Nicole Davis - Customer Success"}
            ],
            "common_tasks": ["Build secure financial platform", "Ensure regulatory compliance", "Create user acquisition strategy"],
            "key_metrics": ["Transaction Volume", "Security Score", "Regulatory Compliance", "User Trust Score"]
        }

    def _healthtech_startup_scenario(self) -> Dict[str, Any]:
        return {
            "name": "HealthTech Startup Team",
            "description": "Specialized team for healthcare technology startup",
            "team_size": 8,
            "agents": [
                {"template": "startup_ceo", "agent_id": "health_ceo_001", "name": "Dr. Sarah Chen - HealthTech CEO"},
                {"template": "tech_cto", "agent_id": "health_cto_001", "name": "Marcus Rodriguez - HealthTech CTO"},
                {"template": "product_manager", "agent_id": "health_pm_001", "name": "Jennifer Park - Product Manager"},
                {"template": "backend_specialist", "agent_id": "health_backend_001", "name": "Alex Thompson - Backend Engineer"},
                {"template": "security_expert", "agent_id": "health_security_001", "name": "Priya Singh - Security Expert"},
                {"template": "legal_advisor", "agent_id": "health_legal_001", "name": "Robert Kim - Legal Advisor"},
                {"template": "ux_researcher", "agent_id": "health_ux_001", "name": "Emma Martinez - UX Researcher"},
                {"template": "data_scientist", "agent_id": "health_data_001", "name": "Tyler Johnson - Data Scientist"}
            ],
            "common_tasks": ["Build HIPAA-compliant platform", "Design patient-centered experiences", "Ensure medical data security"],
            "key_metrics": ["Patient Satisfaction", "HIPAA Compliance", "Clinical Outcomes", "User Adoption"]
        }

    def _web_platform_development_scenario(self) -> Dict[str, Any]:
        return {
            "name": "Web Platform Development Team",
            "description": "Complete team for web platform development",
            "team_size": 7,
            "agents": [
                {"template": "product_manager", "agent_id": "web_pm_001", "name": "Emma Chen - Web Product Manager"},
                {"template": "frontend_specialist", "agent_id": "web_frontend_001", "name": "David Kim - Frontend Engineer"},
                {"template": "backend_specialist", "agent_id": "web_backend_001", "name": "Sarah Park - Backend Engineer"},
                {"template": "cloud_architect", "agent_id": "web_cloud_001", "name": "Alex Thompson - Cloud Architect"},
                {"template": "ui_designer", "agent_id": "web_ui_001", "name": "Lisa Rodriguez - UI Designer"},
                {"template": "ux_researcher", "agent_id": "web_ux_001", "name": "Jordan Martinez - UX Researcher"},
                {"template": "qa_specialist", "agent_id": "web_qa_001", "name": "Maya Singh - QA Engineer"}
            ],
            "common_tasks": ["Design web platform architecture", "Create responsive user interfaces", "Implement scalable backend"],
            "key_metrics": ["Page Load Speed", "User Engagement", "System Uptime", "Conversion Rate"]
        }

    def _enterprise_software_scenario(self) -> Dict[str, Any]:
        return {
            "name": "Enterprise Software Team",
            "description": "Team for enterprise software development",
            "team_size": 9,
            "agents": [
                {"template": "product_manager", "agent_id": "ent_pm_001", "name": "Jennifer Liu - Enterprise PM"},
                {"template": "senior_engineer", "agent_id": "ent_lead_001", "name": "Marcus Chen - Lead Engineer"},
                {"template": "backend_specialist", "agent_id": "ent_backend_001", "name": "Sarah Rodriguez - Backend Engineer"},
                {"template": "cloud_architect", "agent_id": "ent_cloud_001", "name": "Alex Thompson - Cloud Architect"},
                {"template": "security_expert", "agent_id": "ent_security_001", "name": "David Kim - Security Architect"},
                {"template": "business_analyst", "agent_id": "ent_analyst_001", "name": "Emma Martinez - Business Analyst"},
                {"template": "qa_specialist", "agent_id": "ent_qa_001", "name": "Priya Park - QA Engineer"},
                {"template": "legal_advisor", "agent_id": "ent_legal_001", "name": "Lisa Wang - Legal Advisor"},
                {"template": "project_manager", "agent_id": "ent_project_001", "name": "Kevin Singh - Project Manager"}
            ],
            "common_tasks": ["Build enterprise-grade software", "Ensure security and compliance", "Create scalable architecture"],
            "key_metrics": ["System Reliability", "Security Score", "Compliance Rate", "User Satisfaction"]
        }

    def _digital_marketing_campaign_scenario(self) -> Dict[str, Any]:
        return {
            "name": "Digital Marketing Campaign Team",
            "description": "Specialized team for digital marketing campaigns",
            "team_size": 6,
            "agents": [
                {"template": "digital_marketer", "agent_id": "dm_manager_001", "name": "Rachel Green - Digital Marketing Manager"},
                {"template": "content_strategist", "agent_id": "dm_content_001", "name": "Emma Rodriguez - Content Strategist"},
                {"template": "social_media_expert", "agent_id": "dm_social_001", "name": "Alex Park - Social Media Manager"},
                {"template": "seo_specialist", "agent_id": "dm_seo_001", "name": "Ryan Lee - SEO Specialist"},
                {"template": "brand_designer", "agent_id": "dm_design_001", "name": "Lisa Kim - Brand Designer"},
                {"template": "data_scientist", "agent_id": "dm_analytics_001", "name": "Priya Sharma - Marketing Analyst"}
            ],
            "common_tasks": ["Create multi-channel campaigns", "Optimize content for SEO", "Analyze campaign performance"],
            "key_metrics": ["Campaign ROI", "Lead Generation", "Brand Awareness", "Engagement Rate"]
        }

    def _content_marketing_scenario(self) -> Dict[str, Any]:
        return {
            "name": "Content Marketing Team",
            "description": "Specialized team for content marketing",
            "team_size": 5,
            "agents": [
                {"template": "content_strategist", "agent_id": "cm_strategist_001", "name": "Maya Patel - Content Strategist"},
                {"template": "seo_specialist", "agent_id": "cm_seo_001", "name": "Ryan Lee - SEO Specialist"},
                {"template": "social_media_expert", "agent_id": "cm_social_001", "name": "Ashley Davis - Social Media Manager"},
                {"template": "brand_designer", "agent_id": "cm_designer_001", "name": "Jordan Smith - Brand Designer"},
                {"template": "data_scientist", "agent_id": "cm_analytics_001", "name": "Tyler Johnson - Content Analyst"}
            ],
            "common_tasks": ["Create content strategy", "Produce engaging content", "Optimize for search engines"],
            "key_metrics": ["Content Engagement", "Organic Traffic", "Lead Generation", "Brand Authority"]
        }

    def _growth_hacking_scenario(self) -> Dict[str, Any]:
        return {
            "name": "Growth Hacking Team",
            "description": "Rapid growth and user acquisition team",
            "team_size": 6,
            "agents": [
                {"template": "growth_hacker", "agent_id": "gh_lead_001", "name": "Chris Wilson - Growth Lead"},
                {"template": "digital_marketer", "agent_id": "gh_marketer_001", "name": "Sarah Martinez - Performance Marketer"},
                {"template": "data_scientist", "agent_id": "gh_data_001", "name": "Alex Rodriguez - Growth Analyst"},
                {"template": "product_manager", "agent_id": "gh_product_001", "name": "Emma Chen - Growth Product Manager"},
                {"template": "content_strategist", "agent_id": "gh_content_001", "name": "David Park - Content Creator"},
                {"template": "social_media_expert", "agent_id": "gh_social_001", "name": "Lisa Wang - Community Manager"}
            ],
            "common_tasks": ["Design growth experiments", "Optimize conversion funnels", "Create viral content"],
            "key_metrics": ["Growth Rate", "Viral Coefficient", "Customer Acquisition Cost", "Retention Rate"]
        }

    def _merger_acquisition_scenario(self) -> Dict[str, Any]:
        return {
            "name": "Merger & Acquisition Team",
            "description": "Enterprise M&A transaction team",
            "team_size": 8,
            "agents": [
                {"template": "enterprise_ceo", "agent_id": "ma_ceo_001", "name": "Jennifer Liu - M&A CEO"},
                {"template": "finance_cfo", "agent_id": "ma_cfo_001", "name": "Marcus Chen - M&A CFO"},
                {"template": "legal_advisor", "agent_id": "ma_legal_001", "name": "Sarah Rodriguez - M&A Legal"},
                {"template": "business_analyst", "agent_id": "ma_analyst_001", "name": "Alex Thompson - M&A Analyst"},
                {"template": "finance_analyst", "agent_id": "ma_finance_001", "name": "Priya Park - Financial Analyst"},
                {"template": "hr_specialist", "agent_id": "ma_hr_001", "name": "Emma Martinez - HR Integration"},
                {"template": "operations_manager", "agent_id": "ma_ops_001", "name": "David Kim - Operations"},
                {"template": "project_manager", "agent_id": "ma_pm_001", "name": "Lisa Wang - Integration PM"}
            ],
            "common_tasks": ["Conduct due diligence", "Analyze financial impact", "Plan integration strategy"],
            "key_metrics": ["Deal Value", "Synergy Realization", "Integration Timeline", "Employee Retention"]
        }

    def _international_expansion_scenario(self) -> Dict[str, Any]:
        return {
            "name": "International Expansion Team",
            "description": "Global market expansion team",
            "team_size": 8,
            "agents": [
                {"template": "enterprise_ceo", "agent_id": "ie_ceo_001", "name": "Alex Chen - Global CEO"},
                {"template": "marketing_cmo", "agent_id": "ie_cmo_001", "name": "Sarah Kim - Global CMO"},
                {"template": "business_analyst", "agent_id": "ie_analyst_001", "name": "Marcus Johnson - Market Analyst"},
                {"template": "legal_advisor", "agent_id": "ie_legal_001", "name": "Jennifer Liu - International Legal"},
                {"template": "finance_analyst", "agent_id": "ie_finance_001", "name": "Carlos Silva - Financial Analyst"},
                {"template": "operations_manager", "agent_id": "ie_ops_001", "name": "Maria Garcia - Global Operations"},
                {"template": "hr_specialist", "agent_id": "ie_hr_001", "name": "Kevin Liu - Global HR"},
                {"template": "digital_marketer", "agent_id": "ie_marketing_001", "name": "Amanda Foster - Global Marketing"}
            ],
            "common_tasks": ["Analyze target markets", "Develop localization strategy", "Plan market entry"],
            "key_metrics": ["Market Penetration", "Revenue Growth", "Local Compliance", "Brand Recognition"]
        }

    def _cost_optimization_scenario(self) -> Dict[str, Any]:
        return {
            "name": "Cost Optimization Team",
            "description": "Enterprise cost reduction and efficiency team",
            "team_size": 7,
            "agents": [
                {"template": "finance_cfo", "agent_id": "co_cfo_001", "name": "Michael Rodriguez - CFO"},
                {"template": "operations_manager", "agent_id": "co_ops_001", "name": "Jennifer Park - Operations Manager"},
                {"template": "business_analyst", "agent_id": "co_analyst_001", "name": "Robert Kim - Business Analyst"},
                {"template": "finance_analyst", "agent_id": "co_finance_001", "name": "Priya Sharma - Finance Analyst"},
                {"template": "data_scientist", "agent_id": "co_data_001", "name": "Alex Thompson - Data Analyst"},
                {"template": "project_manager", "agent_id": "co_pm_001", "name": "Emma Martinez - Project Manager"},
                {"template": "hr_specialist", "agent_id": "co_hr_001", "name": "Tyler Johnson - HR Specialist"}
            ],
            "common_tasks": ["Analyze cost structures", "Identify optimization opportunities", "Implement efficiency measures"],
            "key_metrics": ["Cost Reduction", "Efficiency Gains", "ROI", "Employee Impact"]
        }

    def _ai_research_lab_scenario(self) -> Dict[str, Any]:
        return {
            "name": "AI Research Lab Team",
            "description": "Advanced AI research and development team",
            "team_size": 6,
            "agents": [
                {"template": "ai_researcher", "agent_id": "ai_lead_001", "name": "Dr. Priya Sharma - AI Research Lead"},
                {"template": "data_scientist", "agent_id": "ai_ds_001", "name": "Marcus Liu - Data Scientist"},
                {"template": "senior_engineer", "agent_id": "ai_eng_001", "name": "Alex Rodriguez - ML Engineer"},
                {"template": "cloud_architect", "agent_id": "ai_cloud_001", "name": "Sarah Kim - ML Infrastructure"},
                {"template": "business_analyst", "agent_id": "ai_analyst_001", "name": "David Thompson - AI Business Analyst"},
                {"template": "product_manager", "agent_id": "ai_pm_001", "name": "Emma Martinez - AI Product Manager"}
            ],
            "common_tasks": ["Conduct AI research", "Develop ML models", "Build AI infrastructure"],
            "key_metrics": ["Research Output", "Model Performance", "Innovation Index", "Publication Count"]
        }

    def _cybersecurity_team_scenario(self) -> Dict[str, Any]:
        return {
            "name": "Cybersecurity Team",
            "description": "Enterprise cybersecurity and risk management team",
            "team_size": 6,
            "agents": [
                {"template": "security_expert", "agent_id": "sec_lead_001", "name": "Alex Thompson - Security Lead"},
                {"template": "backend_specialist", "agent_id": "sec_eng_001", "name": "Sarah Rodriguez - Security Engineer"},
                {"template": "data_scientist", "agent_id": "sec_analyst_001", "name": "Marcus Chen - Security Analyst"},
                {"template": "legal_advisor", "agent_id": "sec_legal_001", "name": "Jennifer Park - Security Legal"},
                {"template": "operations_manager", "agent_id": "sec_ops_001", "name": "David Kim - Security Operations"},
                {"template": "business_analyst", "agent_id": "sec_risk_001", "name": "Emma Martinez - Risk Analyst"}
            ],
            "common_tasks": ["Assess security risks", "Implement security measures", "Monitor threats"],
            "key_metrics": ["Security Score", "Incident Response Time", "Compliance Rate", "Threat Detection"]
        }

    def _data_analytics_team_scenario(self) -> Dict[str, Any]:
        return {
            "name": "Data Analytics Team",
            "description": "Business intelligence and analytics team",
            "team_size": 5,
            "agents": [
                {"template": "data_scientist", "agent_id": "da_lead_001", "name": "Priya Sharma - Data Science Lead"},
                {"template": "business_analyst", "agent_id": "da_analyst_001", "name": "Marcus Johnson - Business Analyst"},
                {"template": "backend_specialist", "agent_id": "da_eng_001", "name": "Alex Rodriguez - Data Engineer"},
                {"template": "cloud_architect", "agent_id": "da_cloud_001", "name": "Sarah Kim - Data Infrastructure"},
                {"template": "product_manager", "agent_id": "da_pm_001", "name": "Emma Chen - Analytics Product Manager"}
            ],
            "common_tasks": ["Build analytics dashboards", "Analyze business data", "Create predictive models"],
            "key_metrics": ["Data Quality", "Insight Generation", "Decision Impact", "Analytics Adoption"]
        }

    def _consulting_firm_scenario(self) -> Dict[str, Any]:
        return {
            "name": "Consulting Firm Team",
            "description": "Management consulting and advisory team",
            "team_size": 7,
            "agents": [
                {"template": "enterprise_ceo", "agent_id": "cons_partner_001", "name": "Jennifer Liu - Managing Partner"},
                {"template": "business_analyst", "agent_id": "cons_analyst_001", "name": "Marcus Chen - Senior Consultant"},
                {"template": "finance_analyst", "agent_id": "cons_finance_001", "name": "Sarah Rodriguez - Financial Consultant"},
                {"template": "operations_manager", "agent_id": "cons_ops_001", "name": "Alex Thompson - Operations Consultant"},
                {"template": "data_scientist", "agent_id": "cons_data_001", "name": "Priya Park - Data Consultant"},
                {"template": "project_manager", "agent_id": "cons_pm_001", "name": "Emma Martinez - Project Manager"},
                {"template": "digital_marketer", "agent_id": "cons_marketing_001", "name": "David Kim - Marketing Consultant"}
            ],
            "common_tasks": ["Analyze client challenges", "Develop strategic recommendations", "Implement solutions"],
            "key_metrics": ["Client Satisfaction", "Project Success Rate", "Revenue Growth", "Recommendation Impact"]
        }

# Global scenario manager instance
business_scenarios = BusinessScenarioManager()
