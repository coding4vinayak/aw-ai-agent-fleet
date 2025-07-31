"""
Custom LLM Integration System
Supports multiple LLM providers with unified interface.
"""

import asyncio
import aiohttp
import json
import time
from typing import Dict, List, Any, Optional, AsyncGenerator
from abc import ABC, abstractmethod
import logging

from config.settings import LLMConfig, LLMProvider, settings

logger = logging.getLogger(__name__)

class BaseLLMProvider(ABC):
    """Base class for LLM providers."""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.config.timeout),
            headers=self.config.custom_headers
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    @abstractmethod
    async def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate response from messages."""
        pass
    
    @abstractmethod
    async def stream_response(self, messages: List[Dict[str, str]], **kwargs) -> AsyncGenerator[str, None]:
        """Stream response from messages."""
        pass

class OpenAIProvider(BaseLLMProvider):
    """OpenAI API provider."""
    
    async def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        url = f"{self.config.api_base or 'https://api.openai.com/v1'}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.config.model_name,
            "messages": messages,
            "temperature": kwargs.get("temperature", self.config.temperature),
            "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
            "stream": False
        }
        
        for attempt in range(self.config.retry_attempts):
            try:
                async with self.session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data["choices"][0]["message"]["content"]
                    else:
                        error_text = await response.text()
                        logger.error(f"OpenAI API error: {response.status} - {error_text}")
                        if attempt == self.config.retry_attempts - 1:
                            raise Exception(f"OpenAI API error: {response.status}")
            except Exception as e:
                if attempt == self.config.retry_attempts - 1:
                    raise e
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
    
    async def stream_response(self, messages: List[Dict[str, str]], **kwargs) -> AsyncGenerator[str, None]:
        url = f"{self.config.api_base or 'https://api.openai.com/v1'}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.config.model_name,
            "messages": messages,
            "temperature": kwargs.get("temperature", self.config.temperature),
            "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
            "stream": True
        }
        
        async with self.session.post(url, headers=headers, json=payload) as response:
            async for line in response.content:
                if line:
                    line_str = line.decode('utf-8').strip()
                    if line_str.startswith('data: '):
                        data_str = line_str[6:]
                        if data_str != '[DONE]':
                            try:
                                data = json.loads(data_str)
                                if 'choices' in data and data['choices']:
                                    delta = data['choices'][0].get('delta', {})
                                    if 'content' in delta:
                                        yield delta['content']
                            except json.JSONDecodeError:
                                continue

class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude API provider."""
    
    async def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        url = f"{self.config.api_base or 'https://api.anthropic.com'}/v1/messages"
        
        headers = {
            "x-api-key": self.config.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        # Convert messages format for Anthropic
        system_message = ""
        user_messages = []
        
        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                user_messages.append(msg)
        
        payload = {
            "model": self.config.model_name,
            "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
            "temperature": kwargs.get("temperature", self.config.temperature),
            "messages": user_messages
        }
        
        if system_message:
            payload["system"] = system_message
        
        for attempt in range(self.config.retry_attempts):
            try:
                async with self.session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data["content"][0]["text"]
                    else:
                        error_text = await response.text()
                        logger.error(f"Anthropic API error: {response.status} - {error_text}")
                        if attempt == self.config.retry_attempts - 1:
                            raise Exception(f"Anthropic API error: {response.status}")
            except Exception as e:
                if attempt == self.config.retry_attempts - 1:
                    raise e
                await asyncio.sleep(2 ** attempt)
    
    async def stream_response(self, messages: List[Dict[str, str]], **kwargs) -> AsyncGenerator[str, None]:
        # Anthropic streaming implementation
        # Similar to generate_response but with stream=True
        yield "Streaming not implemented for Anthropic yet"

class OllamaProvider(BaseLLMProvider):
    """Ollama local LLM provider."""
    
    async def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        url = f"{self.config.api_base}/api/chat"
        
        payload = {
            "model": self.config.model_name,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", self.config.temperature),
                "num_predict": kwargs.get("max_tokens", self.config.max_tokens)
            }
        }
        
        async with self.session.post(url, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                return data["message"]["content"]
            else:
                error_text = await response.text()
                raise Exception(f"Ollama error: {response.status} - {error_text}")
    
    async def stream_response(self, messages: List[Dict[str, str]], **kwargs) -> AsyncGenerator[str, None]:
        url = f"{self.config.api_base}/api/chat"
        
        payload = {
            "model": self.config.model_name,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": kwargs.get("temperature", self.config.temperature),
                "num_predict": kwargs.get("max_tokens", self.config.max_tokens)
            }
        }
        
        async with self.session.post(url, json=payload) as response:
            async for line in response.content:
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        if 'message' in data and 'content' in data['message']:
                            yield data['message']['content']
                    except json.JSONDecodeError:
                        continue

