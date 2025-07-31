"""
Simple AI Company Setup
Basic setup without external dependencies for immediate use.
"""

import os
import json
from datetime import datetime

def create_basic_config():
    """Create basic configuration files."""
    
    print("🤖 AI Company - Simple Setup")
    print("=" * 40)
    
    # Create directories
    os.makedirs("config", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Basic configuration
    config = {
        "llm_configs": {
            "openai_gpt4": {
                "provider": "openai",
                "model_name": "gpt-4",
                "api_key": os.getenv("OPENAI_API_KEY", ""),
                "temperature": 0.7,
                "max_tokens": 4000,
                "timeout": 30,
                "retry_attempts": 3,
                "custom_headers": {}
            }
        },
        "database_config": {
            "type": "sqlite",
            "host": "localhost",
            "port": 5432,
            "database": "ai_company",
            "username": "admin",
            "password": "",
            "ssl_mode": "prefer",
            "connection_pool_size": 10,
            "max_overflow": 20
        },
        "agent_configs": {},
        "integration_configs": {},
        "general_settings": {
            "company_name": "AI Company",
            "timezone": "UTC",
            "log_level": "INFO",
            "max_concurrent_tasks": 10,
            "task_timeout_minutes": 60,
            "auto_save_interval": 300,
            "backup_enabled": True,
            "backup_interval_hours": 24,
            "monitoring_enabled": True,
            "metrics_retention_days": 30,
            "security": {
                "encryption_enabled": True,
                "session_timeout_minutes": 30,
                "max_login_attempts": 5,
                "require_2fa": False
            },
            "notifications": {
                "email_enabled": False,
                "slack_enabled": False,
                "webhook_enabled": False
            },
            "performance": {
                "cache_enabled": True,
                "cache_ttl_seconds": 3600,
                "rate_limiting_enabled": True,
                "max_requests_per_minute": 100
            }
        }
    }
    
    # Save configuration
    config_file = "config/ai_company_config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Configuration saved to {config_file}")
    
    # Create agent configurations
    agent_roles = [
        ("ceo_001", "ceo", "Alex Chen - CEO"),
        ("cto_001", "cto", "Sarah Kim - CTO"),
        ("cmo_001", "cmo", "Emma Thompson - CMO"),
        ("cfо_001", "cfo", "Michael Rodriguez - CFO"),
        ("chro_001", "chro", "Lisa Wang - CHRO"),
        ("pm_001", "product_manager", "David Park - Product Manager"),
        ("lead_eng_001", "lead_engineer", "Alex Rodriguez - Lead Engineer"),
        ("frontend_eng_001", "frontend_engineer", "Sophie Chen - Frontend Engineer"),
        ("backend_eng_001", "backend_engineer", "Marcus Johnson - Backend Engineer"),
        ("qa_eng_001", "qa_engineer", "Priya Patel - QA Engineer"),
        ("ux_designer_001", "ux_designer", "Jordan Smith - UX Designer"),
        ("ui_designer_001", "ui_designer", "Taylor Brown - UI Designer"),
        ("marketing_mgr_001", "marketing_manager", "Rachel Green - Marketing Manager"),
        ("content_creator_001", "content_creator", "Chris Wilson - Content Creator"),
        ("social_media_001", "social_media_manager", "Ashley Davis - Social Media Manager"),
        ("seo_specialist_001", "seo_specialist", "Ryan Lee - SEO Specialist"),
        ("sales_mgr_001", "sales_manager", "Jennifer Martinez - Sales Manager"),
        ("customer_success_001", "customer_success", "Kevin Zhang - Customer Success"),
        ("ops_mgr_001", "operations_manager", "Michael Chen - Operations Manager"),
        ("finance_analyst_001", "finance_analyst", "Jennifer Park - Finance Analyst"),
        ("legal_advisor_001", "legal_advisor", "Robert Kim - Legal Advisor"),
        ("data_analyst_001", "data_analyst", "Priya Sharma - Data Analyst"),
        ("security_specialist_001", "security_specialist", "Alex Thompson - Security Specialist")
    ]
    
    for agent_id, role, name in agent_roles:
        config["agent_configs"][agent_id] = {
            "agent_id": agent_id,
            "role": role,
            "name": name,
            "llm_config": "openai_gpt4",
            "system_prompt": f"You are a {role.replace('_', ' ').title()} in an AI company. Work collaboratively with other AI agents to achieve business objectives.",
            "temperature": 0.7,
            "max_context_length": 8000,
            "memory_enabled": True,
            "tools_enabled": ["web_search", "calculator", "file_access"],
            "custom_instructions": ""
        }
    
    # Save updated configuration
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Configured {len(agent_roles)} AI agents")
    
    # Create .env file if it doesn't exist
    env_file = ".env"
    if not os.path.exists(env_file):
        env_content = f"""# AI Company Environment Configuration
# Generated on {datetime.now().isoformat()}

# LLM Configuration
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Database Configuration
DB_TYPE=sqlite
DB_PATH=data/ai_company.db

# Application Settings
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
COMPANY_NAME=AI Company
HOST=0.0.0.0
PORT=5000

# Security
JWT_SECRET_KEY=your_jwt_secret_key_here
SESSION_SECRET=your_session_secret_here

# Performance
CACHE_ENABLED=true
MAX_CONCURRENT_TASKS=10
"""
        
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print(f"✅ Environment template created: {env_file}")
        print("⚠️ Please edit .env file with your actual API keys")
    
    # Create basic data directory structure
    data_dirs = [
        "data/files",
        "data/backups",
        "data/logs",
        "data/cache"
    ]
    
    for dir_path in data_dirs:
        os.makedirs(dir_path, exist_ok=True)
    
    print("✅ Data directories created")
    
    # Create a simple status file
    status = {
        "setup_completed": True,
        "setup_date": datetime.now().isoformat(),
        "version": "1.0.0",
        "agents_configured": len(agent_roles),
        "llm_providers": 1,
        "database_type": "sqlite"
    }
    
    with open("data/setup_status.json", 'w') as f:
        json.dump(status, f, indent=2)
    
    print("\n🎉 Basic setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file with your API keys")
    print("2. Start the system: py main.py dashboard")
    print("3. Access dashboard: http://localhost:5000")
    print("4. Assign tasks: py assign_task.py \"your task here\"")
    
    return True

def check_setup_status():
    """Check if setup has been completed."""
    status_file = "data/setup_status.json"
    if os.path.exists(status_file):
        with open(status_file, 'r') as f:
            status = json.load(f)
        return status.get("setup_completed", False)
    return False

def main():
    """Main setup function."""
    print("🤖 AI Company Setup")
    print("=" * 30)
    
    if check_setup_status():
        print("✅ Setup already completed!")
        print("Configuration files found.")
        
        choice = input("\nRe-run setup? (y/N): ").strip().lower()
        if choice != 'y':
            print("Setup skipped.")
            return
    
    try:
        create_basic_config()
        print("\n✅ Setup completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    main()
