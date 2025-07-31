"""
Quick Setup Script for AI Company
Use pre-built templates to quickly set up teams for different business scenarios.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any

from templates.agent_templates import agent_templates
from templates.business_scenarios import business_scenarios
from config.settings import settings

class QuickSetup:
    """Quick setup manager using templates."""
    
    def __init__(self):
        self.setup_complete = False
    
    def run_interactive_setup(self):
        """Run interactive setup with template selection."""
        print("🚀 AI Company Quick Setup")
        print("=" * 50)
        print("Choose from pre-built templates to get started quickly!")
        print()
        
        # Show available scenarios
        self.show_available_scenarios()
        
        # Get user choice
        choice = input("\nSelect a scenario number or 'custom' for individual agents: ").strip()
        
        if choice.lower() == 'custom':
            self.setup_custom_agents()
        else:
            try:
                scenario_index = int(choice) - 1
                scenarios = self.get_all_scenarios()
                if 0 <= scenario_index < len(scenarios):
                    scenario_name = scenarios[scenario_index]
                    self.setup_scenario_team(scenario_name)
                else:
                    print("Invalid choice. Please run the setup again.")
                    return
            except ValueError:
                print("Invalid choice. Please run the setup again.")
                return
        
        # Finalize setup
        self.finalize_setup()
    
    def show_available_scenarios(self):
        """Display all available business scenarios."""
        categories = business_scenarios.get_scenarios_by_category()
        scenario_count = 1
        
        for category, scenario_list in categories.items():
            print(f"\n📋 {category}:")
            for scenario in scenario_list:
                scenario_info = business_scenarios.get_scenario(scenario)
                print(f"  {scenario_count}. {scenario_info['name']}")
                print(f"     {scenario_info['description']}")
                print(f"     Team size: {scenario_info['team_size']} agents")
                scenario_count += 1
    
    def get_all_scenarios(self) -> List[str]:
        """Get flat list of all scenarios."""
        all_scenarios = []
        categories = business_scenarios.get_scenarios_by_category()
        for scenario_list in categories.values():
            all_scenarios.extend(scenario_list)
        return all_scenarios
    
    def setup_scenario_team(self, scenario_name: str):
        """Set up a complete team from a scenario."""
        print(f"\n🏗️ Setting up {scenario_name} team...")
        
        scenario = business_scenarios.get_scenario(scenario_name)
        print(f"📋 {scenario['name']}")
        print(f"📝 {scenario['description']}")
        print(f"👥 Team size: {scenario['team_size']} agents")
        print()
        
        # Create team configurations
        team_configs = business_scenarios.create_scenario_team(scenario_name)
        
        # Add to settings
        for team_member in team_configs:
            config = team_member["config"]
            settings.add_agent_config(config)
            print(f"✅ Added {config.name} ({config.role})")
        
        # Save scenario info
        self.save_scenario_info(scenario_name, scenario)
        
        print(f"\n🎉 Successfully set up {scenario['name']} with {len(team_configs)} agents!")
        
        # Show common tasks
        if 'common_tasks' in scenario:
            print(f"\n📋 Common tasks for this team:")
            for i, task in enumerate(scenario['common_tasks'], 1):
                print(f"  {i}. {task}")
        
        # Show key metrics
        if 'key_metrics' in scenario:
            print(f"\n📊 Key metrics to track:")
            for metric in scenario['key_metrics']:
                print(f"  • {metric}")
    
    def setup_custom_agents(self):
        """Set up individual agents from templates."""
        print("\n🤖 Custom Agent Setup")
        print("=" * 30)
        
        # Show available templates
        categories = agent_templates.get_templates_by_category()
        template_count = 1
        all_templates = []
        
        for category, template_list in categories.items():
            print(f"\n📋 {category}:")
            for template in template_list:
                template_info = agent_templates.get_template(template)
                print(f"  {template_count}. {template_info['name']}")
                all_templates.append(template)
                template_count += 1
        
        print("\nSelect agents to add (comma-separated numbers, e.g., 1,3,5):")
        choices = input("Your choice: ").strip()
        
        try:
            selected_indices = [int(x.strip()) - 1 for x in choices.split(',')]
            
            for index in selected_indices:
                if 0 <= index < len(all_templates):
                    template_name = all_templates[index]
                    agent_id = f"custom_{template_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    
                    config = agent_templates.create_agent_from_template(template_name, agent_id)
                    settings.add_agent_config(config)
                    print(f"✅ Added {config.name}")
                else:
                    print(f"❌ Invalid selection: {index + 1}")
        
        except ValueError:
            print("❌ Invalid input format. Please use comma-separated numbers.")
    
    def save_scenario_info(self, scenario_name: str, scenario_info: Dict[str, Any]):
        """Save scenario information for reference."""
        os.makedirs("data", exist_ok=True)
        
        scenario_data = {
            "scenario_name": scenario_name,
            "scenario_info": scenario_info,
            "setup_date": datetime.now().isoformat(),
            "setup_type": "quick_setup"
        }
        
        with open("data/current_scenario.json", 'w') as f:
            json.dump(scenario_data, f, indent=2)
    
    def finalize_setup(self):
        """Finalize the setup process."""
        print("\n⚙️ Finalizing setup...")
        
        # Create basic LLM config if none exists
        if not settings.llm_configs:
            print("🧠 Setting up default LLM configuration...")
            self.setup_default_llm()
        
        # Create basic directories
        self.create_directories()
        
        # Create status file
        self.create_status_file()
        
        print("\n🎉 Quick setup completed successfully!")
        print("\nNext steps:")
        print("1. Edit .env file with your API keys")
        print("2. Start the system: py main.py dashboard")
        print("3. Access dashboard: http://localhost:5000")
        print("4. Assign tasks to your new team!")
        
        self.setup_complete = True
    
    def setup_default_llm(self):
        """Set up default LLM configuration."""
        from config.settings import LLMConfig, LLMProvider
        
        # Check for environment variables
        openai_key = os.getenv("OPENAI_API_KEY")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        
        if openai_key:
            config = LLMConfig(
                provider=LLMProvider.OPENAI,
                model_name="gpt-4",
                api_key=openai_key,
                temperature=0.7,
                max_tokens=4000
            )
            settings.add_llm_config("openai_gpt4", config)
            print("✅ Added OpenAI GPT-4 configuration")
        
        if anthropic_key:
            config = LLMConfig(
                provider=LLMProvider.ANTHROPIC,
                model_name="claude-3-sonnet-20240229",
                api_key=anthropic_key,
                temperature=0.7,
                max_tokens=4000
            )
            settings.add_llm_config("anthropic_claude", config)
            print("✅ Added Anthropic Claude configuration")
        
        if not openai_key and not anthropic_key:
            # Create placeholder config
            config = LLMConfig(
                provider=LLMProvider.OPENAI,
                model_name="gpt-4",
                api_key="your_api_key_here",
                temperature=0.7,
                max_tokens=4000
            )
            settings.add_llm_config("openai_gpt4", config)
            print("⚠️ Created placeholder LLM config - please add your API key to .env")
    
    def create_directories(self):
        """Create necessary directories."""
        directories = [
            "data",
            "data/files",
            "data/backups",
            "data/logs",
            "logs",
            "config"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        print("✅ Created data directories")
    
    def create_status_file(self):
        """Create setup status file."""
        status = {
            "setup_completed": True,
            "setup_date": datetime.now().isoformat(),
            "setup_type": "quick_setup_templates",
            "agents_configured": len(settings.agent_configs),
            "llm_providers": len(settings.llm_configs),
            "version": "1.0.0"
        }
        
        with open("data/setup_status.json", 'w') as f:
            json.dump(status, f, indent=2)
    
    def show_scenario_preview(self, scenario_name: str):
        """Show detailed preview of a scenario."""
        scenario = business_scenarios.get_scenario(scenario_name)
        
        print(f"\n📋 {scenario['name']}")
        print("=" * 50)
        print(f"Description: {scenario['description']}")
        print(f"Team Size: {scenario['team_size']} agents")
        print()
        
        print("👥 Team Members:")
        for agent in scenario['agents']:
            template = agent_templates.get_template(agent['template'])
            print(f"  • {agent['name']} - {template['role'].replace('_', ' ').title()}")
        
        if 'common_tasks' in scenario:
            print(f"\n📋 Example Tasks:")
            for task in scenario['common_tasks'][:3]:
                print(f"  • {task}")
        
        if 'key_metrics' in scenario:
            print(f"\n📊 Key Metrics:")
            for metric in scenario['key_metrics'][:3]:
                print(f"  • {metric}")

def main():
    """Main quick setup function."""
    setup = QuickSetup()
    
    print("🚀 AI Company Quick Setup")
    print("=" * 40)
    print("Choose your setup option:")
    print("1. Interactive template selection")
    print("2. Show all available scenarios")
    print("3. Preview specific scenario")
    print()
    
    choice = input("Select option (1-3): ").strip()
    
    if choice == "1":
        setup.run_interactive_setup()
    elif choice == "2":
        setup.show_available_scenarios()
    elif choice == "3":
        scenarios = setup.get_all_scenarios()
        print("\nAvailable scenarios:")
        for i, scenario in enumerate(scenarios, 1):
            print(f"{i}. {scenario}")
        
        try:
            scenario_choice = int(input("\nSelect scenario to preview: ")) - 1
            if 0 <= scenario_choice < len(scenarios):
                setup.show_scenario_preview(scenarios[scenario_choice])
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input.")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
