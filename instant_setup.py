"""
Instant AI Company Setup
One-command setup for immediate AI company deployment with templates.
"""

import sys
import os
from datetime import datetime
from templates.business_scenarios import business_scenarios
from config.settings import settings, LLMConfig, LLMProvider

def instant_setup(scenario_name="tech_startup"):
    """Set up AI company instantly with a business scenario."""
    
    print("⚡ Instant AI Company Setup")
    print("=" * 50)
    print(f"Setting up: {scenario_name}")
    print()
    
    try:
        # Get scenario
        scenario = business_scenarios.get_scenario(scenario_name)
        print(f"📋 {scenario['name']}")
        print(f"📝 {scenario['description']}")
        print(f"👥 Team size: {scenario['team_size']} agents")
        print()
        
        # Create directories
        os.makedirs("config", exist_ok=True)
        os.makedirs("data", exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        
        # Set up basic LLM config
        if not settings.llm_configs:
            print("🧠 Setting up LLM configuration...")
            config = LLMConfig(
                provider=LLMProvider.OPENAI,
                model_name="gpt-4",
                api_key=os.getenv("OPENAI_API_KEY", "your_openai_api_key_here"),
                temperature=0.7,
                max_tokens=4000
            )
            settings.add_llm_config("openai_gpt4", config)
            print("✅ LLM configuration ready")
        
        # Create team
        print("👥 Creating AI team...")
        team_configs = business_scenarios.create_scenario_team(scenario_name)
        
        for team_member in team_configs:
            config = team_member["config"]
            settings.add_agent_config(config)
            print(f"  ✅ {config.name}")
        
        # Save scenario info
        scenario_data = {
            "scenario_name": scenario_name,
            "scenario_info": scenario,
            "setup_date": datetime.now().isoformat(),
            "setup_type": "instant_setup"
        }
        
        os.makedirs("data", exist_ok=True)
        import json
        with open("data/current_scenario.json", 'w') as f:
            json.dump(scenario_data, f, indent=2)
        
        # Create status file
        status = {
            "setup_completed": True,
            "setup_date": datetime.now().isoformat(),
            "setup_type": "instant_template_setup",
            "scenario": scenario_name,
            "agents_configured": len(team_configs),
            "version": "1.0.0"
        }
        
        with open("data/setup_status.json", 'w') as f:
            json.dump(status, f, indent=2)
        
        print(f"\n🎉 {scenario['name']} setup complete!")
        print(f"✅ {len(team_configs)} AI agents ready")
        
        # Show example tasks
        if 'common_tasks' in scenario:
            print(f"\n📋 Example tasks for your team:")
            for i, task in enumerate(scenario['common_tasks'][:3], 1):
                print(f"  {i}. {task}")
        
        # Show key metrics
        if 'key_metrics' in scenario:
            print(f"\n📊 Key metrics to track:")
            for metric in scenario['key_metrics'][:3]:
                print(f"  • {metric}")
        
        print(f"\n🚀 Next steps:")
        print(f"1. Add your OpenAI API key to .env file")
        print(f"2. Start dashboard: py main.py dashboard")
        print(f"3. Access interface: http://localhost:5000")
        print(f"4. Assign tasks: py assign_task.py \"your task here\"")
        
        return True
        
    except Exception as e:
        print(f"❌ Setup failed: {str(e)}")
        return False

def show_available_scenarios():
    """Show all available scenarios for instant setup."""
    print("⚡ Available Instant Setup Scenarios")
    print("=" * 50)
    
    categories = business_scenarios.get_scenarios_by_category()
    
    for category, scenario_list in categories.items():
        print(f"\n📋 {category}:")
        for scenario in scenario_list:
            try:
                scenario_info = business_scenarios.get_scenario(scenario)
                print(f"  • {scenario} - {scenario_info['name']} ({scenario_info['team_size']} agents)")
            except:
                print(f"  • {scenario}")

def main():
    """Main function with command line arguments."""
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "list":
            show_available_scenarios()
            return
        elif command in business_scenarios.list_scenarios():
            instant_setup(command)
            return
        else:
            print(f"❌ Unknown scenario: {command}")
            print("Use 'py instant_setup.py list' to see available scenarios")
            return
    
    # Default interactive mode
    print("⚡ Instant AI Company Setup")
    print("=" * 40)
    print("Choose a setup option:")
    print()
    print("🚀 Popular Scenarios:")
    print("1. tech_startup - Tech Startup Team (8 agents)")
    print("2. saas_startup - SaaS Startup Team (10 agents)")
    print("3. mobile_app_development - Mobile App Team (7 agents)")
    print("4. ai_product_development - AI Product Team (8 agents)")
    print("5. product_launch - Product Launch Team (8 agents)")
    print()
    print("📋 Other options:")
    print("• Type scenario name directly")
    print("• Use 'list' to see all scenarios")
    print()
    
    choice = input("Enter choice (1-5, scenario name, or 'list'): ").strip()
    
    scenario_map = {
        "1": "tech_startup",
        "2": "saas_startup", 
        "3": "mobile_app_development",
        "4": "ai_product_development",
        "5": "product_launch"
    }
    
    if choice in scenario_map:
        instant_setup(scenario_map[choice])
    elif choice == "list":
        show_available_scenarios()
    elif choice in business_scenarios.list_scenarios():
        instant_setup(choice)
    else:
        print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
