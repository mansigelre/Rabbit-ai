# Architecture Decision Records (ADR)

## ADR-001: Technology Stack Selection

### Status: ACCEPTED

### Context
Need to build a quick-response tool for sales data processing with AI integration.

### Decision
- **Backend**: FastAPI (Python)
  - Built-in async support
  - Excellent documentation
  - Built-in Swagger/OpenAPI
  - Great for rapid development

- **Frontend**: React with Vite
  - Fast development experience
  - Excellent TypeScript support
  - Smaller bundle size
  - Modern tooling

- **LLM**: Google Gemini API
  - Fast and cost-effective
  - Good for text summarization
  - Easy integration

- **Email Service**: SMTP (Gmail)
  - No external dependencies
  - Easy to configure
  - Widely supported

### Consequences
- FastAPI has excellent async performance (✓)
- React ecosystem is mature and well-supported (✓)
- Gemini has latency concerns for large batches (⚠)
- Gmail has SMTP limits for high volume (⚠)

---

## ADR-002: Containerization Strategy

### Status: ACCEPTED

### Context
Need production-ready deployment on multiple platforms.

### Decision
- Use Docker multi-stage builds
- Minimize image sizes:
  - Backend: Python 3.11-slim
  - Frontend: Node 18-alpine + serve

### Consequences
- Faster builds and deployments (✓)
- Reduced attack surface (✓)
- Easier scaling on cloud platforms (✓)
- Limited debugging capabilities in slim images (⚠)

---

## ADR-003: Security Approach

### Status: ACCEPTED

### Context
Application handles sensitive sales data and customer emails.

### Decision
1. **Input Validation**
   - Email regex validation
   - File type checking (CSV/XLSX only)
   - File size limits (10MB)

2. **Rate Limiting**
   - 5 requests/minute per IP
   - Prevents resource abuse

3. **CORS Protection**
   - Whitelist-based origin checking
   - Configurable per environment

4. **Middleware Security**
   - Trusted host validation
   - Error message sanitization

### Consequences
- Protected against common attacks (✓)
- Prevents API abuse (✓)
- Scalable security model (✓)
- May need additional auth for enterprise (⚠)

---

## ADR-004: Email Delivery Model

### Status: ACCEPTED

### Context
Need reliable email delivery for executive summaries.

### Decision
- Synchronous email sending in request
- Attempts 3 times before timeout
- Fallback to basic summary if email fails

### Alternatives Considered
- Async queue-based delivery (Celery)
  - Rejected: Added complexity
  - Slower feedback to user

- Webhook-based delivery (SendGrid)
  - Rejected: Extra cost
  - Harder to debug

### Consequences
- Simple implementation (✓)
- User gets immediate feedback (✓)
- Long request times if email slow (⚠)
- Single point of failure if SMTP down (⚠)

---

## ADR-005: CI/CD Pipeline

### Status: ACCEPTED

### Context
Need automated testing and deployment.

### Decision
- GitHub Actions for CI/CD
- Triggers on PR and push to main
- Steps: Lint → Build → Test Docker

### Consequences
- Free CI/CD for public repos (✓)
- Easy integration with GitHub (✓)
- Native matrix builds (✓)
- Limited to GitHub only (⚠)

---

## ADR-006: Data Handling

### Status: ACCEPTED

### Context
Application processes customer sales data.

### Decision
1. Store uploaded files temporarily in `/app/uploads/`
2. Clean up after processing
3. Use secure random names for files
4. No persistent storage of data

### Consequences
- Compliant with data minimization (✓)
- Files automatically cleaned on container restart (✓)
- Lost if container crashes during processing (⚠)
- May need persistent storage for audit logs (⚠)

---

## ADR-007: API Versioning

### Status: ACCEPTED

### Context
Need to support API evolution without breaking clients.

### Decision
- Use path-based versioning: `/api/v1/`
- Semantic versioning for releases
- Deprecation path for v1 → v2 migrations

### Consequences
- Clear API contracts (✓)
- Easy to support multiple versions (✓)
- Requires migration path planning (⚠)

---

## ADR-008: Error Handling Strategy

### Status: ACCEPTED

### Context
Need consistent error responses across the application.

### Decision
1. **HTTP Status Codes**:
   - 400: Validation errors
   - 413: File too large
   - 429: Rate limit exceeded
   - 500: Server errors

2. **Error Response Format**:
   ```json
   {
     "detail": "Human-readable error message"
   }
   ```

3. **Logging**:
   - Log errors with context
   - Never log sensitive data
   - Structured logging format

### Consequences
- Consistent API behavior (✓)
- Easy client error handling (✓)
- Clear debugging trail (✓)
- May expose too much detail (⚠)

---

## ADR-009: Frontend State Management

### Status: ACCEPTED

### Context
React form needs to manage upload, email, and loading states.

### Decision
- Use React hooks (useState) for local state
- No Redux/Zustand (complexity not needed)
- Component-level state management

### Alternatives
- Redux: Overkill for this scope
- Zustand: Good but unnecessary
- React Context: Good options but hooks sufficient

### Consequences
- Simple implementation (✓)
- Easy to understand (✓)
- No global state (✓)
- Difficult to scale if app grows (⚠)

---

## ADR-010: Fallback Strategy for AI Engine

### Status: ACCEPTED

### Context
Gemini API may be unavailable or rate-limited.

### Decision
- Implement automatic fallback to basic summary
- Basic summary includes:
  - Total revenue
  - Total units sold
  - Record count
  - Generic insights

### Consequences
- App always functional (✓)
- Users get value even if API down (✓)
- Degraded experience acceptable (✓)
- May frustrate users expecting AI insights (⚠)

---

## Future Considerations

### ADR-011: Queue-Based Processing (Future)
When email/AI latency becomes critical:
- Implement Redis/RabbitMQ queue
- Async task processing
- Webhook notifications

### ADR-012: Database Integration (Future)
When audit/history needed:
- Add PostgreSQL for:
  - Upload history
  - Generated summaries
  - Audit logs
  - User analytics

### ADR-013: Authentication & Authorization (Future)
When multi-tenant features needed:
- OAuth2/JWT implementation
- Role-based access control
- API key management

### ADR-014: Enhanced Error Recovery (Future)
- Circuit breaker pattern
- Retry strategies with exponential backoff
- Dead letter queues
