"""
Sales Insight Automator - Backend API
FastAPI application for processing sales data and generating AI summaries
"""
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
import io
import os
import logging
import secrets
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import pandas as pd
import aiofiles
from dotenv import load_dotenv
import httpx
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
from functools import lru_cache
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel, EmailStr, validator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Sales Insight Automator API",
    description="Secure API for processing sales data and generating AI-powered summaries",
    version="1.0.0"
)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Configure CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in ALLOWED_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware for security
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1"])

# Configuration
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {".csv", ".xlsx"}
UPLOAD_DIRECTORY = Path("uploads")
UPLOAD_DIRECTORY.mkdir(exist_ok=True)

# Pydantic models
class SalesDataRequest(BaseModel):
    recipient_email: EmailStr
    
    @validator('recipient_email')
    def validate_email(cls, v):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('Invalid email format')
        return v

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str

# Security helpers
def validate_file(filename: str) -> bool:
    """Validate file type"""
    if not filename:
        return False
    ext = Path(filename).suffix.lower()
    return ext in ALLOWED_EXTENSIONS

def validate_email_format(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

async def get_api_key():
    """Dependency for API key validation"""
    # In production, extract from header
    return os.getenv("API_KEY")

# AI Integration
class AIEngine:
    @staticmethod
    async def generate_summary(data_df: pd.DataFrame) -> str:
        """Generate AI summary using Gemini API"""
        try:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                logger.warning("Gemini API key not configured")
                return AIEngine.generate_fallback_summary(data_df)
            
            # Prepare data summary for LLM
            total_revenue = data_df['Revenue'].sum() if 'Revenue' in data_df.columns else 0
            total_units = data_df['Units_Sold'].sum() if 'Units_Sold' in data_df.columns else 0
            
            product_summary = ""
            if 'Product_Category' in data_df.columns:
                product_summary = data_df['Product_Category'].value_counts().to_dict()
            
            region_summary = ""
            if 'Region' in data_df.columns:
                region_summary = data_df['Region'].value_counts().to_dict()
            
            prompt = f"""
            You are a professional business analyst. Analyze this sales data and provide a concise, 
            executive summary (2-3 paragraphs) suitable for leadership. Include key metrics, trends, 
            and actionable insights.
            
            Data Summary:
            - Total Units Sold: {total_units}
            - Total Revenue: ${total_revenue:,.2f}
            - Product Categories: {product_summary}
            - Regions: {region_summary}
            - Date Range: {data_df['Date'].min() if 'Date' in data_df.columns else 'N/A'} to {data_df['Date'].max() if 'Date' in data_df.columns else 'N/A'}
            
            Data Preview:
            {data_df.head(10).to_string()}
            
            Provide an insightful, professional summary that an executive would appreciate.
            """
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
                    json={
                        "contents": [{
                            "parts": [{"text": prompt}]
                        }]
                    },
                    params={"key": api_key},
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    summary = result['candidates'][0]['content']['parts'][0]['text']
                    return summary
                else:
                    logger.error(f"Gemini API error: {response.status_code}")
                    return AIEngine.generate_fallback_summary(data_df)
                    
        except Exception as e:
            logger.error(f"AI Engine error: {str(e)}")
            return AIEngine.generate_fallback_summary(data_df)
    
    @staticmethod
    def generate_fallback_summary(data_df: pd.DataFrame) -> str:
        """Generate fallback summary if AI is unavailable"""
        total_revenue = data_df['Revenue'].sum() if 'Revenue' in data_df.columns else 0
        total_units = data_df['Units_Sold'].sum() if 'Units_Sold' in data_df.columns else 0
        
        summary = f"""
        Sales Performance Summary
        
        Total Revenue: ${total_revenue:,.2f}
        Total Units Sold: {int(total_units)}
        Record Count: {len(data_df)}
        
        This data provides a comprehensive view of sales activity across the period. 
        Further analysis is recommended for detailed insights and strategic planning.
        """
        return summary

# Email Service
class EmailService:
    @staticmethod
    async def send_summary(recipient_email: str, summary: str, filename: str) -> bool:
        """Send email with summary"""
        try:
            sender_email = os.getenv("SMTP_EMAIL")
            sender_password = os.getenv("SMTP_PASSWORD")
            smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
            smtp_port = int(os.getenv("SMTP_PORT", 587))
            
            if not sender_email or not sender_password:
                logger.warning("Email credentials not configured")
                return False
            
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = f"Sales Insights Summary - {datetime.now().strftime('%B %d, %Y')}"
            message["From"] = sender_email
            message["To"] = recipient_email
            
            # Create HTML email
            html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #333;">📊 Sales Insight Summary</h2>
                        <p style="color: #666; margin-bottom: 20px;">
                            Generated from: <strong>{filename}</strong><br>
                            Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
                        </p>
                        <div style="background-color: #f5f5f5; padding: 20px; border-radius: 5px; border-left: 4px solid #4CAF50;">
                            {summary.replace(chr(10), '<br>')}
                        </div>
                        <p style="color: #999; font-size: 12px; margin-top: 20px;">
                            This is an automated summary generated by Sales Insight Automator.
                        </p>
                    </div>
                </body>
            </html>
            """
            
            part = MIMEText(html, "html")
            message.attach(part)
            
            # Send email
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)
            
            logger.info(f"Email sent successfully to {recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Email service error: {str(e)}")
            return False

# API Endpoints
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )

@app.post("/api/v1/analyze")
@limiter.limit("5/minute")
async def analyze_sales_data(
    request: Request,
    recipient_email: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Upload a sales data file and generate an AI-powered summary
    
    - **recipient_email**: Email address to send the summary to
    - **file**: CSV or XLSX file containing sales data
    """
    try:
        # Validate email
        if not validate_email_format(recipient_email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )
        
        # Validate file
        if not file.filename or not validate_file(file.filename):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be .csv or .xlsx"
            )
        
        # Check file size
        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size exceeds 10MB limit"
            )
        
        # Reset file pointer
        await file.seek(0)
        
        # Save file temporarily
        safe_filename = f"{secrets.token_hex(8)}_{Path(file.filename).name}"
        file_path = UPLOAD_DIRECTORY / safe_filename
        
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(await file.read())
        
        logger.info(f"File saved: {safe_filename}")
        
        # Parse file
        try:
            if file.filename.endswith('.csv'):
                data_df = pd.read_csv(file_path)
            else:
                data_df = pd.read_excel(file_path)
            
            if data_df.empty:
                raise ValueError("The uploaded file is empty")
                
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error parsing file: {str(e)}"
            )
        
        # Generate AI summary
        logger.info("Generating AI summary...")
        summary = await AIEngine.generate_summary(data_df)
        
        # Send email
        logger.info(f"Sending email to {recipient_email}...")
        email_sent = await EmailService.send_summary(recipient_email, summary, file.filename)
        
        # Cleanup
        try:
            Path(file_path).unlink()
        except Exception as e:
            logger.warning(f"Could not delete temporary file: {str(e)}")
        
        return {
            "status": "success",
            "message": "Analysis completed",
            "email_sent": email_sent,
            "recipient": recipient_email,
            "summary_preview": summary[:200] + "..." if len(summary) > 200 else summary,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    """Handle rate limit exceeded"""
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": "Rate limit exceeded. Maximum 5 requests per minute."}
    )

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Sales Insight Automator API",
        version="1.0.0",
        description="Secure API for processing sales data and generating AI-powered summaries",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENV", "development") == "development"
    )
