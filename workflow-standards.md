# Git Workflow

- **Branching**: Create a new branch for each issue/task
  - Branch naming: `issue-{number}` or `feature/{short-description}`
  - Example: `issue-1`, `feature/observability-setup`
- **Integration**: All code changes must be merged via pull request
  - PRs require clear commit history demonstrating incremental progress
  - Include reference to related issue in PR description
  - Avoid squash-merging; preserve commit history on demonstration PRs (per challenge requirements)
- **Commit Messages**: Use [Conventional Commits](https://www.conventionalcommits.org/)
  - Format: `<type>: <description>`
  - Types: `feat:`, `fix:`, `chore:`, `docs:`, `test:`, `revert:`
  - Example: `feat: Add infrastructure provisioning API endpoint`
  - Include detailed explanation in commit body when needed
  - End with co-author line: `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`
