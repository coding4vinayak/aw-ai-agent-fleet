"""
AI Company Main Application
Entry point for running the complete AI company system.
"""

import asyncio
import argparse
import logging
import sys
from datetime import datetime
from typing import Dict, Any

from workflows.product_launch_demo import run_product_launch_demo
from dashboard.app import app
from core.communication_system import standup_manager, performance_monitor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_company.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class AICompanyManager:
    """Main manager for the AI company system."""
    
    def __init__(self):
        self.is_running = False
        self.background_tasks = []
    
    async def start_company(self):
        """Start the AI company with all systems."""
        logger.info("🚀 Starting AI Company...")
        
        try:
            # Start background monitoring tasks
            await self.start_background_tasks()
            
            # Run the product launch demo
            logger.info("📋 Running product launch demonstration...")
            demo_result = await run_product_launch_demo()
            
            logger.info("✅ AI Company started successfully!")
            logger.info("🌐 Dashboard available at: http://localhost:5000")
            
            self.is_running = True
            return demo_result
            
        except Exception as e:
            logger.error(f"❌ Failed to start AI company: {str(e)}")
            raise
    
    async def start_background_tasks(self):
        """Start background monitoring and coordination tasks."""
        logger.info("🔄 Starting background tasks...")
        
        # Start daily standup task
        standup_task = asyncio.create_task(self.run_daily_standups())
        self.background_tasks.append(standup_task)
        
        # Start performance monitoring task
        monitoring_task = asyncio.create_task(self.run_performance_monitoring())
        self.background_tasks.append(monitoring_task)
        
        logger.info("✅ Background tasks started")
    
    async def run_daily_standups(self):
        """Run daily standup meetings."""
        while self.is_running:
            try:
                # Run standup every 24 hours (for demo, we'll run every hour)
                await asyncio.sleep(3600)  # 1 hour for demo purposes
                
                logger.info("📅 Conducting daily standup...")
                standup_report = await standup_manager.conduct_daily_standup()
                
                logger.info(f"✅ Standup completed with {len(standup_report['participants'])} participants")
                if standup_report['blockers']:
                    logger.warning(f"⚠️ {len(standup_report['blockers'])} blockers identified")
                
            except Exception as e:
                logger.error(f"❌ Error in daily standup: {str(e)}")
                await asyncio.sleep(300)  # Wait 5 minutes before retry
    
    async def run_performance_monitoring(self):
        """Run continuous performance monitoring."""
        while self.is_running:
            try:
                # Collect metrics every 30 minutes
                await asyncio.sleep(1800)  # 30 minutes
                
                logger.info("📊 Collecting performance metrics...")
                metrics = await performance_monitor.collect_performance_metrics()
                
                # Log key metrics
                system_metrics = metrics.get('system_metrics', {})
                logger.info(f"📈 System Status: {system_metrics.get('active_agents', 0)} active agents, "
                           f"{system_metrics.get('response_time_avg', 'N/A')} avg response time")
                
            except Exception as e:
                logger.error(f"❌ Error in performance monitoring: {str(e)}")
                await asyncio.sleep(300)  # Wait 5 minutes before retry
    
    async def stop_company(self):
        """Stop the AI company and cleanup."""
        logger.info("🛑 Stopping AI Company...")
        
        self.is_running = False
        
        # Cancel background tasks
        for task in self.background_tasks:
            task.cancel()
        
        # Wait for tasks to complete
        if self.background_tasks:
            await asyncio.gather(*self.background_tasks, return_exceptions=True)
        
        logger.info("✅ AI Company stopped successfully")
    
    def start_dashboard(self, host='0.0.0.0', port=5000, debug=False):
        """Start the web dashboard."""
        logger.info(f"🌐 Starting dashboard at http://{host}:{port}")
        app.run(host=host, port=port, debug=debug)

