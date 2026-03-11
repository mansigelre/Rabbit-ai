# Sales Insight Automator - Complete Project

A production-ready AI-powered backend service and interactive frontend for processing sales data and generating executive summaries with automatic email delivery.

## 📊 Project Overview

**Sales Insight Automator** is a containerized application that enables teams to:
- Upload CSV/XLSX sales files
- Automatically generate AI-powered executive summaries
- Send summaries directly to stakeholder emails
- Access secure, documented API endpoints

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Sales Insight Automator                   │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────┐         ┌────────────────────────┐ │
│  │   React Frontend     │         │    FastAPI Backend     │ │
│  │  (Port 3000 / 5173)  │◄───────►│   (Port 8000)         │ │
│  │  - File Upload       │         │ - Data Processing     │ │
│  │  - Email Input       │         │ - Swagger API Docs    │ │
│  │  - Real-time Status  │         │ - Rate Limiting       │ │
│  └──────────────────────┘         │ - CORS Protected      │ │
│          △                        └────────────────────────┘ │
│          │                                △                   │
│          │ Docker Network                 │                   │
│          └─────────────────────────────────┘                   │
│                                                               │
│  ┌────────────────────┐  ┌────────────────┐                 │
│  │  Gemini API        │  │  SMTP Service  │                 │
│  │  (Llama Fallback)  │  │  (Gmail/etc)   │                 │
│  └────────────────────┘  └────────────────┘                 │
└──────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Configuration keys (see `.env.example`)

### Local Development with Docker Compose

1. **Clone & Configure**
   ```bash
   cd sales-insight-automator
   
   # Copy environment files
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   
   # Edit .env files with your API keys
   # Required: GEMINI_API_KEY, SMTP credentials
   ```

2. **Start the Application**
   ```bash
   docker-compose up -d
   ```

3. **Access the Application**
   - **Frontend**: http://localhost:3000
   - **API Swagger Docs**: http://localhost:8000/docs
   - **Backend Health**: http://localhost:8000/health

4. **Test the Flow**
   - Use the provided `sales_q1_2026.csv` in the upload form
   - Enter a test email address
   - Check your email for the generated summary

5. **Stop the Application**
   ```bash
   docker-compose down
   ```

## 📋 Environment Configuration

### Backend Configuration
Create `backend/.env`:
```env
ENV=production
PORT=8000

# Frontend CORS URLs
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Google Gemini API for AI summaries
GEMINI_API_KEY=your_gemini_api_key_here

# Email service (Gmail example)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_specific_password

# Security
API_KEY=your_secure_api_key_here

# File constraints
MAX_FILE_SIZE=10485760  # 10MB
```

### Frontend Configuration
Create `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
```

## 🔒 Security Implementation

### Backend Security Features

1. **Rate Limiting**
   - 5 requests per minute per IP
   - Prevents resource abuse and DOS attacks

2. **CORS Protection**
   - Whitelist allowed origins
   - Custom configuration per environment

3. **Input Validation**
   - Email format validation (regex + pydantic)
   - File type validation (only CSV/XLSX)
   - File size limits (10MB max)
   - File name sanitization

4. **Trusted Host Middleware**
   - Restricts request origins
   - Prevents header injection attacks

5. **Data Security**
   - Sensitive data not logged
   - Temporary files are cleaned up
   - No credentials stored in code

6. **API Documentation**
   - Built-in Swagger UI at `/docs`
   - ReDoc at `/redoc`
   - OpenAPI schema available

### Frontend Security

1. **Email Validation**
   - Client-side regex validation
   - HTML5 email input type

2. **File Type Checking**
   - Extension validation
   - MIME type checking

3. **XSS Prevention**
   - React automatic escaping
   - Sanitized error messages

## 🔌 API Endpoints

### Health Check
```bash
GET /health
Response: { "status": "healthy", "timestamp": "2026-03-11T...", "version": "1.0.0" }
```

### Upload & Analyze (Main Endpoint)
```bash
POST /api/v1/analyze
Content-Type: multipart/form-data

Parameters:
- recipient_email (string, required): Recipient email address
- file (file, required): CSV or XLSX file

Response:
{
  "status": "success",
  "message": "Analysis completed",
  "email_sent": true,
  "recipient": "user@example.com",
  "summary_preview": "...",
  "timestamp": "2026-03-11T..."
}
```

### Rate Limiting
- Limit: 5 requests/minute per IP
- Status Code: 429 Too Many Requests when exceeded

## 🏗️ Project Structure

```
sales-insight-automator/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile              # Multi-stage build
│   ├── .env.example            # Configuration template
│   └── uploads/                # Temporary file storage
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx             # Main React component
│   │   ├── App.css             # Styling
│   │   └── main.tsx            # Entry point
│   ├── package.json            # Node dependencies
│   ├── vite.config.ts          # Vite configuration
│   ├── Dockerfile              # Frontend container
│   ├── .env.example            # Configuration template
│   └── index.html              # HTML template
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # GitHub Actions pipeline
│
├── docker-compose.yml          # Full stack orchestration
└── README.md                   # This file
```

