# Contributing Guidelines

## Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make changes and commit: `git commit -m "feat: description"`
4. Push to branch: `git push origin feature/your-feature`
5. Submit a pull request

## Code Standards

### Backend (Python)
- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions
- Keep functions focused and small
- Maximum file size: 500 lines

### Frontend (TypeScript/React)
- Use functional components with hooks
- Write meaningful prop types
- Keep components under 150 lines
- Use descriptive variable names
- Follow React best practices

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `test`: Tests
- `chore`: Build/dependencies

Example:
```
feat(api): add rate limiting
Implement per-IP rate limiting (5 req/min)
Fixes #123
```

## Pull Request Process

1. **Title Format**: `[Type] Brief description`
   - Example: `[Feature] Add CSV file validation`

2. **Description Template**:
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change

   ## Testing
   How to test these changes

   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] No new warnings
   - [ ] Tests pass
   - [ ] Documentation updated
   ```

3. **Review Process**:
   - At least 1 review required
   - CI/CD pipeline must pass
   - No merge conflicts

## Testing Requirements

### Backend
```bash
cd backend
python -m pytest
python -m pylint main.py
```

### Frontend
```bash
cd frontend
npm run lint
npm run build
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions
- Update API documentation in comments
- Include examples where applicable

## Questions?

- Check existing issues
- Review documentation
- Ask in pull request comments
- Contact maintainers
