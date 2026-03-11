## Deployment Instructions

### Prerequisites
- GitHub account with repository
- Vercel account (for frontend)
- Render account (for backend)
- Google Gemini API key
- SMTP credentials for email service

### Step 1: Deploy Backend to Render

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Deploy Backend Service**
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Repository: Select `sales-insight-automator`
   - Branch: `main`
   - Build Command:
     ```
     pip install --upgrade pip && pip install -r requirements.txt
     ```
   - Start Command:
     ```
     python -m uvicorn main:app --host 0.0.0.0 --port $PORT
     ```

3. **Set Environment Variables**
   - Navigate to "Environment" tab
   - Add from `backend/.env`:
     ```
     GEMINI_API_KEY=your_key
     SMTP_HOST=smtp.gmail.com
     SMTP_PORT=587
     SMTP_EMAIL=your_email@gmail.com
     SMTP_PASSWORD=your_app_password
     API_KEY=your_secure_key
     ALLOWED_ORIGINS=https://your-vercel-domain.vercel.app
     ENV=production
     ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Note the URL: `https://your-backend.onrender.com`

### Step 2: Deploy Frontend to Vercel

1. **Create Vercel Account**
   - Go to https://vercel.com
   - Sign up with GitHub

2. **Deploy Frontend**
   - Click "Add New..." → "Project"
   - Import repository
   - Set Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

3. **Set Environment Variables**
   - Add from `frontend/.env.example`:
     ```
     VITE_API_URL=https://your-backend.onrender.com
     ```

4. **Deploy**
   - Click "Deploy"
   - Wait for build to complete
   - Your frontend is now live

### Step 3: Update Backend CORS

Once frontend is deployed:
1. Go to Render dashboard
2. Select backend service
3. Update `ALLOWED_ORIGINS`:
   ```
   https://your-frontend.vercel.app
   ```
4. Redeploy

### Step 4: Test Live Application

1. Open frontend URL
2. Upload `sales_q1_2026.csv`
3. Enter your email
4. Check email inbox for summary

### CI/CD Configuration

The GitHub Actions workflow will:
- Run on each pull request to `main`
- Lint and build frontend
- Lint and test backend
- Build Docker images
- Verify everything works

Once merged to main:
- Render automatically deploys backend
- Vercel automatically deploys frontend

### Monitoring

**Backend Monitoring (Render)**:
- View logs: Render Dashboard → Logs tab
- Health endpoint: `https://your-backend.onrender.com/health`

**Frontend Monitoring (Vercel)**:
- View logs: Vercel Dashboard → Deployments
- Analytics: Vercel Dashboard → Analytics tab

### Configuration Management

**Render Secrets**:
- Use Render's environment management
- Rotate secrets periodically
- Never commit .env files

**Vercel Secrets**:
- Use Vercel's environment management
- Separate preview and production variables
- Audit access logs

### Troubleshooting Deployment

1. **Backend won't start**
   - Check Python version (3.11+)
   - Verify all env vars set
   - Check logs for module errors

2. **Frontend won't build**
   - Check Node version (18+)
   - Clear npm cache
   - Verify API URL is correct

3. **Requests timing out**
   - Check CORS settings
   - Verify ports are correct
   - Check email service connectivity

### Rollback Procedure

**Render Backend**:
1. Go to Deployments tab
2. Select previous deployment
3. Click "Redeploy"

**Vercel Frontend**:
1. Go to Deployments tab
2. Click "..." on previous deployment
3. Select "Promote to Production"

### Performance Optimization

**Backend**:
- Enable caching headers
- Use CDN for static files
- Monitor Gemini API latency

**Frontend**:
- Enable Vercel Analytics
- Monitor Core Web Vitals
- Optimize bundle size

### Security Post-Deployment

- [ ] Change API keys
- [ ] Enable 2FA on Render
- [ ] Enable 2FA on Vercel
- [ ] Review CORS origins
- [ ] Set up rate limiting alerts
- [ ] Configure backup strategy
- [ ] Document runbook

### Support & Escalation

| Issue | Action |
|-------|--------|
| 5xx errors | Check backend logs on Render |
| Slow responses | Check Gemini API status |
| Email failures | Verify SMTP credentials |
| Deployment failures | Review CI/CD logs on GitHub |
| Rate limiting | Check incoming request volume |

---

For more details, see [README.md](../README.md)
