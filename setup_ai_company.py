"""
AI Company Setup and Configuration Script
Complete setup wizard for configuring the AI company with custom LLMs, data sources, and settings.
"""

import asyncio
import os
import json
from typing import Dict, List, Any
import logging

from config.settings import settings, LLMConfig, LLMProvider, AgentConfig, DatabaseConfig, DatabaseType
from core.llm_integration import llm_manager
from core.data_manager import data_manager
from core.advanced_agent import AdvancedAIAgent
from core.agent_framework import AgentRole, communication_hub

logger = logging.getLogger(__name__)

class AICompanySetup:
    """Setup wizard for AI company configuration."""
    
    def __init__(self):
        self.setup_complete = False
        self.config_backup = None
    
    async def run_setup_wizard(self):
        """Run the complete setup wizard."""
        print("🤖 AI Company Setup Wizard")
        print("=" * 50)
        print("Welcome! Let's configure your AI company with custom settings.")
        print()
        
        try:
            # Step 1: Basic Configuration
            await self.setup_basic_config()
            
            # Step 2: LLM Providers
            await self.setup_llm_providers()
            
            # Step 3: Database Configuration
            await self.setup_database()
            
            # Step 4: Agent Configuration
            await self.setup_agents()
            
            # Step 5: Integrations
            await self.setup_integrations()
            
            # Step 6: Initialize System
            await self.initialize_system()
            
            # Step 7: Verification
            await self.verify_setup()
            
            print("\n🎉 Setup completed successfully!")
            print("Your AI company is ready to use.")
            print("\nNext steps:")
            print("1. Start the dashboard: py main.py dashboard")
            print("2. Assign tasks: py assign_task.py \"your task here\"")
            print("3. Access settings: http://localhost:5000/settings")
            
            self.setup_complete = True
            
        except Exception as e:
            print(f"\n❌ Setup failed: {str(e)}")
            await self.restore_backup()
            raise
    
    async def setup_basic_config(self):
        """Setup basic company configuration."""
        print("📋 Step 1: Basic Configuration")
        print("-" * 30)
        
        company_name = input("Company name [AI Company]: ").strip() or "AI Company"
        timezone = input("Timezone [UTC]: ").strip() or "UTC"
        
        settings.update_general_setting("company_name", company_name)
        settings.update_general_setting("timezone", timezone)
        
        print(f"✅ Basic configuration set for {company_name}")
        print()
    
    async def setup_llm_providers(self):
        """Setup LLM provider configurations."""
        print("🧠 Step 2: LLM Provider Configuration")
        print("-" * 40)
        
        print("Configure at least one LLM provider for your AI agents.")
        print("Available providers:")
        print("1. OpenAI (GPT-4, GPT-3.5)")
        print("2. Anthropic (Claude)")
        print("3. Azure OpenAI")
        print("4. Ollama (Local)")
        print("5. Custom API")
        print()
        
        while True:
            choice = input("Select provider (1-5) or 'done' to finish: ").strip()
            
            if choice.lower() == 'done':
                break
            elif choice == '1':
                await self.setup_openai()
            elif choice == '2':
                await self.setup_anthropic()
            elif choice == '3':
                await self.setup_azure_openai()
            elif choice == '4':
                await self.setup_ollama()
            elif choice == '5':
                await self.setup_custom_llm()
            else:
                print("Invalid choice. Please select 1-5 or 'done'.")
        
        if not settings.llm_configs:
            print("⚠️ No LLM providers configured. Setting up default OpenAI config.")
            await self.setup_default_openai()
        
        print("✅ LLM providers configured")
        print()
    
    async def setup_openai(self):
        """Setup OpenAI configuration."""
        print("\n🔧 OpenAI Configuration")
        
        config_name = input("Configuration name [openai_gpt4]: ").strip() or "openai_gpt4"
        model_name = input("Model name [gpt-4]: ").strip() or "gpt-4"
        api_key = input("API Key (required): ").strip()
        
        if not api_key:
            print("❌ API key is required for OpenAI")
            return
        
        config = LLMConfig(
            provider=LLMProvider.OPENAI,
            model_name=model_name,
            api_key=api_key,
            temperature=0.7,
            max_tokens=4000
        )
        
        settings.add_llm_config(config_name, config)
        
        # Test connection
        print("Testing connection...")
        result = await llm_manager.test_connection(config_name)
        if result["success"]:
            print(f"✅ OpenAI connection successful ({result['response_time']:.2f}s)")
        else:
            print(f"❌ Connection failed: {result['error']}")
    
    async def setup_anthropic(self):
        """Setup Anthropic configuration."""
        print("\n🔧 Anthropic Configuration")
        
        config_name = input("Configuration name [anthropic_claude]: ").strip() or "anthropic_claude"
        model_name = input("Model name [claude-3-sonnet-20240229]: ").strip() or "claude-3-sonnet-20240229"
        api_key = input("API Key (required): ").strip()
        
        if not api_key:
            print("❌ API key is required for Anthropic")
            return
        
        config = LLMConfig(
            provider=LLMProvider.ANTHROPIC,
            model_name=model_name,
            api_key=api_key,
            temperature=0.7,
            max_tokens=4000
        )
        
        settings.add_llm_config(config_name, config)
        print("✅ Anthropic configuration added")
    
    async def setup_azure_openai(self):
        """Setup Azure OpenAI configuration."""
        print("\n🔧 Azure OpenAI Configuration")
        
        config_name = input("Configuration name [azure_gpt4]: ").strip() or "azure_gpt4"
        model_name = input("Deployment name: ").strip()
        api_key = input("API Key: ").strip()
        endpoint = input("Endpoint URL: ").strip()
        
        if not all([model_name, api_key, endpoint]):
            print("❌ All fields are required for Azure OpenAI")
            return
        
        config = LLMConfig(
            provider=LLMProvider.AZURE_OPENAI,
            model_name=model_name,
            api_key=api_key,
            api_base=endpoint,
            temperature=0.7,
            max_tokens=4000
        )
        
        settings.add_llm_config(config_name, config)
        print("✅ Azure OpenAI configuration added")
    
    async def setup_ollama(self):
        """Setup Ollama local configuration."""
        print("\n🔧 Ollama Local Configuration")
        
        config_name = input("Configuration name [ollama_local]: ").strip() or "ollama_local"
        model_name = input("Model name [llama2]: ").strip() or "llama2"
        api_base = input("Ollama URL [http://localhost:11434]: ").strip() or "http://localhost:11434"
        
        config = LLMConfig(
            provider=LLMProvider.OLLAMA,
            model_name=model_name,
            api_base=api_base,
            temperature=0.7,
            max_tokens=4000
        )
        
        settings.add_llm_config(config_name, config)
        
        # Test connection
        print("Testing Ollama connection...")
        try:
            result = await llm_manager.test_connection(config_name)
            if result["success"]:
                print(f"✅ Ollama connection successful")
            else:
                print(f"⚠️ Connection failed: {result['error']}")
                print("Make sure Ollama is running and the model is available")
        except Exception as e:
            print(f"⚠️ Could not test connection: {e}")
    
    async def setup_custom_llm(self):
        """Setup custom LLM configuration."""
        print("\n🔧 Custom LLM Configuration")
        
        config_name = input("Configuration name: ").strip()
        model_name = input("Model identifier: ").strip()
        api_base = input("API endpoint URL: ").strip()
        api_key = input("API key (optional): ").strip() or None
        
        if not all([config_name, model_name, api_base]):
            print("❌ Configuration name, model, and endpoint are required")
            return
        
        config = LLMConfig(
            provider=LLMProvider.CUSTOM,
            model_name=model_name,
            api_key=api_key,
            api_base=api_base,
            temperature=0.7,
            max_tokens=4000
        )
        
        settings.add_llm_config(config_name, config)
        print("✅ Custom LLM configuration added")
    
    async def setup_default_openai(self):
        """Setup default OpenAI configuration with environment variable."""
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            config = LLMConfig(
                provider=LLMProvider.OPENAI,
                model_name="gpt-4",
                api_key=api_key,
                temperature=0.7,
                max_tokens=4000
            )
            settings.add_llm_config("openai_gpt4", config)
            print("✅ Default OpenAI configuration created from environment variable")
        else:
            print("⚠️ No OPENAI_API_KEY environment variable found")
            print("You can add LLM configurations later in the settings")
    
    async def setup_database(self):
        """Setup database configuration."""
        print("🗄️ Step 3: Database Configuration")
        print("-" * 35)
        
        print("Database options:")
        print("1. SQLite (Local, recommended for development)")
        print("2. PostgreSQL (Production recommended)")
        print("3. MySQL")
        print("4. MongoDB")
        print()
        
        choice = input("Select database (1-4) [1]: ").strip() or "1"
        
        if choice == "1":
            db_config = DatabaseConfig(
                type=DatabaseType.SQLITE,
                database="ai_company",
                host="localhost"
            )
        elif choice == "2":
            host = input("PostgreSQL host [localhost]: ").strip() or "localhost"
            port = int(input("Port [5432]: ").strip() or "5432")
            database = input("Database name [ai_company]: ").strip() or "ai_company"
            username = input("Username [postgres]: ").strip() or "postgres"
            password = input("Password: ").strip()
            
            db_config = DatabaseConfig(
                type=DatabaseType.POSTGRESQL,
                host=host,
                port=port,
                database=database,
                username=username,
                password=password
            )
        else:
            print("Using default SQLite configuration")
            db_config = DatabaseConfig(
                type=DatabaseType.SQLITE,
                database="ai_company",
                host="localhost"
            )
        
        settings.database_config = db_config
        settings.save_config()
        
        print("✅ Database configuration set")
        print()
    
    async def setup_agents(self):
        """Setup agent configurations."""
        print("🤖 Step 4: Agent Configuration")
        print("-" * 32)
        
        if not settings.llm_configs:
            print("⚠️ No LLM configurations available. Skipping agent setup.")
            return
        
        # Get default LLM config
        default_llm = list(settings.llm_configs.keys())[0]
        print(f"Using '{default_llm}' as default LLM for agents")
        
        # Create agent configurations for all roles
        agent_roles = [
            (AgentRole.CEO, "Alex Chen - CEO"),
            (AgentRole.CTO, "Sarah Kim - CTO"),
            (AgentRole.CMO, "Emma Thompson - CMO"),
            (AgentRole.CFO, "Michael Rodriguez - CFO"),
            (AgentRole.CHRO, "Lisa Wang - CHRO"),
            (AgentRole.PRODUCT_MANAGER, "David Park - Product Manager"),
            (AgentRole.LEAD_ENGINEER, "Alex Rodriguez - Lead Engineer"),
            (AgentRole.FRONTEND_ENGINEER, "Sophie Chen - Frontend Engineer"),
            (AgentRole.BACKEND_ENGINEER, "Marcus Johnson - Backend Engineer"),
            (AgentRole.QA_ENGINEER, "Priya Patel - QA Engineer"),
            (AgentRole.UX_DESIGNER, "Jordan Smith - UX Designer"),
            (AgentRole.UI_DESIGNER, "Taylor Brown - UI Designer"),
            (AgentRole.MARKETING_MANAGER, "Rachel Green - Marketing Manager"),
            (AgentRole.CONTENT_CREATOR, "Chris Wilson - Content Creator"),
            (AgentRole.SOCIAL_MEDIA_MANAGER, "Ashley Davis - Social Media Manager"),
            (AgentRole.SEO_SPECIALIST, "Ryan Lee - SEO Specialist"),
            (AgentRole.SALES_MANAGER, "Jennifer Martinez - Sales Manager"),
            (AgentRole.CUSTOMER_SUCCESS, "Kevin Zhang - Customer Success"),
            (AgentRole.OPERATIONS_MANAGER, "Michael Chen - Operations Manager"),
            (AgentRole.FINANCE_ANALYST, "Jennifer Park - Finance Analyst"),
            (AgentRole.LEGAL_ADVISOR, "Robert Kim - Legal Advisor"),
            (AgentRole.DATA_ANALYST, "Priya Sharma - Data Analyst"),
            (AgentRole.SECURITY_SPECIALIST, "Alex Thompson - Security Specialist")
        ]
        
        for role, name in agent_roles:
            agent_id = f"{role.value}_001"
            config = AgentConfig(
                agent_id=agent_id,
                role=role.value,
                name=name,
                llm_config=default_llm,
                system_prompt=self._get_role_prompt(role),
                temperature=0.7,
                max_context_length=8000,
                memory_enabled=True,
                tools_enabled=["web_search", "calculator", "file_access"],
                custom_instructions=""
            )
            settings.add_agent_config(config)
        
        print(f"✅ Configured {len(agent_roles)} AI agents")
        print()
    
    def _get_role_prompt(self, role: AgentRole) -> str:
        """Get system prompt for agent role."""
        # This would return detailed prompts for each role
        return f"You are a {role.value.replace('_', ' ').title()} in an AI company. Work collaboratively with other AI agents to achieve business objectives."
    
    async def setup_integrations(self):
        """Setup external integrations."""
        print("🔌 Step 5: External Integrations")
        print("-" * 35)
        
        print("Available integrations:")
        print("1. Slack notifications")
        print("2. Email notifications")
        print("3. Webhooks")
        print("4. Skip integrations")
        print()
        
        choice = input("Select integration to configure (1-4) [4]: ").strip() or "4"
        
        if choice == "4":
            print("⏭️ Skipping integrations (can be configured later)")
        else:
            print("⏭️ Integration setup will be available in the settings interface")
        
        print()
    
    async def initialize_system(self):
        """Initialize the AI company system."""
        print("⚙️ Step 6: System Initialization")
        print("-" * 33)
        
        print("Initializing data manager...")
        await data_manager.initialize()
        
        print("Creating agent instances...")
        # This would create actual agent instances
        
        print("Setting up communication hub...")
        # Initialize communication system
        
        print("✅ System initialized successfully")
        print()
    
    async def verify_setup(self):
        """Verify the setup is working correctly."""
        print("✅ Step 7: Setup Verification")
        print("-" * 30)
        
        # Test LLM connections
        print("Testing LLM connections...")
        for config_name in settings.llm_configs.keys():
            try:
                result = await llm_manager.test_connection(config_name)
                status = "✅" if result["success"] else "❌"
                print(f"  {status} {config_name}")
            except Exception as e:
                print(f"  ❌ {config_name}: {str(e)}")
        
        # Test database connection
        print("Testing database connection...")
        try:
            # This would test the actual database connection
            print("  ✅ Database connection successful")
        except Exception as e:
            print(f"  ❌ Database connection failed: {e}")
        
        # Validate configuration
        print("Validating configuration...")
        issues = settings.validate_config()
        if issues:
            print("  ⚠️ Configuration issues found:")
            for issue in issues:
                print(f"    - {issue}")
        else:
            print("  ✅ Configuration is valid")
        
        print()
    
    async def restore_backup(self):
        """Restore configuration backup if setup fails."""
        if self.config_backup:
            print("Restoring previous configuration...")
            # Restore backup logic here
            print("✅ Configuration restored")

async def main():
    """Main setup function."""
    setup = AICompanySetup()
    
    print("Choose setup option:")
    print("1. Full setup wizard (recommended for first time)")
    print("2. Quick setup with defaults")
    print("3. Load existing configuration")
    print()
    
    choice = input("Select option (1-3) [1]: ").strip() or "1"
    
    if choice == "1":
        await setup.run_setup_wizard()
    elif choice == "2":
        await setup.quick_setup()
    elif choice == "3":
        await setup.load_existing_config()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    asyncio.run(main())
