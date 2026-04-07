# skills

A collection of Claude Code skills, automatically synced to `~/.claude/skills/`.

## Setup

After cloning, run:

```bash
./setup.sh
```

This will:
- Symlink all skills to `~/.claude/skills/`
- Configure git hooks so future `git pull` keeps them in sync

## Skills

### Coding Standards

- **clean-code** — Uncle Bob's Clean Code and formatting rules: function size, naming, SOLID principles, TDD, clean architecture, and formatting standards.

### Architecture & Design

- **design-an-interface** — Generate multiple radically different interface designs for a module using parallel sub-agents. Use when exploring API shapes, comparing module designs, or "designing it twice."
- **improve-codebase-architecture** — Explore a codebase to find opportunities for architectural improvement, focusing on making the codebase more testable by deepening shallow modules and consolidating tightly-coupled code.

### Requirements & Planning

- **write-a-prd** — Create a PRD through user interview, codebase exploration, and module design, then submit as a GitHub issue.
- **prd-to-issues** — Break a PRD into independently-grabbable GitHub issues using tracer-bullet vertical slices.
- **grill-me** — Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree.
- **ubiquitous-language** — Extract a DDD-style ubiquitous language glossary from the current conversation, flagging ambiguities and proposing canonical terms. Saves to `UBIQUITOUS_LANGUAGE.md`.

### Development Workflow

- **harness-orchestrate** — Decompose a feature or goal into independently-implementable tasks, then delegate each to an agent team.
- **harness-task-team** — Execute a full task lifecycle with a 4-agent team: write tests, adversarial test review, implement, adversarial code review. Uses a GAN-inspired generator-evaluator pattern.

### Development Environment

- **build-statusline** — Configure the Claude Code status line showing path, git branch, model, and context usage.

## Adding a new skill

Create a directory with a `SKILL.md` file:

```
my-skill/
└── SKILL.md
```

After pushing, anyone who runs `git pull` will automatically get the new skill symlinked.