## 🔄 Development Workflow

### Local Development (Without Docker)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
export GEMINI_API_KEY=your_key
export SMTP_EMAIL=your_email
python -m uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Building Docker Images

```bash
# Build backend
docker build -t sales-automator-backend:latest ./backend

# Build frontend
docker build -t sales-automator-frontend:latest ./frontend

# Run containers
docker run -p 8000:8000 sales-automator-backend:latest
docker run -p 3000:3000 sales-automator-frontend:latest
```

## 📊 AI Engine Details

### Gemini Integration
- **Model**: Gemini 1.5 Flash (optimized for speed)
- **Prompt**: Contextual analysis with executive focus
- **Fallback**: Automatic basic summary if API unavailable

### Email Delivery
- **Supported Providers**: Gmail, Outlook, Custom SMTP
- **Format**: HTML with professional styling
- **Headers**: Timestamp, file name, sender info

## 📈 CI/CD Pipeline

**GitHub Actions Workflow** (`ci-cd.yml`):

1. **Code Checkout** - Clone repository
2. **Frontend Checks**:
   - Install dependencies
   - Run linter
   - Build production bundle
3. **Backend Checks**:
   - Install dependencies
   - Python syntax validation
   - Code quality checks
4. **Docker Tests**:
   - Build Docker images
   - Verify image integrity
5. **Deployment Ready** - Artifacts prepared

**Trigger Events**:
- Push to `main` branch
- Pull requests to `main`
- Manual workflow dispatch

## 🚢 Deployment Guide

### Deploy to Vercel (Frontend)

1. Push code to GitHub
2. Connect repository to Vercel
3. Set Environment Variables:
   ```
   VITE_API_URL=https://your-backend-url.com
   ```
4. Deploy

### Deploy to Render (Backend)

1. Connect GitHub repository
2. Create New Web Service
3. Set Build Command:
   ```bash
   pip install -r requirements.txt
   ```
4. Set Start Command:
   ```bash
   python -m uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
5. Set Environment Variables from `.env.example`
6. Deploy

## 📝 Testing Sample Data

Use the provided test CSV:
```csv
Date,Product_Category,Region,Units_Sold,Unit_Price,Revenue,Status
2026-01-05,Electronics,North,150,1200,180000,Shipped
2026-01-12,Home Appliances,South,45,450,20250,Shipped
2026-01-20,Electronics,East,80,1100,88000,Delivered
2026-02-15,Electronics,North,210,1250,262500,Delivered
2026-02-28,Home Appliances,North,60,400,24000,Cancelled
2026-03-10,Electronics,West,95,1150,109250,Shipped
```

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check logs
docker logs sales-automator-backend

# Verify environment variables
docker exec sales-automator-backend env

# Test API
curl http://localhost:8000/health
```

### Email not sending
1. Check SMTP credentials
2. Enable "Less secure app access" (Gmail)
3. Use app-specific password
4. Check spam folder

### File upload failing
1. Check file format (CSV or XLSX only)
2. Verify file size < 10MB
3. Check backend logs for errors

## 📚 API Documentation

Interactive API docs available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## 📦 Dependencies

**Backend (Python)**:
- fastapi: Web framework
- uvicorn: ASGI server
- pandas: Data processing
- httpx: Async HTTP client
- python-dotenv: Environment management
- slowapi: Rate limiting

**Frontend (Node.js)**:
- React 18: UI library
- Vite: Build tool
- Axios: HTTP client
- TypeScript: Type safety

## 🎯 Performance Optimization

**Docker Images**:
- Multi-stage builds to reduce size
- Alpine base images for frontend
- Slim Python images for backend

**Frontend**:
- Vite for fast development builds
- Lazy loading components
- Minimized CSS/JS bundles

**Backend**:
- Async file processing
- Efficient data handling
- Connection pooling

## 🔐 Security Checklist

- ✅ Rate limiting enabled
- ✅ CORS configured
- ✅ Input validation
- ✅ File type validation
- ✅ Email format validation
- ✅ File size limits
- ✅ Temporary file cleanup
- ✅ Error message sanitization
- ✅ Secrets in environment variables
- ✅ Health check endpoints
- ✅ Trusted host middleware
- ✅ API documentation secured

## 📄 License

This project is provided as-is for Rabbitt AI's internal use.

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review logs: `docker logs <container-name>`
3. Verify environment configuration
4. Check API documentation at `/docs`

---

**Version**: 1.0.0  
**Last Updated**: March 11, 2026  
**Status**: Production Ready ✓
