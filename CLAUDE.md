# Claude Code Project Conventions

## Branch Naming

Use `agentic/` as the branch prefix instead of `claude/`. For example:
`agentic/fix-lint-issues` or `agentic/update-docs`.

## Git Conventions

- Use conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, `style:`, `test:`
- Keep subject lines under 72 characters
- Imperative mood ("add" not "added")

## Pre-push Checklist

Always run `make check` before pushing to catch CI issues locally.
