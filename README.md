# 🚀 Company AI Assistant - Gemini & Cloudflare Integration

Trợ lý AI nội bộ hỗ trợ công việc cho công ty, được tích hợp với Google Gemini AI và Cloudflare.

## ✨ Features

### AI Capabilities (Powered by Google Gemini)
- ✅ Natural Vietnamese conversation
- ✅ Context-aware responses  
- ✅ Smart intent detection
- ✅ Knowledge extraction from CSV files
- ✅ Streaming responses
- ✅ Multi-turn dialogue support
- ✅ Time queries
- ✅ Basic translation support

### Performance (Powered by Cloudflare)
- ✅ Global CDN distribution
- ✅ Edge computing
- ✅ DDoS protection
- ✅ SSL/TLS termination
- ✅ API proxy with security headers
- ✅ CORS handling

### User Experience
- ✅ Real-time chat interface
- ✅ File upload (CSV)
- ✅ Conversation history
- ✅ Loading indicators
- ✅ Error handling
- ✅ Responsive design

## 🏗️ Architecture

```
┌─────────────────┐
│   Frontend      │
│  (React + TS)   │
│  Cloudflare     │
│     Pages       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Cloudflare    │
│    Workers      │
│  (API Proxy)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Backend      │
│   (FastAPI)     │
│  Gemini AI      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Redis       │
│   (Caching)     │
└─────────────────┘
```

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Google Gemini API Key
- Cloudflare Account (optional for deployment)

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/tekdela/company-ai-assistant.git
cd company-ai-assistant
```

### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Run backend
python -m app.main
```

Backend will be available at: http://localhost:8000

API Documentation: http://localhost:8000/docs

### 3. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at: http://localhost:3000

### 4. Using Docker Compose (Recommended)

```bash
# Copy environment file
cp backend/.env.example backend/.env
# Edit backend/.env and add your GEMINI_API_KEY

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔑 Environment Variables

### Backend (.env)

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional
CLOUDFLARE_API_TOKEN=your_cloudflare_api_token
CLOUDFLARE_ZONE_ID=your_zone_id
CLOUDFLARE_ACCOUNT_ID=your_account_id

BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

REDIS_URL=redis://localhost:6379
ENVIRONMENT=development
```

### Get Gemini API Key

1. Visit https://makersuite.google.com/app/apikey
2. Create new API key
3. Copy and paste into `.env` file

## 📚 API Documentation

### Chat Endpoints

#### Send Message
```http
POST /api/chat/message
Content-Type: application/json

{
  "message": "Xin chào",
  "session_id": "default",
  "stream": false
}
```

Response:
```json
{
  "response": "Xin chào! Tôi là trợ lý AI của công ty...",
  "metadata": {
    "intent": "greeting",
    "confidence": 0.9,
    "timestamp": "10:30:00, 19/11/2024"
  },
  "session_id": "default"
}
```

#### Stream Message
```http
POST /api/chat/stream
Content-Type: application/json

{
  "message": "Mấy giờ rồi?",
  "session_id": "default"
}
```

#### Get History
```http
GET /api/chat/history/{session_id}
```

#### Clear History
```http
DELETE /api/chat/history/{session_id}
```

### Upload Endpoints

#### Upload CSV
```http
POST /api/upload/csv
Content-Type: multipart/form-data

file: <CSV file>
```

#### Get Knowledge Stats
```http
GET /api/upload/stats
```

### System Endpoints

#### Health Check
```http
GET /api/health
```

#### Root
```http
GET /api/
```

## 🎯 Usage Examples

### Chat with AI

```python
import requests

response = requests.post('http://localhost:8000/api/chat/message', json={
    'message': 'Xin chào!',
    'session_id': 'user123'
})

print(response.json()['response'])
```

### Upload CSV

```python
import requests

with open('data.csv', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/api/upload/csv', files=files)
    
print(response.json())
```

### Query Knowledge Base

After uploading CSV:

