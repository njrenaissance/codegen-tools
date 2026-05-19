---
name: clean-code-review
description: Review pending code changes against the Clean Code standards. Use when the user asks for a clean-code review, runs /clean-code-review, or finishes a chunk of work and wants a standards check.
---

# Clean Code Review

Runs a Clean Code review of the current changes by dispatching to the
`clean-code-reviewer` subagent — so the review runs in a throwaway context
window, not this conversation.

The standard is *Clean Code: A Handbook of Agile Software Craftsmanship*
(Robert C. Martin, Prentice Hall, 2008). The subagent reviews source code in
any language against the full standard and reports every violation it finds.

## Steps

1. **Determine scope.**
   - If the user named specific files, use those.
   - Otherwise run `git diff --name-only` (and `git diff`) against the base
     branch — or the working tree, if changes are uncommitted — to find changed
     source files.
   - If nothing relevant changed, tell the user and stop.

2. **Dispatch to the reviewer.** Spawn the `clean-code-reviewer` agent via the
   Agent tool (`subagent_type: clean-code-reviewer`), passing the list of
   changed files and the diff. The agent carries the Clean Code standard itself
   and reads the files in its own context.

3. **Relay the report.** Present the subagent's report to the user exactly as
   it produced it. Do not re-derive, re-format, or second-guess it — the output
   format is fixed by the `clean-code-reviewer` agent.

4. **Offer to fix.** Ask whether to apply any of the suggested fixes.
