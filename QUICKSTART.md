# 🚀 Quick Start Guide

## 5-Minute Setup

### Step 1: Prerequisites Check
```bash
# Verify Docker is installed
docker --version
docker-compose --version
```

**Need Docker?** Download [Docker Desktop](https://www.docker.com/products/docker-desktop)

### Step 2: Configure Environment
```bash
# Navigate to project
cd sales-insight-automator

# Copy configuration files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

**Edit `backend/.env`** with:
```env
GEMINI_API_KEY=sk-...  # Get from https://aistudio.google.com/app/apikeys
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_password  # Not your regular password!
```

#### Get Credentials

**Google Gemini API:**
1. Go to https://aistudio.google.com/app/apikeys
2. Click "Get API Key"
3. Copy and paste into `GEMINI_API_KEY`

**Gmail App Password:**
1. Enable 2FA: https://myaccount.google.com/security
2. Go to App Passwords: https://myaccount.google.com/apppasswords
3. Select Mail and Windows Computer
4. Copy the generated password

### Step 3: Start Services
```bash
# Start all services
docker-compose up -d

# Verify they're running
docker-compose ps
```

**Expected output:**
```
CONTAINER ID   STATUS           PORTS
...            Up (healthy)     0.0.0.0:8000->8000/tcp  (backend)
...            Up (healthy)     0.0.0.0:3000->3000/tcp  (frontend)
```

### Step 4: Access Application
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Step 5: Test End-to-End
1. Download [sales_q1_2026.csv](./sales_q1_2026.csv)
2. Open http://localhost:3000
3. Upload the CSV file
4. Enter your email
5. Click "Generate & Send Summary"
6. Check your email inbox in 30 seconds

---

## ⚙️ Configuration Details

### Environment Variables

**Backend (.env)**
| Variable | Purpose | Example |
|----------|---------|---------|
| `GEMINI_API_KEY` | AI engine access | `sk-xyz...` |
| `SMTP_HOST` | Email server | `smtp.gmail.com` |
| `SMTP_PORT` | Email port | `587` |
| `SMTP_EMAIL` | Sender email | `notify@company.com` |
| `SMTP_PASSWORD` | Email password | `app_password_xyz` |
| `PORT` | Backend port | `8000` |
| `ALLOWED_ORIGINS` | CORS whitelist | `http://localhost:3000` |

**Frontend (.env)**
| Variable | Purpose | Example |
|----------|---------|---------|
| `VITE_API_URL` | Backend URL | `http://localhost:8000` |

### File Upload Constraints
- **Formats**: `.csv`, `.xlsx`
- **Max Size**: 10 MB
- **Min Records**: 1 row

---

## 🔍 Verification Checklist

```bash
# ✓ Backend is running
curl http://localhost:8000/health
# {status: "healthy"}

# ✓ API documentation accessible
open http://localhost:8000/docs

# ✓ Frontend is running
curl http://localhost:3000
# HTML response

# ✓ Check backend logs
docker logs sales-automator-backend

# ✓ Check frontend logs
docker logs sales-automator-frontend
```

---

## 📝 Common Tasks

### View Live Logs
```bash
docker-compose logs -f backend        # Backend logs only
docker-compose logs -f frontend       # Frontend logs only
docker-compose logs -f                # All services
```

### Stop Services
```bash
docker-compose down                   # Stop all
```

### Restart Services
```bash
docker-compose restart backend        # Restart backend only
docker-compose restart                # Restart all
```

### Rebuild (After code changes)
```bash
docker-compose build --no-cache       # Rebuild images
docker-compose up -d                  # Restart
```

### View File Uploads
```bash
ls backend/uploads/
```

### Test API Directly
```bash
# Using curl
curl -X POST http://localhost:8000/api/v1/analyze \
  -F "recipient_email=test@example.com" \
  -F "file=@sales_q1_2026.csv"

# Using Python
python scripts/test_api.py
```

---

## 🐛 Troubleshooting

### Frontend won't load
```bash
# Check if frontend container is running
docker ps | grep frontend

# View logs
docker logs sales-automator-frontend

# Rebuild
docker-compose build frontend
docker-compose up -d frontend
```

### Email not sending
```bash
# Verify SMTP credentials in .env
# Check gmail security settings
# Enable 2FA and use app password

# Test email service
docker exec sales-automator-backend python -c "
import os, smtplib
smtp_host = os.getenv('SMTP_HOST')
print(f'Email: {os.getenv(\"SMTP_EMAIL\")}')
print(f'Host: {smtp_host}')
"
```

### API returns 500 error
```bash
# Check backend logs
docker logs sales-automator-backend

# Verify Gemini API key
echo $GEMINI_API_KEY

# Test Gemini API
curl -X POST https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=YOUR_KEY \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"hello"}]}]}'
```

### Port already in use
```bash
# Change ports in docker-compose.yml
# Example:
# ports:
#   - "8001:8000"  # Changed from 8000:8000
```

---

## 📚 API Usage Examples

### Upload & Analyze
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: multipart/form-data" \
  -F "recipient_email=john@company.com" \
  -F "file=@sales_q1_2026.csv"
```

### Check Health
```bash
curl http://localhost:8000/health
```

### View API Documentation
```bash
# Swagger UI
curl http://localhost:8000/docs

# ReDoc
curl http://localhost:8000/redoc

# OpenAPI Schema
curl http://localhost:8000/openapi.json
```

---

## 🚢 Deployment Quick Links

- **Frontend to Vercel**: See [DEPLOYMENT.md](./DEPLOYMENT.md#step-2-deploy-frontend-to-vercel)
- **Backend to Render**: See [DEPLOYMENT.md](./DEPLOYMENT.md#step-1-deploy-backend-to-render)
- **Full Guide**: [DEPLOYMENT.md](./DEPLOYMENT.md)

---

## 📞 Getting Help

1. **Check Logs**
   ```bash
   docker-compose logs -f
   ```

2. **Review Documentation**
   - [README.md](./README.md) - Full overview
   - [DEPLOYMENT.md](./DEPLOYMENT.md) - Deployment guide
   - [ARCHITECTURE.md](./ARCHITECTURE.md) - Design decisions
   - [SECURITY.md](./SECURITY.md) - Security policies

3. **API Documentation**
   - http://localhost:8000/docs (Swagger)
   - http://localhost:8000/redoc (ReDoc)

4. **Check GitHub Issues**
   - Search existing issues
   - Review pull requests

---

## ✅ Success Indicators

You know it's working when:
- ✓ http://localhost:3000 loads (purple gradient page)
- ✓ http://localhost:8000/health returns `{"status":"healthy"}`
- ✓ http://localhost:8000/docs shows Swagger UI
- ✓ File upload form accepts CSV/XLSX files
- ✓ Email is received within 30 seconds
- ✓ Summary includes AI-generated insights

---

## 🎓 Next Steps

1. **Explore the API**
   - Visit http://localhost:8000/docs
   - Try different file types and sizes

2. **Understand the Architecture**
   - Read [ARCHITECTURE.md](./ARCHITECTURE.md)
   - Review security decisions in [SECURITY.md](./SECURITY.md)

3. **Contribute**
   - See [CONTRIBUTING.md](./CONTRIBUTING.md)
   - Submit issues and PRs

4. **Deploy**
   - Follow [DEPLOYMENT.md](./DEPLOYMENT.md)
   - Point to live Render/Vercel URLs

---

**Version**: 1.0.0  
**Last Updated**: March 11, 2026  
**Status**: ✓ Production Ready
