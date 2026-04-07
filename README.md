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

## Adding a new skill

Create a directory with a `SKILL.md` file:

```
my-skill/
└── SKILL.md
```

After pushing, anyone who runs `git pull` will automatically get the new skill symlinked.
