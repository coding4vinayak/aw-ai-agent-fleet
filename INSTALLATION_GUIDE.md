# AI Company - Complete Installation & Setup Guide

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.8+ installed
- 4GB+ RAM recommended
- Internet connection for LLM APIs

### 1. Clone and Install
```bash
git clone <repository-url>
cd ai-company
pip install -r requirements.txt
```

### 2. Basic Setup
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys (at minimum, add OpenAI API key)
# OPENAI_API_KEY=your_api_key_here

# Run setup wizard
python setup_ai_company.py
```

### 3. Start the System
```bash
# Start dashboard
python main.py dashboard

# Or assign tasks directly
python assign_task.py "Create a mobile app for task management"
```

**🎉 You're ready! Visit http://localhost:5000 to access the dashboard.**

---

## 📋 Detailed Installation Guide

### Step 1: System Requirements

#### Minimum Requirements
- **OS**: Windows 10+, macOS 10.14+, or Linux
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **Network**: Internet connection for LLM APIs

#### Recommended Requirements
- **Python**: 3.10+
- **RAM**: 16GB for optimal performance
- **Storage**: 10GB for data and logs
- **Database**: PostgreSQL for production use

### Step 2: Environment Setup

#### Option A: Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv ai-company-env

# Activate (Windows)
ai-company-env\Scripts\activate

# Activate (macOS/Linux)
source ai-company-env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Option B: Conda Environment
```bash
# Create conda environment
conda create -n ai-company python=3.10

# Activate environment
conda activate ai-company

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configuration

#### Environment Variables
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your configurations:
   ```bash
   # Required: At least one LLM provider
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Optional: Additional providers
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   AZURE_OPENAI_API_KEY=your_azure_key_here
   AZURE_OPENAI_ENDPOINT=your_azure_endpoint
   
   # Database (SQLite by default)
   DB_TYPE=sqlite
   DB_PATH=data/ai_company.db
   
   # Company settings
   COMPANY_NAME=Your AI Company
   TIMEZONE=UTC
   ```

#### Setup Wizard
Run the interactive setup wizard:
```bash
python setup_ai_company.py
```

The wizard will guide you through:
- Basic company configuration
- LLM provider setup
- Database configuration
- Agent customization
- Integration setup

### Step 4: Database Setup

#### SQLite (Default - No Setup Required)
SQLite is used by default and requires no additional setup.

#### PostgreSQL (Production Recommended)
1. Install PostgreSQL
2. Create database:
   ```sql
   CREATE DATABASE ai_company;
   CREATE USER ai_company_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE ai_company TO ai_company_user;
   ```
3. Update `.env`:
   ```bash
   DB_TYPE=postgresql
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=ai_company
   DB_USER=ai_company_user
   DB_PASSWORD=your_password
   ```

#### MongoDB (Alternative)
1. Install MongoDB
2. Update `.env`:
   ```bash
   DB_TYPE=mongodb
   DB_HOST=localhost
   DB_PORT=27017
   DB_NAME=ai_company
   ```

### Step 5: LLM Provider Setup

#### OpenAI (Recommended)
1. Get API key from https://platform.openai.com/api-keys
2. Add to `.env`:
   ```bash
   OPENAI_API_KEY=sk-your-key-here
   OPENAI_MODEL=gpt-4
   ```

#### Anthropic Claude
1. Get API key from https://console.anthropic.com/
2. Add to `.env`:
   ```bash
   ANTHROPIC_API_KEY=your-key-here
   ANTHROPIC_MODEL=claude-3-sonnet-20240229
   ```

#### Azure OpenAI
1. Set up Azure OpenAI resource
2. Add to `.env`:
   ```bash
   AZURE_OPENAI_API_KEY=your-key-here
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_DEPLOYMENT=your-deployment-name
   ```

#### Ollama (Local/Free)
1. Install Ollama from https://ollama.ai/
2. Pull a model:
   ```bash
   ollama pull llama2
   ```
3. Add to `.env`:
   ```bash
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama2
   ```

### Step 6: Testing Installation

#### Basic Test
```bash
# Test core functionality
python -c "from core.agent_framework import BaseAIAgent; print('✅ Core framework working')"

# Test LLM integration
python -c "from core.llm_integration import llm_manager; print('✅ LLM integration working')"

# Test data manager
python -c "from core.data_manager import data_manager; print('✅ Data manager working')"
```

