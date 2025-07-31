"""
Advanced Data Management System
Handles databases, file storage, caching, and data processing.
"""

import asyncio
import json
import os
import sqlite3
import aiofiles
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
import logging

try:
    import asyncpg
    import aioredis
    import motor.motor_asyncio
    ADVANCED_DB_AVAILABLE = True
except ImportError:
    ADVANCED_DB_AVAILABLE = False

from config.settings import DatabaseConfig, DatabaseType, settings

logger = logging.getLogger(__name__)

@dataclass
class DataRecord:
    """Generic data record."""
    id: str
    type: str
    data: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class BaseDataStore:
    """Base class for data stores."""
    
    async def connect(self):
        """Connect to data store."""
        pass
    
    async def disconnect(self):
        """Disconnect from data store."""
        pass
    
    async def save(self, record: DataRecord) -> bool:
        """Save a data record."""
        pass
    
    async def load(self, record_id: str) -> Optional[DataRecord]:
        """Load a data record by ID."""
        pass
    
    async def query(self, filters: Dict[str, Any]) -> List[DataRecord]:
        """Query data records with filters."""
        pass
    
    async def delete(self, record_id: str) -> bool:
        """Delete a data record."""
        pass

class SQLiteDataStore(BaseDataStore):
    """SQLite data store implementation."""
    
    def __init__(self, db_path: str = "data/ai_company.db"):
        self.db_path = db_path
        self.connection = None
    
    async def connect(self):
        """Connect to SQLite database."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.connection = sqlite3.connect(self.db_path)
        
        # Create tables
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS data_records (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                data TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                metadata TEXT
            )
        """)
        
        self.connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_type ON data_records(type)
        """)
        
        self.connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_created_at ON data_records(created_at)
        """)
        
        self.connection.commit()
    
    async def disconnect(self):
        """Disconnect from SQLite database."""
        if self.connection:
            self.connection.close()
    
    async def save(self, record: DataRecord) -> bool:
        """Save a data record to SQLite."""
        try:
            self.connection.execute("""
                INSERT OR REPLACE INTO data_records 
                (id, type, data, created_at, updated_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                record.id,
                record.type,
                json.dumps(record.data),
                record.created_at.isoformat(),
                record.updated_at.isoformat(),
                json.dumps(record.metadata)
            ))
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Error saving record: {e}")
            return False
    
    async def load(self, record_id: str) -> Optional[DataRecord]:
        """Load a data record from SQLite."""
        try:
            cursor = self.connection.execute(
                "SELECT * FROM data_records WHERE id = ?", (record_id,)
            )
            row = cursor.fetchone()
            
            if row:
                return DataRecord(
                    id=row[0],
                    type=row[1],
                    data=json.loads(row[2]),
                    created_at=datetime.fromisoformat(row[3]),
                    updated_at=datetime.fromisoformat(row[4]),
                    metadata=json.loads(row[5]) if row[5] else {}
                )
            return None
        except Exception as e:
            logger.error(f"Error loading record: {e}")
            return None
    
    async def query(self, filters: Dict[str, Any]) -> List[DataRecord]:
        """Query data records with filters."""
        try:
            query = "SELECT * FROM data_records WHERE 1=1"
            params = []
            
            if 'type' in filters:
                query += " AND type = ?"
                params.append(filters['type'])
            
            if 'created_after' in filters:
                query += " AND created_at > ?"
                params.append(filters['created_after'].isoformat())
            
            if 'created_before' in filters:
                query += " AND created_at < ?"
                params.append(filters['created_before'].isoformat())
            
            query += " ORDER BY created_at DESC"
            
            if 'limit' in filters:
                query += " LIMIT ?"
                params.append(filters['limit'])
            
            cursor = self.connection.execute(query, params)
            rows = cursor.fetchall()
            
            records = []
            for row in rows:
                records.append(DataRecord(
                    id=row[0],
                    type=row[1],
                    data=json.loads(row[2]),
                    created_at=datetime.fromisoformat(row[3]),
                    updated_at=datetime.fromisoformat(row[4]),
                    metadata=json.loads(row[5]) if row[5] else {}
                ))
            
            return records
        except Exception as e:
            logger.error(f"Error querying records: {e}")
            return []
    
    async def delete(self, record_id: str) -> bool:
        """Delete a data record from SQLite."""
        try:
            self.connection.execute("DELETE FROM data_records WHERE id = ?", (record_id,))
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Error deleting record: {e}")
            return False

class FileDataStore(BaseDataStore):
    """File-based data store for documents and media."""
    
    def __init__(self, base_path: str = "data/files"):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)
    
    async def save_file(self, file_id: str, content: bytes, metadata: Dict[str, Any] = None) -> bool:
        """Save file content."""
        try:
            file_path = os.path.join(self.base_path, file_id)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(content)
            
            # Save metadata
            if metadata:
                metadata_path = file_path + ".meta"
                async with aiofiles.open(metadata_path, 'w') as f:
                    await f.write(json.dumps(metadata, default=str))
            
            return True
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            return False
    
    async def load_file(self, file_id: str) -> Optional[bytes]:
        """Load file content."""
        try:
            file_path = os.path.join(self.base_path, file_id)
            if os.path.exists(file_path):
                async with aiofiles.open(file_path, 'rb') as f:
                    return await f.read()
            return None
        except Exception as e:
            logger.error(f"Error loading file: {e}")
            return None
    
    async def load_file_metadata(self, file_id: str) -> Optional[Dict[str, Any]]:
        """Load file metadata."""
        try:
            metadata_path = os.path.join(self.base_path, file_id + ".meta")
            if os.path.exists(metadata_path):
                async with aiofiles.open(metadata_path, 'r') as f:
                    content = await f.read()
                    return json.loads(content)
            return None
        except Exception as e:
            logger.error(f"Error loading file metadata: {e}")
            return None
    
    async def delete_file(self, file_id: str) -> bool:
        """Delete file and metadata."""
        try:
            file_path = os.path.join(self.base_path, file_id)
            metadata_path = file_path + ".meta"
            
            if os.path.exists(file_path):
                os.remove(file_path)
            
            if os.path.exists(metadata_path):
                os.remove(metadata_path)
            
            return True
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            return False

class CacheManager:
    """In-memory cache manager."""
    
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
    
    def _is_expired(self, item: Dict[str, Any]) -> bool:
        """Check if cache item is expired."""
        return datetime.now() > item['expires_at']
    
    def _cleanup_expired(self):
        """Remove expired items from cache."""
        expired_keys = [
            key for key, item in self.cache.items()
            if self._is_expired(item)
        ]
        for key in expired_keys:
            del self.cache[key]
    
    def get(self, key: str) -> Optional[Any]:
        """Get item from cache."""
        self._cleanup_expired()
        
        if key in self.cache:
            item = self.cache[key]
            if not self._is_expired(item):
                return item['value']
            else:
                del self.cache[key]
        
        return None
    
    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> bool:
        """Set item in cache."""
        self._cleanup_expired()
        
        # Remove oldest items if cache is full
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k]['created_at'])
            del self.cache[oldest_key]
        
        ttl = ttl_seconds or self.ttl_seconds
        self.cache[key] = {
            'value': value,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(seconds=ttl)
        }
        
        return True
    
    def delete(self, key: str) -> bool:
        """Delete item from cache."""
        if key in self.cache:
            del self.cache[key]
            return True
        return False
    
    def clear(self):
        """Clear all cache items."""
        self.cache.clear()
    
    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        self._cleanup_expired()
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hit_rate': 0.95,  # Placeholder
            'memory_usage': f"{len(str(self.cache)) / 1024:.2f} KB"
        }

class DataManager:
    """Main data manager coordinating all data operations."""
    
    def __init__(self):
        self.data_store: BaseDataStore = None
        self.file_store = FileDataStore()
        self.cache = CacheManager(
            max_size=settings.get_general_setting('performance.cache_enabled', 1000),
            ttl_seconds=settings.get_general_setting('performance.cache_ttl_seconds', 3600)
        )
        self.connected = False
    
    async def initialize(self):
        """Initialize data manager with configured data store."""
        db_config = settings.database_config
        
        if db_config.type == DatabaseType.SQLITE:
            self.data_store = SQLiteDataStore(f"data/{db_config.database}.db")
        elif db_config.type == DatabaseType.POSTGRESQL and ADVANCED_DB_AVAILABLE:
            # PostgreSQL implementation would go here
            self.data_store = SQLiteDataStore()  # Fallback for now
        else:
            # Default to SQLite
            self.data_store = SQLiteDataStore()
        
        await self.data_store.connect()
        self.connected = True
        logger.info("Data manager initialized")
    
    async def shutdown(self):
        """Shutdown data manager."""
        if self.data_store:
            await self.data_store.disconnect()
        self.connected = False
        logger.info("Data manager shutdown")
    
    async def save_agent_memory(self, agent_id: str, memory_data: Dict[str, Any]) -> bool:
        """Save agent memory data."""
        record = DataRecord(
            id=f"agent_memory_{agent_id}",
            type="agent_memory",
            data=memory_data,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={"agent_id": agent_id}
        )
        
        success = await self.data_store.save(record)
        if success:
            # Also cache for quick access
            self.cache.set(f"agent_memory_{agent_id}", memory_data)
        
        return success
    
    async def load_agent_memory(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Load agent memory data."""
        # Try cache first
        cached = self.cache.get(f"agent_memory_{agent_id}")
        if cached:
            return cached
        
        # Load from data store
        record = await self.data_store.load(f"agent_memory_{agent_id}")
        if record:
            self.cache.set(f"agent_memory_{agent_id}", record.data)
            return record.data
        
        return None
    
    async def save_task_data(self, task_id: str, task_data: Dict[str, Any]) -> bool:
        """Save task data."""
        record = DataRecord(
            id=f"task_{task_id}",
            type="task",
            data=task_data,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={"task_id": task_id}
        )
        
        return await self.data_store.save(record)
    
    async def load_task_data(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Load task data."""
        record = await self.data_store.load(f"task_{task_id}")
        return record.data if record else None
    
    async def save_conversation(self, conversation_id: str, messages: List[Dict[str, str]]) -> bool:
        """Save conversation history."""
        record = DataRecord(
            id=f"conversation_{conversation_id}",
            type="conversation",
            data={"messages": messages},
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={"conversation_id": conversation_id}
        )
        
        return await self.data_store.save(record)
    
    async def load_conversation(self, conversation_id: str) -> Optional[List[Dict[str, str]]]:
        """Load conversation history."""
        record = await self.data_store.load(f"conversation_{conversation_id}")
        return record.data.get("messages", []) if record else None
    
    async def save_document(self, doc_id: str, content: str, metadata: Dict[str, Any] = None) -> bool:
        """Save document content."""
        content_bytes = content.encode('utf-8')
        return await self.file_store.save_file(doc_id, content_bytes, metadata)
    
    async def load_document(self, doc_id: str) -> Optional[str]:
        """Load document content."""
        content_bytes = await self.file_store.load_file(doc_id)
        return content_bytes.decode('utf-8') if content_bytes else None
    
    async def get_analytics_data(self, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get analytics data for dashboard."""
        filters = filters or {}
        
        # Get recent tasks
        task_filters = {"type": "task", "limit": 100}
        if 'days' in filters:
            task_filters['created_after'] = datetime.now() - timedelta(days=filters['days'])
        
        tasks = await self.data_store.query(task_filters)
        
        # Get agent activities
        memory_filters = {"type": "agent_memory", "limit": 50}
        memories = await self.data_store.query(memory_filters)
        
        return {
            "total_tasks": len(tasks),
            "active_agents": len(memories),
            "recent_activity": len([t for t in tasks if t.created_at > datetime.now() - timedelta(hours=24)]),
            "cache_stats": self.cache.stats()
        }
    
    def generate_id(self, prefix: str = "") -> str:
        """Generate unique ID."""
        timestamp = str(int(datetime.now().timestamp() * 1000))
        hash_obj = hashlib.md5(f"{prefix}{timestamp}".encode())
        return f"{prefix}{hash_obj.hexdigest()[:8]}"

# Global data manager instance
data_manager = DataManager()
