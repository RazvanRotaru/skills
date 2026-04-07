#!/bin/bash
# Run once after cloning to configure hooks and install skills

REPO_ROOT="$(cd "$(dirname "$0")" && git rev-parse --show-toplevel)"

# Point git hooks to the committed .githooks directory
git -C "$REPO_ROOT" config core.hooksPath .githooks

# Run the initial sync (post-merge doesn't trigger on clone)
"$REPO_ROOT/.githooks/post-merge"

echo "Done. Skills synced to ~/.claude/skills/ and hooks configured."
