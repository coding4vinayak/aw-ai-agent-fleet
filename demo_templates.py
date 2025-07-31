"""
Demo script to showcase AI Company Templates
"""

from templates.agent_templates import agent_templates
from templates.business_scenarios import business_scenarios

def show_available_templates():
    """Show all available agent templates."""
    print("🤖 Available Agent Templates")
    print("=" * 50)
    
    categories = agent_templates.get_templates_by_category()
    
    for category, template_list in categories.items():
        print(f"\n📋 {category}:")
        for template in template_list:
            try:
                template_info = agent_templates.get_template(template)
                print(f"  • {template_info['name']}")
            except:
                print(f"  • {template} (template)")
    
    print(f"\nTotal: {len(agent_templates.list_templates())} agent templates available")

def show_available_scenarios():
    """Show all available business scenarios."""
    print("\n🏢 Available Business Scenarios")
    print("=" * 50)
    
    categories = business_scenarios.get_scenarios_by_category()
    
    for category, scenario_list in categories.items():
        print(f"\n📋 {category}:")
        for scenario in scenario_list:
            try:
                scenario_info = business_scenarios.get_scenario(scenario)
                print(f"  • {scenario_info['name']} ({scenario_info['team_size']} agents)")
                print(f"    {scenario_info['description']}")
            except Exception as e:
                print(f"  • {scenario} (scenario) - {e}")
    
    print(f"\nTotal: {len(business_scenarios.list_scenarios())} business scenarios available")

def demo_tech_startup():
    """Demonstrate creating a tech startup team."""
    print("\n🚀 Demo: Creating Tech Startup Team")
    print("=" * 50)
    
    try:
        scenario = business_scenarios.get_scenario("tech_startup")
        print(f"📋 {scenario['name']}")
        print(f"📝 {scenario['description']}")
        print(f"👥 Team size: {scenario['team_size']} agents")
        print()
        
        print("Team Members:")
        for agent in scenario['agents']:
            template_name = agent['template']
            try:
                template = agent_templates.get_template(template_name)
                print(f"  • {agent['name']} - {template['role'].replace('_', ' ').title()}")
            except:
                print(f"  • {agent['name']} - {template_name}")
        
        print(f"\n📋 Example Tasks:")
        for task in scenario['common_tasks']:
            print(f"  • {task}")
        
        print(f"\n📊 Key Metrics:")
        for metric in scenario['key_metrics']:
            print(f"  • {metric}")
            
    except Exception as e:
        print(f"Error: {e}")

def demo_agent_creation():
    """Demonstrate creating individual agents."""
    print("\n🤖 Demo: Creating Individual Agents")
    print("=" * 50)
    
    try:
        # Create a startup CEO
        ceo_config = agent_templates.create_agent_from_template(
            "startup_ceo", 
            "demo_ceo_001",
            "Alex Chen - Demo CEO"
        )
        
        print("✅ Created Startup CEO:")
        print(f"  • ID: {ceo_config.agent_id}")
        print(f"  • Name: {ceo_config.name}")
        print(f"  • Role: {ceo_config.role}")
        print(f"  • LLM: {ceo_config.llm_config}")
        print(f"  • Temperature: {ceo_config.temperature}")
        print(f"  • Tools: {', '.join(ceo_config.tools_enabled)}")
        
        # Create an AI researcher
        ai_config = agent_templates.create_agent_from_template(
            "ai_researcher",
            "demo_ai_001", 
            "Dr. Priya Sharma - Demo AI Researcher"
        )
        
        print("\n✅ Created AI Researcher:")
        print(f"  • ID: {ai_config.agent_id}")
        print(f"  • Name: {ai_config.name}")
        print(f"  • Role: {ai_config.role}")
        print(f"  • LLM: {ai_config.llm_config}")
        print(f"  • Temperature: {ai_config.temperature}")
        print(f"  • Tools: {', '.join(ai_config.tools_enabled)}")
        
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Main demo function."""
    print("🎯 AI Company Templates Demo")
    print("=" * 60)
    
    # Show available templates
    show_available_templates()
    
    # Show available scenarios
    show_available_scenarios()
    
    # Demo tech startup creation
    demo_tech_startup()
    
    # Demo individual agent creation
    demo_agent_creation()
    
    print("\n🎉 Template Demo Complete!")
    print("\nTo use templates in your AI company:")
    print("1. Run: py quick_setup.py")
    print("2. Choose a business scenario")
    print("3. Start your AI company: py main.py dashboard")
    print("4. Assign tasks to your specialized team!")

if __name__ == "__main__":
    main()