async def run_demo_mode():
    """Run the AI company in demo mode."""
    company = AICompanyManager()
    
    try:
        # Start the company
        demo_result = await company.start_company()
        
        print("\n" + "="*60)
        print("🎉 AI COMPANY DEMO COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"📊 Project: {demo_result.get('project_name', 'AI Platform Launch')}")
        print(f"⏱️ Duration: {demo_result.get('duration', '4 months')}")
        print(f"👥 Team Size: {demo_result.get('team_size', '25 AI agents')}")
        print(f"📦 Deliverables: {len(demo_result.get('key_deliverables', []))} completed")
        print(f"🎯 Success Rate: {demo_result.get('success_metrics', {}).get('on_time_delivery', '100%')}")
        print("\n📋 Key Deliverables:")
        for deliverable in demo_result.get('key_deliverables', []):
            print(f"   ✅ {deliverable}")
        
        print("\n🏆 Success Metrics:")
        success_metrics = demo_result.get('success_metrics', {})
        for metric, value in success_metrics.items():
            print(f"   📈 {metric.replace('_', ' ').title()}: {value}")
        
        print("\n💡 Lessons Learned:")
        for lesson in demo_result.get('lessons_learned', []):
            print(f"   🔍 {lesson}")
        
        print("\n🚀 Next Steps:")
        for step in demo_result.get('next_steps', []):
            print(f"   📌 {step}")
        
        print("\n🌐 Dashboard URL: http://localhost:5000")
        print("📝 Logs saved to: ai_company.log")
        print("="*60)
        
        return demo_result
        
    except KeyboardInterrupt:
        logger.info("🛑 Demo interrupted by user")
        await company.stop_company()
    except Exception as e:
        logger.error(f"❌ Demo failed: {str(e)}")
        await company.stop_company()
        raise

def run_dashboard_mode(host='0.0.0.0', port=5000, debug=False):
    """Run only the dashboard."""
    company = AICompanyManager()
    company.start_dashboard(host=host, port=port, debug=debug)

async def run_interactive_mode():
    """Run the AI company in interactive mode."""
    company = AICompanyManager()
    
    print("🤖 AI Company Interactive Mode")
    print("Available commands:")
    print("  start    - Start the AI company")
    print("  demo     - Run product launch demo")
    print("  status   - Show company status")
    print("  standup  - Run daily standup")
    print("  metrics  - Show performance metrics")
    print("  stop     - Stop the company")
    print("  exit     - Exit interactive mode")
    print()
    
    try:
        while True:
            command = input("ai-company> ").strip().lower()
            
            if command == "start":
                await company.start_company()
            elif command == "demo":
                await run_demo_mode()
            elif command == "status":
                from core.agent_framework import communication_hub
                status = communication_hub.get_company_status()
                print(f"📊 Company Status: {status['active_agents']}/{status['total_agents']} agents active")
            elif command == "standup":
                report = await standup_manager.conduct_daily_standup()
                print(f"📅 Standup: {len(report['participants'])} participants, {len(report['blockers'])} blockers")
            elif command == "metrics":
                metrics = await performance_monitor.collect_performance_metrics()
                system_metrics = metrics.get('system_metrics', {})
                print(f"📈 Metrics: {system_metrics}")
            elif command == "stop":
                await company.stop_company()
            elif command in ["exit", "quit"]:
                break
            elif command == "help":
                print("Available commands: start, demo, status, standup, metrics, stop, exit")
            else:
                print(f"Unknown command: {command}. Type 'help' for available commands.")
                
    except KeyboardInterrupt:
        print("\n🛑 Exiting interactive mode...")
        await company.stop_company()

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="AI Company Management System")
    parser.add_argument("mode", choices=["demo", "dashboard", "interactive"], 
                       help="Mode to run the AI company")
    parser.add_argument("--host", default="0.0.0.0", help="Dashboard host (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=5000, help="Dashboard port (default: 5000)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    print("🤖 AI Company Management System")
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Mode: {args.mode}")
    print()
    
    try:
        if args.mode == "demo":
            asyncio.run(run_demo_mode())
        elif args.mode == "dashboard":
            run_dashboard_mode(host=args.host, port=args.port, debug=args.debug)
        elif args.mode == "interactive":
            asyncio.run(run_interactive_mode())
    except KeyboardInterrupt:
        print("\n🛑 Application interrupted by user")
    except Exception as e:
        logger.error(f"❌ Application failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