class CustomProvider(BaseLLMProvider):
    """Custom LLM provider for any API."""
    
    async def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        # Custom implementation based on config
        url = self.config.api_base
        
        headers = {"Content-Type": "application/json"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        
        payload = {
            "messages": messages,
            "temperature": kwargs.get("temperature", self.config.temperature),
            "max_tokens": kwargs.get("max_tokens", self.config.max_tokens)
        }
        
        async with self.session.post(url, headers=headers, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                # Customize this based on your API response format
                return data.get("response", data.get("content", str(data)))
            else:
                error_text = await response.text()
                raise Exception(f"Custom API error: {response.status} - {error_text}")
    
    async def stream_response(self, messages: List[Dict[str, str]], **kwargs) -> AsyncGenerator[str, None]:
        yield "Custom streaming implementation needed"

class LLMManager:
    """Manager for all LLM providers."""
    
    def __init__(self):
        self.providers = {
            LLMProvider.OPENAI: OpenAIProvider,
            LLMProvider.ANTHROPIC: AnthropicProvider,
            LLMProvider.OLLAMA: OllamaProvider,
            LLMProvider.CUSTOM: CustomProvider
        }
        self.active_providers: Dict[str, BaseLLMProvider] = {}
    
    def get_provider(self, config_name: str) -> BaseLLMProvider:
        """Get or create LLM provider instance."""
        if config_name not in self.active_providers:
            config = settings.get_llm_config(config_name)
            if not config:
                raise ValueError(f"LLM config '{config_name}' not found")
            
            provider_class = self.providers.get(config.provider)
            if not provider_class:
                raise ValueError(f"Provider '{config.provider}' not supported")
            
            self.active_providers[config_name] = provider_class(config)
        
        return self.active_providers[config_name]
    
    async def generate_response(self, config_name: str, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate response using specified LLM config."""
        provider = self.get_provider(config_name)
        
        async with provider:
            return await provider.generate_response(messages, **kwargs)
    
    async def stream_response(self, config_name: str, messages: List[Dict[str, str]], **kwargs) -> AsyncGenerator[str, None]:
        """Stream response using specified LLM config."""
        provider = self.get_provider(config_name)
        
        async with provider:
            async for chunk in provider.stream_response(messages, **kwargs):
                yield chunk
    
    async def test_connection(self, config_name: str) -> Dict[str, Any]:
        """Test connection to LLM provider."""
        try:
            start_time = time.time()
            
            test_messages = [
                {"role": "user", "content": "Hello, please respond with 'Connection test successful'"}
            ]
            
            response = await self.generate_response(config_name, test_messages)
            
            end_time = time.time()
            
            return {
                "success": True,
                "response_time": end_time - start_time,
                "response": response[:100] + "..." if len(response) > 100 else response
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def list_available_configs(self) -> List[str]:
        """List all available LLM configurations."""
        return list(settings.llm_configs.keys())
    
    def add_custom_provider(self, provider_type: str, provider_class: type):
        """Add custom provider type."""
        self.providers[provider_type] = provider_class

# Global LLM manager instance
llm_manager = LLMManager()
