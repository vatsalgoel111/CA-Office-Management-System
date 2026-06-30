# Git Workflow

## Branches

Recommended branches:

- `main`: stable production-ready code
- `develop`: integration branch during active development
- `codex/feature-name`: feature branches created by Codex

## Commit Style

Use conventional-style commit messages:

```text
feat: add login service
fix: handle inactive users during login
test: add client repository tests
docs: update database design
chore: configure project structure
```

## Module Rule

Each completed module must include:

1. Implementation
2. Tests
3. Documentation update
4. Git commit

## Safety Rule

Never rewrite history or discard local changes unless explicitly approved.

