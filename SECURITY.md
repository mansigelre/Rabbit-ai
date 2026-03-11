# Security Policy

## Reporting Vulnerabilities

**DO NOT open a public GitHub issue for security vulnerabilities.**

Please report security vulnerabilities to: `security@rabbittai.example.com`

Include:
- Description of vulnerability
- Affected components
- Steps to reproduce (if applicable)
- Potential impact

## Security Best Practices

### API Security
- ✅ CORS properly configured
- ✅ Rate limiting enabled
- ✅ Input validation on all endpoints
- ✅ No sensitive data in logs
- ✅ HTTPS required in production
- ✅ API keys rotated regularly

### Data Security
- ✅ Temporary files cleaned up
- ✅ No credentials in code
- ✅ Environment variables used
- ✅ Email content sanitized
- ✅ File uploads validated

### Container Security
- ✅ Non-root user in Docker
- ✅ Minimal dependencies
- ✅ Regular updates
- ✅ Security scanning enabled

### Dependency Management
- ✅ `requirements.txt` pinned versions
- ✅ `package.json` versions reviewed
- ✅ Regular security audits
- ✅ CVE monitoring enabled

## Compliance

- **Rate Limiting**: 5 requests/minute per IP
- **File Size Limit**: 10 MB maximum
- **Email Validation**: RFC 5322 compliant
- **CORS**: Whitelist-based origins

## Incident Response

1. Vulnerability reported
2. Assessment within 24 hours
3. Fix implementation
4. Security patch release
5. Public disclosure (if needed)

## Security Updates

Subscribe to notifications:
- GitHub security alerts
- Dependency audit reports
- Container scanning results

## Support

For security concerns about deployed instances:
- Email: `security@rabbittai.example.com`
- Response time: < 24 hours