#### Full System Test
```bash
# Run simple demo
python run_simple_demo.py

# Test task assignment
python assign_task.py "Test the AI company system"
```

### Step 7: Starting the System

#### Dashboard Mode (Web Interface)
```bash
python main.py dashboard
```
Access at: http://localhost:5000

#### Interactive Mode (Command Line)
```bash
python main.py interactive
```

#### Demo Mode (Showcase)
```bash
python main.py demo
```

---

## 🔧 Advanced Configuration

### Custom LLM Integration

#### Adding Custom Provider
1. Create provider class in `core/llm_integration.py`
2. Register in LLM manager
3. Add configuration in settings

#### Example Custom Provider
```python
class CustomProvider(BaseLLMProvider):
    async def generate_response(self, messages, **kwargs):
        # Your custom implementation
        return response
```

### Agent Customization

#### Custom Agent Roles
1. Add role to `AgentRole` enum
2. Create agent class extending `AdvancedAIAgent`
3. Configure in settings

#### Custom System Prompts
Edit agent configurations in the settings interface or directly in config files.

### Database Optimization

#### PostgreSQL Performance
```sql
-- Recommended indexes
CREATE INDEX idx_data_records_type ON data_records(type);
CREATE INDEX idx_data_records_created_at ON data_records(created_at);

-- Connection pooling
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_buffers = '256MB';
```

#### Redis Caching
```bash
# Install Redis
# Ubuntu/Debian
sudo apt install redis-server

# macOS
brew install redis

# Configure in .env
REDIS_HOST=localhost
REDIS_PORT=6379
CACHE_ENABLED=true
```

### Security Configuration

#### JWT Security
```bash
# Generate secure JWT secret
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Add to .env
JWT_SECRET_KEY=your_generated_secret
```

#### API Rate Limiting
```bash
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_BURST=200
```

#### HTTPS Setup
```bash
# Generate SSL certificate
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365

# Configure in .env
SSL_CERT_PATH=path/to/cert.pem
SSL_KEY_PATH=path/to/key.pem
```

---

## 🐳 Docker Deployment

### Docker Compose Setup
```yaml
version: '3.8'
services:
  ai-company:
    build: .
    ports:
      - "5000:5000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DB_TYPE=postgresql
      - DB_HOST=postgres
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: ai_company
      POSTGRES_USER: ai_company_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Build and Run
```bash
# Build image
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f ai-company
```

---

## 🚀 Production Deployment

### Cloud Deployment Options

#### AWS Deployment
- **Compute**: EC2 or ECS
- **Database**: RDS PostgreSQL
- **Cache**: ElastiCache Redis
- **Storage**: S3
- **Load Balancer**: ALB

#### Azure Deployment
- **Compute**: App Service or Container Instances
- **Database**: Azure Database for PostgreSQL
- **Cache**: Azure Cache for Redis
- **Storage**: Blob Storage

#### Google Cloud Deployment
- **Compute**: Cloud Run or GKE
- **Database**: Cloud SQL PostgreSQL
- **Cache**: Memorystore Redis
- **Storage**: Cloud Storage

### Environment-Specific Configurations

#### Production Settings
```bash
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING
SSL_REQUIRED=true
SECURE_COOKIES=true
```

#### Monitoring Setup
```bash
# Sentry for error tracking
SENTRY_DSN=your_sentry_dsn

# DataDog for monitoring
DATADOG_API_KEY=your_datadog_key

# Health check endpoint
HEALTH_CHECK_ENABLED=true
```

---

## 🔍 Troubleshooting

### Common Issues

#### "Module not found" errors
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### LLM API errors
```bash
# Check API key validity
# Verify network connectivity
# Check rate limits
```

#### Database connection errors
```bash
# Verify database is running
# Check connection parameters
# Test with database client
```

#### Port already in use
```bash
# Find process using port
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill process or use different port
export PORT=5001
```

### Getting Help

1. **Check logs**: Look in `ai_company.log`
2. **Run diagnostics**: `python -m pytest tests/`
3. **Validate config**: Use setup wizard
4. **Community support**: Create GitHub issue

---

## 📚 Next Steps

After successful installation:

1. **Explore the Dashboard**: http://localhost:5000
2. **Assign Your First Task**: Use the task interface
3. **Customize Agents**: Configure in settings
4. **Set Up Integrations**: Connect external services
5. **Monitor Performance**: Check analytics dashboard

**🎉 Welcome to your AI Company!**
