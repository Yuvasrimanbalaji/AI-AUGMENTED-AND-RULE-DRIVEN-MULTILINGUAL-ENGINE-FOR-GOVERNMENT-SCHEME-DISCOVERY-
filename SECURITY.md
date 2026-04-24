# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Which versions are currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of Scheme Finder seriously. If you discover a security vulnerability, please report it to us as described below.

### How to Report

Please do **NOT** report security vulnerabilities through public GitHub issues.

Instead, please email us at:
- **Email:** yuvasrimanbalaji@gmail.com

Please include the following information in your report:
- Type of issue (e.g. SQL injection, XSS, CSRF, etc.)
- Full paths of source file(s) related to the issue
- Location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

### What to Expect

- **Initial Response:** You will receive an acknowledgment within 48 hours
- **Updates:** We will keep you informed of our progress
- **Resolution:** We aim to resolve critical issues within 7 days

### Security Best Practices

When using this project, please follow these security guidelines:
1. **Never commit API keys** to version control - use environment variables
2. **Keep dependencies updated** - regularly run `pip install --upgrade -r requirements.txt`
3. **Use strong passwords** for any authentication systems
4. **Enable HTTPS** when deploying to production
5. **Validate all user inputs** before processing
6. **Review third-party packages** before adding them as dependencies

## Security Measures in This Project

This project implements the following security measures:
- Environment variable management for sensitive data (API keys, etc.)
- Input validation and sanitization
- CORS configuration for API endpoints
- Security headers in HTTP responses
- Rate limiting for API requests
- Secure cookie handling

Thank you for helping keep Scheme Finder secure!
