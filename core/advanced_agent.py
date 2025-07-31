"""
Advanced AI Agent with Custom LLM Integration and Memory
Enhanced agent with configurable LLMs, persistent memory, and advanced capabilities.
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

from core.agent_framework import BaseAIAgent, AgentRole, MessageType, Priority, Task, Message
from core.llm_integration import llm_manager
from core.data_manager import data_manager
from config.settings import settings, AgentConfig

logger = logging.getLogger(__name__)

class AdvancedAIAgent(BaseAIAgent):
    """Enhanced AI agent with custom LLM integration and advanced features."""
    
    def __init__(self, agent_id: str, role: AgentRole, name: str, llm_config_name: str = None):
        super().__init__(agent_id, role, name)
        
        # Load agent configuration
        self.config = settings.get_agent_config(agent_id)
        if not self.config and llm_config_name:
            # Create default config if none exists
            self.config = AgentConfig(
                agent_id=agent_id,
                role=role.value,
                name=name,
                llm_config=llm_config_name,
                system_prompt=self._get_default_system_prompt(),
                temperature=0.7,
                max_context_length=8000,
                memory_enabled=True,
                tools_enabled=["web_search", "calculator", "file_access"],
                custom_instructions=""
            )
            settings.add_agent_config(self.config)
        
        # Agent memory and context
        self.memory: Dict[str, Any] = {}
        self.conversation_history: List[Dict[str, str]] = []
        self.context_window: List[Dict[str, str]] = []
        self.tools: Dict[str, Any] = {}
        
        # Performance metrics
        self.metrics = {
            "total_messages": 0,
            "successful_responses": 0,
            "average_response_time": 0.0,
            "last_activity": None,
            "error_count": 0
        }
        
        # Initialize tools
        self._initialize_tools()
    
    def _get_default_system_prompt(self) -> str:
        """Get default system prompt based on role."""
        role_prompts = {
            AgentRole.CEO: "You are a CEO responsible for strategic leadership and decision-making.",
            AgentRole.CTO: "You are a CTO responsible for technology strategy and innovation.",
            AgentRole.CMO: "You are a CMO responsible for marketing strategy and brand management.",
            AgentRole.CFO: "You are a CFO responsible for financial planning and analysis.",
            AgentRole.CHRO: "You are a CHRO responsible for human resources and organizational development.",
            AgentRole.PRODUCT_MANAGER: "You are a Product Manager responsible for product strategy and development.",
            AgentRole.LEAD_ENGINEER: "You are a Lead Engineer responsible for technical architecture and team leadership.",
            AgentRole.FRONTEND_ENGINEER: "You are a Frontend Engineer responsible for user interface development.",
            AgentRole.BACKEND_ENGINEER: "You are a Backend Engineer responsible for server-side development.",
            AgentRole.QA_ENGINEER: "You are a QA Engineer responsible for quality assurance and testing.",
            AgentRole.UX_DESIGNER: "You are a UX Designer responsible for user experience design.",
            AgentRole.UI_DESIGNER: "You are a UI Designer responsible for visual interface design.",
            AgentRole.MARKETING_MANAGER: "You are a Marketing Manager responsible for marketing campaigns and strategy.",
            AgentRole.CONTENT_CREATOR: "You are a Content Creator responsible for creating engaging content.",
            AgentRole.SOCIAL_MEDIA_MANAGER: "You are a Social Media Manager responsible for social media presence.",
            AgentRole.SEO_SPECIALIST: "You are an SEO Specialist responsible for search engine optimization.",
            AgentRole.SALES_MANAGER: "You are a Sales Manager responsible for sales strategy and customer acquisition.",
            AgentRole.CUSTOMER_SUCCESS: "You are a Customer Success Manager responsible for customer satisfaction.",
            AgentRole.OPERATIONS_MANAGER: "You are an Operations Manager responsible for operational efficiency.",
            AgentRole.FINANCE_ANALYST: "You are a Finance Analyst responsible for financial analysis and reporting.",
            AgentRole.LEGAL_ADVISOR: "You are a Legal Advisor responsible for legal compliance and risk management.",
            AgentRole.DATA_ANALYST: "You are a Data Analyst responsible for business intelligence and analytics.",
            AgentRole.SECURITY_SPECIALIST: "You are a Security Specialist responsible for cybersecurity and protection."
        }
        
        base_prompt = role_prompts.get(self.role, "You are an AI assistant.")
        return f"{base_prompt}\n\nYou work as part of an AI company where all roles are performed by AI agents. Collaborate effectively with other agents to achieve business objectives."
    
    def _initialize_tools(self):
        """Initialize available tools for the agent."""
        if not self.config or not self.config.tools_enabled:
            return
        
        for tool_name in self.config.tools_enabled:
            if tool_name == "web_search":
                self.tools["web_search"] = self._web_search_tool
            elif tool_name == "calculator":
                self.tools["calculator"] = self._calculator_tool
            elif tool_name == "file_access":
                self.tools["file_access"] = self._file_access_tool
            elif tool_name == "data_query":
                self.tools["data_query"] = self._data_query_tool
    
    async def _web_search_tool(self, query: str) -> str:
        """Web search tool implementation."""
        # Placeholder implementation
        return f"Web search results for: {query}\n[This would contain actual search results]"
    
    async def _calculator_tool(self, expression: str) -> str:
        """Calculator tool implementation."""
        try:
            # Safe evaluation of mathematical expressions
            result = eval(expression, {"__builtins__": {}}, {})
            return f"Calculation result: {result}"
        except Exception as e:
            return f"Calculation error: {str(e)}"
    
    async def _file_access_tool(self, action: str, file_path: str, content: str = None) -> str:
        """File access tool implementation."""
        if action == "read":
            document = await data_manager.load_document(file_path)
            return document or "File not found"
        elif action == "write" and content:
            success = await data_manager.save_document(file_path, content)
            return "File saved successfully" if success else "Failed to save file"
        else:
            return "Invalid file operation"
    
    async def _data_query_tool(self, query_type: str, filters: Dict[str, Any] = None) -> str:
        """Data query tool implementation."""
        try:
            if query_type == "analytics":
                data = await data_manager.get_analytics_data(filters)
                return json.dumps(data, indent=2)
            else:
                return "Unsupported query type"
        except Exception as e:
            return f"Query error: {str(e)}"
    
    async def load_memory(self):
        """Load agent memory from persistent storage."""
        if not self.config or not self.config.memory_enabled:
            return
        
        memory_data = await data_manager.load_agent_memory(self.agent_id)
        if memory_data:
            self.memory = memory_data.get("memory", {})
            self.conversation_history = memory_data.get("conversation_history", [])
            self.metrics = memory_data.get("metrics", self.metrics)
    
    async def save_memory(self):
        """Save agent memory to persistent storage."""
        if not self.config or not self.config.memory_enabled:
            return
        
        memory_data = {
            "memory": self.memory,
            "conversation_history": self.conversation_history[-100:],  # Keep last 100 messages
            "metrics": self.metrics,
            "last_saved": datetime.now().isoformat()
        }
        
        await data_manager.save_agent_memory(self.agent_id, memory_data)
    
    def _build_context_window(self, new_message: str) -> List[Dict[str, str]]:
        """Build context window for LLM with system prompt and conversation history."""
        context = []
        
        # Add system prompt
        system_prompt = self.config.system_prompt if self.config else self._get_default_system_prompt()
        if self.config and self.config.custom_instructions:
            system_prompt += f"\n\nAdditional Instructions: {self.config.custom_instructions}"
        
        context.append({"role": "system", "content": system_prompt})
        
        # Add relevant memory context
        if self.memory:
            memory_context = self._get_relevant_memory_context(new_message)
            if memory_context:
                context.append({"role": "system", "content": f"Relevant context from memory: {memory_context}"})
        
        # Add recent conversation history
        max_history = (self.config.max_context_length - 1000) // 100 if self.config else 10
        recent_history = self.conversation_history[-max_history:]
        context.extend(recent_history)
        
        # Add current message
        context.append({"role": "user", "content": new_message})
        
        return context
    
    def _get_relevant_memory_context(self, message: str) -> str:
        """Get relevant context from agent memory based on current message."""
        # Simple keyword-based relevance (could be enhanced with embeddings)
        relevant_items = []
        message_lower = message.lower()
        
        for key, value in self.memory.items():
            if any(word in key.lower() for word in message_lower.split()):
                relevant_items.append(f"{key}: {value}")
        
        return "; ".join(relevant_items[:3])  # Return top 3 relevant items
    
    async def generate_response(self, message: str, context: Dict[str, Any] = None) -> str:
        """Generate response using configured LLM."""
        start_time = datetime.now()
        
        try:
            # Build context window
            context_messages = self._build_context_window(message)
            
            # Get LLM configuration
            llm_config_name = self.config.llm_config if self.config else "openai_gpt4"
            
            # Generate response using LLM
            response = await llm_manager.generate_response(
                llm_config_name,
                context_messages,
                temperature=self.config.temperature if self.config else 0.7,
                max_tokens=2000
            )
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": response})
            
            # Update metrics
            response_time = (datetime.now() - start_time).total_seconds()
            self.metrics["total_messages"] += 1
            self.metrics["successful_responses"] += 1
            self.metrics["average_response_time"] = (
                (self.metrics["average_response_time"] * (self.metrics["successful_responses"] - 1) + response_time) /
                self.metrics["successful_responses"]
            )
            self.metrics["last_activity"] = datetime.now().isoformat()
            
            # Save memory
            await self.save_memory()
            
            return response
            
        except Exception as e:
            self.metrics["error_count"] += 1
            logger.error(f"Error generating response for {self.agent_id}: {e}")
            return f"I apologize, but I encountered an error while processing your request: {str(e)}"
    
    async def process_task_with_tools(self, task: Task) -> Dict[str, Any]:
        """Process task with available tools."""
        try:
            # Analyze task to determine if tools are needed
            task_analysis = await self.analyze_task_requirements(task)
            
            # Execute task with tools if needed
            if task_analysis.get("tools_needed"):
                return await self.execute_task_with_tools(task, task_analysis["tools_needed"])
            else:
                # Regular task processing
                response = await self.generate_response(f"Please complete this task: {task.description}")
                return {
                    "status": "completed",
                    "result": response,
                    "tools_used": [],
                    "execution_time": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error processing task with tools: {e}")
            return {
                "status": "error",
                "error": str(e),
                "execution_time": datetime.now().isoformat()
            }
    
    async def analyze_task_requirements(self, task: Task) -> Dict[str, Any]:
        """Analyze task to determine required tools."""
        analysis_prompt = f"""
        Analyze this task and determine if any tools are needed:
        Task: {task.description}
        
        Available tools: {list(self.tools.keys())}
        
        Respond with JSON indicating which tools are needed and why.
        """
        
        response = await self.generate_response(analysis_prompt)
        
        # Parse response to extract tool requirements
        # This is a simplified implementation
        tools_needed = []
        if "web_search" in response.lower() and "web_search" in self.tools:
            tools_needed.append("web_search")
        if "calculator" in response.lower() and "calculator" in self.tools:
            tools_needed.append("calculator")
        if "file" in response.lower() and "file_access" in self.tools:
            tools_needed.append("file_access")
        
        return {
            "tools_needed": tools_needed,
            "analysis": response
        }
    
    async def execute_task_with_tools(self, task: Task, tools_needed: List[str]) -> Dict[str, Any]:
        """Execute task using specified tools."""
        results = []
        tools_used = []
        
        for tool_name in tools_needed:
            if tool_name in self.tools:
                try:
                    # This is a simplified tool execution
                    # In practice, you'd parse the task to extract tool parameters
                    if tool_name == "web_search":
                        result = await self.tools[tool_name](task.title)
                    elif tool_name == "calculator":
                        result = await self.tools[tool_name]("1+1")  # Placeholder
                    else:
                        result = await self.tools[tool_name]("default_action")
                    
                    results.append(result)
                    tools_used.append(tool_name)
                    
                except Exception as e:
                    results.append(f"Tool {tool_name} error: {str(e)}")
        
        # Generate final response incorporating tool results
        final_prompt = f"""
        Task: {task.description}
        Tool results: {'; '.join(results)}
        
        Please provide a comprehensive response incorporating the tool results.
        """
        
        final_response = await self.generate_response(final_prompt)
        
        return {
            "status": "completed",
            "result": final_response,
            "tools_used": tools_used,
            "tool_results": results,
            "execution_time": datetime.now().isoformat()
        }
    
    def update_memory(self, key: str, value: Any):
        """Update agent memory with new information."""
        self.memory[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat(),
            "type": type(value).__name__
        }
    
    def get_memory(self, key: str) -> Any:
        """Retrieve information from agent memory."""
        memory_item = self.memory.get(key)
        return memory_item["value"] if memory_item else None
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics."""
        return {
            **self.metrics,
            "memory_size": len(self.memory),
            "conversation_length": len(self.conversation_history),
            "tools_available": list(self.tools.keys()),
            "configuration": {
                "llm_config": self.config.llm_config if self.config else None,
                "temperature": self.config.temperature if self.config else 0.7,
                "memory_enabled": self.config.memory_enabled if self.config else False
            }
        }
    
    async def daily_standup(self) -> Dict[str, Any]:
        """Enhanced daily standup with memory and metrics."""
        base_standup = await super().daily_standup()
        
        # Add advanced metrics
        base_standup.update({
            "performance_metrics": self.get_performance_metrics(),
            "recent_memory_updates": list(self.memory.keys())[-5:],  # Last 5 memory keys
            "tools_used_today": self._get_tools_used_today(),
            "collaboration_score": self._calculate_collaboration_score()
        })
        
        return base_standup
    
    def _get_tools_used_today(self) -> List[str]:
        """Get tools used today (placeholder implementation)."""
        return list(self.tools.keys())  # Simplified
    
    def _calculate_collaboration_score(self) -> float:
        """Calculate collaboration effectiveness score."""
        # Simplified scoring based on message frequency and success rate
        if self.metrics["total_messages"] == 0:
            return 0.0
        
        success_rate = self.metrics["successful_responses"] / self.metrics["total_messages"]
        activity_score = min(self.metrics["total_messages"] / 100, 1.0)  # Normalize to 1.0
        
        return (success_rate * 0.7 + activity_score * 0.3) * 10  # Scale to 10
