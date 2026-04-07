---
name: build-statusline
description: Configure Claude Code status line showing path, git branch, model, and context usage. Use when user wants to set up or update their status line.
---

Set up the Claude Code status line by copying the script from this skill and configuring settings.

## Prerequisites

Install `jq` and `git` if not already available:

```bash
# Debian/Ubuntu
sudo apt-get install -y jq git

# macOS
brew install jq git
```

## Steps

1. Ensure `jq` and `git` are installed (see Prerequisites above)
2. Copy `statusline-command.sh` from this skill's directory to `~/.claude/statusline-command.sh`
3. Ensure `~/.claude/settings.json` contains:
   ```json
   "statusLine": {
     "type": "command",
     "command": "bash ~/.claude/statusline-command.sh"
   }
   ```

## What it displays

```
~/workspace/drift  ⎇ master(*3 ↑2)  opus  ctx: 9k/1.0M (3%)
```

| Field | Color | Description |
|-------|-------|-------------|
| Path | Bold blue | Working directory with `~` for home |
| Git branch | Bold magenta | `⎇ branch(*N ↑N)` — dirty count + unpushed commits |
| Model | Bold cyan | Short name: opus, sonnet, haiku |
| Context | Bold green | Tokens used/total and percentage |

Fields are omitted when data is unavailable.
