---
name: clean-code-review
description: Review pending code changes against the Clean Code standards. Use when the user asks for a clean-code review, runs /clean-code-review, or finishes a chunk of Python/TypeScript work and wants a standards check.
---

# Clean Code Review

Runs a judgment-tier Clean Code review of the current changes by dispatching to
the `clean-code-reviewer` subagent — so the rules and detail load in a
throwaway context window, not this conversation.

## Steps

1. **Determine scope.**
   - If the user named specific files, use those.
   - Otherwise run `git diff --name-only` (and `git diff`) against the base
     branch — or the working tree, if changes are uncommitted — to find changed
     `.py` / `.ts` / `.tsx` files.
   - If nothing relevant changed, tell the user and stop.

2. **Dispatch to the reviewer.** Spawn the `clean-code-reviewer` agent via the
   Agent tool (`subagent_type: clean-code-reviewer`), passing:
   - the list of changed files and the diff, and
   - the standards path: `${CLAUDE_PLUGIN_ROOT}/CLEAN-CODE.md`.

   The subagent reads the files and the standards in its own context.

3. **Relay the report.** Present the subagent's findings to the user, grouped
   by severity. Do not re-derive or second-guess them.

4. **Offer to fix.** Ask whether to apply any of the suggested fixes.

## Scope note

This review covers only the **`review`-tier** rules — the judgment-based ones a
linter cannot enforce. `builtin` / `custom` rules are the linter's job (run in
the `PostToolUse` hook); this skill does not re-check them.
