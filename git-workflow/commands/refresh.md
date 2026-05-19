---
description: Sync local repo to the latest origin/main after finishing branch work
allowed-tools: Bash(git checkout:*), Bash(git pull:*), Bash(git log:*), Bash(git rev-parse:*)
---

Sync this repository to the latest main branch:

1. Run `git checkout main && git pull origin main`
2. Report:
   - Current short commit hash
   - Number of commits pulled (0 if already up to date)
   - Summary of changed files (if any)
