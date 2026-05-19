# Refresh - Sync to Main

Quickly sync your local repository to the latest main branch.

## Invocation

```claude
/refresh
```

## Behavior

1. Checkout the `main` branch
2. Pull the latest changes from `origin/main`
3. Report the current commit and any files updated

## Commands

Run these git commands in sequence:

```bash
git checkout main && git pull origin main
```

## Output

After syncing, report:

- Current commit hash (short)
- Number of commits pulled (if any)
- Summary of changed files (if any)
