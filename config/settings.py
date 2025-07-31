"""
AI Company Configuration System
Comprehensive settings for LLMs, data sources, integrations, and customization.
"""

import os
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class LLMProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    AZURE_OPENAI = "azure_openai"
    HUGGINGFACE = "huggingface"
    OLLAMA = "ollama"
    CUSTOM = "custom"

class DatabaseType(Enum):
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    MONGODB = "mongodb"
    REDIS = "redis"

@dataclass
class LLMConfig:
    """Configuration for Language Model providers."""
    provider: LLMProvider
    model_name: str
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 4000
    timeout: int = 30
    retry_attempts: int = 3
    custom_headers: Dict[str, str] = None
    
    def __post_init__(self):
        if self.custom_headers is None:
            self.custom_headers = {}

@dataclass
class DatabaseConfig:
    """Database configuration."""
    type: DatabaseType
    host: str = "localhost"
    port: int = 5432
    database: str = "ai_company"
    username: str = "admin"
    password: str = ""
    ssl_mode: str = "prefer"
    connection_pool_size: int = 10
    max_overflow: int = 20

@dataclass
class AgentConfig:
    """Configuration for individual AI agents."""
    agent_id: str
    role: str
    name: str
    llm_config: str  # Reference to LLM config name
    system_prompt: str
    temperature: float = 0.7
    max_context_length: int = 8000
    memory_enabled: bool = True
    tools_enabled: List[str] = None
    custom_instructions: str = ""
    
    def __post_init__(self):
        if self.tools_enabled is None:
            self.tools_enabled = []

@dataclass
class IntegrationConfig:
    """External service integrations."""
    name: str
    type: str  # slack, discord, email, webhook, etc.
    enabled: bool = True
    api_key: Optional[str] = None
    webhook_url: Optional[str] = None
    settings: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.settings is None:
            self.settings = {}

