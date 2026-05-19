# Contributing

## Code Style

- **Backend:** PEP 8 with flake8
- **Frontend:** ESLint with Airbnb config

## Branch Naming

- Feature: `feature/feature-name`
- Bug fix: `bugfix/bug-description`
- Docs: `docs/doc-topic`

## Commit Messages

Follow conventional commits:
- `feat: Add feature description`
- `fix: Fix bug description`
- `docs: Update documentation`
- `test: Add test for feature`

## Pull Request Process

1. Create a feature branch
2. Make your changes
3. Ensure tests pass locally
4. Push and create a PR
5. Wait for CI checks and code review
6. Merge after approval

## Testing

### Backend Tests
```bash
cd backend
pytest -q
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Local Development Workflow

1. Clone repo
2. `docker-compose up --build`
3. Make changes in your editor
4. Changes auto-reload in containers
5. Commit when happy
6. Create PR

## Reporting Issues

Use GitHub Issues with:
- Clear title
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, Node version)
