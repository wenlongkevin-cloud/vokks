# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) and other AI assistants when working with this repository.

---

## Project Overview

**Repository:** `wenlongkevin-cloud/vokks`
**Status:** Initial setup — no source code has been committed yet.

This repository was initialized on `2026-04-05`. The codebase, tech stack, and architecture are to be determined as the project evolves. Update this file as the project takes shape.

---

## Repository State

- No source files exist yet
- No package manager, framework, or build tool has been chosen
- No CI/CD pipeline is configured
- No tests exist yet

---

## Development Branch

Active development happens on feature branches. The current documentation branch is:

```
claude/add-claude-documentation-j739c
```

Follow the branching convention: `<author>/<short-description>-<id>`

---

## Git Conventions

- **Commit messages:** Use the imperative mood (`Add feature`, not `Added feature`)
- **Branch names:** `<type>/<description>` — e.g. `feat/user-auth`, `fix/login-bug`, `claude/task-name`
- **Never force-push** to `main` or `master`
- **Never skip hooks** (`--no-verify`) without explicit user approval
- Prefer small, focused commits over large monolithic ones

---

## AI Assistant Guidelines

### General

- Read files before editing them
- Do not create files that aren't necessary for the task
- Do not add comments, docstrings, or type annotations to code you didn't change
- Do not add error handling for scenarios that cannot happen
- Do not refactor or "improve" code beyond what was requested
- Prefer editing existing files over creating new ones

### Codebase Changes

- Match the style and conventions already present in each file
- Keep changes minimal and targeted
- Do not introduce speculative abstractions or future-proofing
- Do not add backwards-compatibility shims for removed code

### Security

- Never introduce SQL injection, XSS, command injection, or other OWASP Top 10 vulnerabilities
- Validate input only at system boundaries (user input, external APIs)
- Do not hardcode secrets, tokens, or credentials

### Commits & Pushes

- Only commit when explicitly asked by the user
- Push to the designated development branch (see above), never to `main`/`master` without permission
- Always use `git push -u origin <branch>`

---

## Updating This File

When the project evolves (stack chosen, structure established, workflows defined), update the relevant sections:

1. **Project Overview** — describe what the project does
2. **Tech Stack** — languages, frameworks, package managers, build tools
3. **Directory Structure** — key directories and their purpose
4. **Development Workflow** — how to install dependencies, run dev server, run tests, build
5. **Environment Variables** — required `.env` keys (never commit actual values)
6. **Testing** — test framework, how to run tests, coverage requirements
7. **CI/CD** — pipelines, deployment targets

---

## Template Sections (fill in as project grows)

### Tech Stack

> _To be determined._

### Directory Structure

> _To be determined._

### Development Workflow

```bash
# Install dependencies
# <command here>

# Start dev server
# <command here>

# Run tests
# <command here>

# Build for production
# <command here>
```

### Environment Variables

> _Document required environment variables here. Never commit actual values._

### Testing

> _Describe the test framework and how to run tests._

### CI/CD

> _Describe the CI/CD pipeline and deployment process._