```python
response = requests.post('http://localhost:8000/api/chat/message', json={
    'message': 'Tìm thông tin về nhân viên X',
    'session_id': 'user123'
})

print(response.json()['response'])
```

## 🌐 Cloudflare Deployment

### Deploy Frontend to Cloudflare Pages

```bash
# Install Wrangler CLI
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Build frontend
cd frontend
npm run build

# Deploy
wrangler pages publish dist --project-name=company-ai-assistant
```

### Deploy Cloudflare Workers

```bash
# Deploy API proxy worker
wrangler publish workers/api-proxy.js
```

### Configure Environment Variables

In Cloudflare Dashboard:
1. Go to Workers & Pages
2. Select your project
3. Settings > Environment Variables
4. Add:
   - `BACKEND_URL`: Your backend API URL
   - `GEMINI_API_KEY`: Your Gemini API key

## 🔒 Security Features

- ✅ CORS configuration
- ✅ Security headers (X-Frame-Options, X-Content-Type-Options, etc.)
- ✅ Input validation
- ✅ Rate limiting (via Cloudflare)
- ✅ DDoS protection (via Cloudflare)
- ✅ SSL/TLS encryption (via Cloudflare)

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 📊 Performance Targets

- Response Time: < 200ms (95th percentile)
- Uptime: 99.9%
- Concurrent Users: 1000+
- File Upload: Up to 50MB
- Global Latency: < 100ms (with Cloudflare CDN)

## 🛠️ Development

### Project Structure

```
company-ai-assistant/
├── backend/
│   ├── app/
│   │   ├── services/
│   │   │   ├── gemini_service.py      # Gemini AI integration
│   │   │   ├── ai_service.py          # Main AI orchestration
│   │   │   ├── knowledge_service.py   # CSV knowledge base
│   │   │   ├── time_service.py        # Time queries
│   │   │   └── translation_service.py # Translation
│   │   ├── routes/
│   │   │   ├── chat.py               # Chat endpoints
│   │   │   ├── upload.py             # Upload endpoints
│   │   │   └── health.py             # Health check
│   │   ├── models/
│   │   │   └── schemas.py            # Pydantic models
│   │   └── main.py                   # FastAPI app
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── GeminiChat.tsx        # Main chat component
│   │   ├── services/
│   │   │   └── gemini-api.ts         # API service
│   │   ├── types/
│   │   │   └── api.ts                # TypeScript types
│   │   ├── styles/
│   │   │   └── App.css               # Styles
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── workers/
│   └── api-proxy.js                  # Cloudflare Worker
├── functions/
│   └── api/
│       └── chat.js                   # Cloudflare Function
├── .github/
│   └── workflows/
│       ├── deploy-cloudflare.yml     # Cloudflare deployment
│       └── backend-ci.yml            # Backend CI
├── docker-compose.yml
├── docker-compose.prod.yml
├── wrangler.toml
└── README.md
```

### Add New Intent

1. Update `gemini_service.py` intent analysis
2. Add handler in `ai_service.py`
3. Test with example queries

### Add New Service

1. Create service file in `backend/app/services/`
2. Inject into AIService in `main.py`
3. Use in intent handlers

## 🐛 Troubleshooting

### Backend won't start

```bash
# Check Python version
python --version  # Should be 3.11+

# Check if port 8000 is in use
lsof -i :8000

# Check environment variables
cat backend/.env
```

### Frontend won't build

```bash
# Clear node modules
rm -rf node_modules package-lock.json
npm install

# Check Node version
node --version  # Should be 18+
```

### Gemini API errors

- Check API key is valid
- Verify API quota/limits
- Check network connectivity
- Review error messages in logs

## 📝 License

MIT License

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

## 📧 Support

For issues and questions:
- Open a GitHub Issue
- Email: support@yourcompany.com

## 🎉 Acknowledgments

- Google Gemini AI
- Cloudflare
- FastAPI
- React
- Vite

---

Made with ❤️ by TekDela