class AICompanySettings:
    """Main settings manager for the AI company."""
    
    def __init__(self, config_file: str = "config/ai_company_config.json"):
        self.config_file = config_file
        self.llm_configs: Dict[str, LLMConfig] = {}
        self.database_config: DatabaseConfig = None
        self.agent_configs: Dict[str, AgentConfig] = {}
        self.integration_configs: Dict[str, IntegrationConfig] = {}
        self.general_settings: Dict[str, Any] = {}
        
        # Load configuration
        self.load_config()
        
        # Set defaults if not loaded
        if not self.llm_configs:
            self._set_default_llm_configs()
        if not self.database_config:
            self._set_default_database_config()
        if not self.general_settings:
            self._set_default_general_settings()
    
    def _set_default_llm_configs(self):
        """Set default LLM configurations."""
        self.llm_configs = {
            "openai_gpt4": LLMConfig(
                provider=LLMProvider.OPENAI,
                model_name="gpt-4",
                api_key=os.getenv("OPENAI_API_KEY"),
                temperature=0.7,
                max_tokens=4000
            ),
            "anthropic_claude": LLMConfig(
                provider=LLMProvider.ANTHROPIC,
                model_name="claude-3-sonnet-20240229",
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                temperature=0.7,
                max_tokens=4000
            ),
            "azure_gpt4": LLMConfig(
                provider=LLMProvider.AZURE_OPENAI,
                model_name="gpt-4",
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
                temperature=0.7,
                max_tokens=4000
            ),
            "ollama_local": LLMConfig(
                provider=LLMProvider.OLLAMA,
                model_name="llama2",
                api_base="http://localhost:11434",
                temperature=0.7,
                max_tokens=4000
            )
        }
    
    def _set_default_database_config(self):
        """Set default database configuration."""
        self.database_config = DatabaseConfig(
            type=DatabaseType.POSTGRESQL,
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            database=os.getenv("DB_NAME", "ai_company"),
            username=os.getenv("DB_USER", "admin"),
            password=os.getenv("DB_PASSWORD", ""),
        )
    
    def _set_default_general_settings(self):
        """Set default general settings."""
        self.general_settings = {
            "company_name": "AI Company",
            "timezone": "UTC",
            "log_level": "INFO",
            "max_concurrent_tasks": 10,
            "task_timeout_minutes": 60,
            "auto_save_interval": 300,  # 5 minutes
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
    
    def add_llm_config(self, name: str, config: LLMConfig):
        """Add a new LLM configuration."""
        self.llm_configs[name] = config
        self.save_config()
    
    def add_agent_config(self, config: AgentConfig):
        """Add a new agent configuration."""
        self.agent_configs[config.agent_id] = config
        self.save_config()
    
    def add_integration_config(self, config: IntegrationConfig):
        """Add a new integration configuration."""
        self.integration_configs[config.name] = config
        self.save_config()
    
    def get_llm_config(self, name: str) -> Optional[LLMConfig]:
        """Get LLM configuration by name."""
        return self.llm_configs.get(name)
    
    def get_agent_config(self, agent_id: str) -> Optional[AgentConfig]:
        """Get agent configuration by ID."""
        return self.agent_configs.get(agent_id)
    
    def get_integration_config(self, name: str) -> Optional[IntegrationConfig]:
        """Get integration configuration by name."""
        return self.integration_configs.get(name)
    
    def update_general_setting(self, key: str, value: Any):
        """Update a general setting."""
        keys = key.split('.')
        current = self.general_settings
        
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = value
        self.save_config()
    
    def get_general_setting(self, key: str, default: Any = None) -> Any:
        """Get a general setting value."""
        keys = key.split('.')
        current = self.general_settings
        
        try:
            for k in keys:
                current = current[k]
            return current
        except (KeyError, TypeError):
            return default
    
    def load_config(self):
        """Load configuration from file."""
        if not os.path.exists(self.config_file):
            return
        
        try:
            with open(self.config_file, 'r') as f:
                data = json.load(f)
            
            # Load LLM configs
            if 'llm_configs' in data:
                for name, config_data in data['llm_configs'].items():
                    config_data['provider'] = LLMProvider(config_data['provider'])
                    self.llm_configs[name] = LLMConfig(**config_data)
            
            # Load database config
            if 'database_config' in data:
                db_data = data['database_config']
                db_data['type'] = DatabaseType(db_data['type'])
                self.database_config = DatabaseConfig(**db_data)
            
            # Load agent configs
            if 'agent_configs' in data:
                for agent_id, config_data in data['agent_configs'].items():
                    self.agent_configs[agent_id] = AgentConfig(**config_data)
            
            # Load integration configs
            if 'integration_configs' in data:
                for name, config_data in data['integration_configs'].items():
                    self.integration_configs[name] = IntegrationConfig(**config_data)
            
            # Load general settings
            if 'general_settings' in data:
                self.general_settings = data['general_settings']
                
        except Exception as e:
            print(f"Error loading config: {e}")
    
    def save_config(self):
        """Save configuration to file."""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        
        data = {
            'llm_configs': {
                name: {**asdict(config), 'provider': config.provider.value}
                for name, config in self.llm_configs.items()
            },
            'database_config': {
                **asdict(self.database_config),
                'type': self.database_config.type.value
            } if self.database_config else None,
            'agent_configs': {
                agent_id: asdict(config)
                for agent_id, config in self.agent_configs.items()
            },
            'integration_configs': {
                name: asdict(config)
                for name, config in self.integration_configs.items()
            },
            'general_settings': self.general_settings
        }
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def export_config(self, export_file: str):
        """Export configuration to a different file."""
        original_file = self.config_file
        self.config_file = export_file
        self.save_config()
        self.config_file = original_file
    
    def import_config(self, import_file: str):
        """Import configuration from a file."""
        original_file = self.config_file
        self.config_file = import_file
        self.load_config()
        self.config_file = original_file
        self.save_config()
    
    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        self.llm_configs = {}
        self.database_config = None
        self.agent_configs = {}
        self.integration_configs = {}
        self.general_settings = {}
        
        self._set_default_llm_configs()
        self._set_default_database_config()
        self._set_default_general_settings()
        
        self.save_config()
    
    def validate_config(self) -> List[str]:
        """Validate configuration and return list of issues."""
        issues = []
        
        # Validate LLM configs
        for name, config in self.llm_configs.items():
            if not config.model_name:
                issues.append(f"LLM config '{name}' missing model_name")
            if config.provider in [LLMProvider.OPENAI, LLMProvider.ANTHROPIC] and not config.api_key:
                issues.append(f"LLM config '{name}' missing API key")
        
        # Validate database config
        if self.database_config:
            if not self.database_config.host:
                issues.append("Database config missing host")
            if not self.database_config.database:
                issues.append("Database config missing database name")
        
        # Validate agent configs
        for agent_id, config in self.agent_configs.items():
            if config.llm_config not in self.llm_configs:
                issues.append(f"Agent '{agent_id}' references unknown LLM config '{config.llm_config}'")
        
        return issues

# Global settings instance
settings = AICompanySettings()
