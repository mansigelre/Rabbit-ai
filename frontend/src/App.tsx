import React, { useState, ChangeEvent, FormEvent } from 'react';
import axios from 'axios';
import './App.css';

interface UploadResponse {
  status: string;
  message: string;
  email_sent: boolean;
  recipient: string;
  summary_preview: string;
  timestamp: string;
}

const App: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [fileName, setFileName] = useState('');

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      const fileName = selectedFile.name;
      const fileExt = fileName.split('.').pop()?.toLowerCase();
      
      if (fileExt === 'csv' || fileExt === 'xlsx') {
        setFile(selectedFile);
        setFileName(fileName);
        setError('');
      } else {
        setError('Please upload a CSV or XLSX file');
        setFile(null);
        setFileName('');
      }
    }
  };

  const handleEmailChange = (e: ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target.value);
  };

  const validateEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    // Validation
    if (!file) {
      setError('Please select a file');
      return;
    }

    if (!email) {
      setError('Please enter an email address');
      return;
    }

    if (!validateEmail(email)) {
      setError('Please enter a valid email address');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess(false);

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('recipient_email', email);

      const response = await axios.post<UploadResponse>(
        `${API_URL}/api/v1/analyze`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          timeout: 60000,
        }
      );

      if (response.data.status === 'success') {
        setSuccess(true);
        setSuccessMessage(
          `✓ Analysis completed! Summary sent to ${response.data.recipient}. Preview:\n\n${response.data.summary_preview}`
        );
        setFile(null);
        setFileName('');
        setEmail('');
        
        // Reset form
        const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement;
        if (fileInput) fileInput.value = '';
      }
    } catch (err: unknown) {
      if (axios.isAxiosError(err)) {
        const errorMessage = err.response?.data?.detail || err.message;
        setError(`Error: ${errorMessage}`);
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="card">
        <div className="header">
          <h1>📊 Sales Insight Automator</h1>
          <p className="subtitle">Upload your sales data and get instant AI-powered insights</p>
        </div>

        <form onSubmit={handleSubmit} className="form">
          {/* File Upload */}
          <div className="form-group">
            <label htmlFor="file-input" className="label">
              📁 Select Sales File (CSV or XLSX)
            </label>
            <div className="file-input-wrapper">
              <input
                id="file-input"
                type="file"
                onChange={handleFileChange}
                accept=".csv,.xlsx"
                disabled={loading}
                className="file-input"
              />
              <span className="file-name">{fileName || 'No file chosen'}</span>
            </div>
          </div>

          {/* Email Input */}
          <div className="form-group">
            <label htmlFor="email-input" className="label">
              📧 Recipient Email
            </label>
            <input
              id="email-input"
              type="email"
              placeholder="your.email@company.com"
              value={email}
              onChange={handleEmailChange}
              disabled={loading}
              className="input"
              required
            />
          </div>

          {/* Error Message */}
          {error && (
            <div className="alert alert-error">
              <span className="alert-icon">⚠️</span>
              <span>{error}</span>
            </div>
          )}

          {/* Success Message */}
          {success && successMessage && (
            <div className="alert alert-success">
              <span className="alert-icon">✓</span>
              <div>
                <strong>Success!</strong>
                <p>{successMessage}</p>
              </div>
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading || !file || !email}
            className="button"
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Processing...
              </>
            ) : (
              '🚀 Generate & Send Summary'
            )}
          </button>
        </form>

        {/* Info Section */}
        <div className="info-section">
          <h3>ℹ️ How It Works</h3>
          <ol className="info-list">
            <li>Upload your sales CSV or XLSX file</li>
            <li>Enter the recipient's email address</li>
            <li>AI analyzes your data instantly</li>
            <li>Professional summary is emailed immediately</li>
          </ol>
        </div>

        {/* API Documentation Link */}
        <div className="footer">
          <a 
            href={`${API_URL}/docs`} 
            target="_blank" 
            rel="noopener noreferrer"
            className="api-link"
          >
            📚 View API Documentation (Swagger)
          </a>
        </div>
      </div>
    </div>
  );
};

export default App;
