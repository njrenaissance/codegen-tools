# Decisions

Architecture Decision Records (ADRs) for the Clean Code standards. Newest last.

<!-- markdownlint-disable MD024 MD036 -->
<!-- ADRs intentionally repeat Context / Decision / Consequences headings. -->

---

## ADR-001 — Clean Code enforcement architecture

**Status:** Accepted   **Date:** 2026-05-18

### Context

We maintain a set of Clean Code rules to enforce consistently across projects.
Projects are written in Python or TypeScript, and a single repo may mix both.

Rules vary in how they can be checked:

- some map to off-the-shelf linter rules,
- some are deterministic but need a custom lint rule,
- some are semantic judgments no parser can decide.

Generation-time steering (instructions in context) only shifts probability — it
cannot guarantee compliance. So enforcement needs a deterministic layer plus a
judgment layer. We also considered a generator repo that produces per-language
configs and skills from a machine-readable manifest, and judged it overkill at
the current scale (solo, two languages, mixed-language repos).

### Decision

1. **Mechanism per rule, per language.** Every rule is assigned one of
   `builtin` (off-the-shelf linter rule), `custom` (custom lint rule), or
   `review` (Claude review subagent), independently for Python and TypeScript.
   A trailing `*` marks a partial rule — linter does the mechanical part, review
   does the judgment part.

2. **One hand-maintained routing table** in `CLEAN-CODE.md` is the source of
   truth, with a column per language. No generator, no manifest, no build step.

3. **Two enforcement layers.** `builtin`/`custom` rules run deterministically in
   a `PostToolUse` hook (the linter). `review` rules are handled by a single,
   language-agnostic reviewer subagent that filters the table by each file's
   language at runtime.

4. **No per-language artifacts.** Mixed-language repos are handled by runtime
   filtering, not by generating a skill or config per language.

5. **Distributed as one Claude Code plugin.** The reviewer agent, the review
   skill, and the standards (`CLEAN-CODE.md` + examples) are bundled into a
   single plugin so they travel together and stay portable across projects.

### Consequences

**Positive**

- Each rule is enforced by the cheapest mechanism that can handle it; the
  linter and the review subagent never duplicate work.
- One source of truth; the table's language columns give per-language behavior
  with zero duplication.
- The plugin keeps skill, agent, and standards together and installable.

**Negative / trade-offs**

- The table and linter configs are hand-maintained — they can drift. Acceptable
  at solo, two-language scale.
- The reviewer reads all of `CLEAN-CODE.md` (~6k tokens) each run rather than
  lazy-loading. Acceptable because it runs in a throwaway subagent context.
- A third language, or moving to a team / CI, may justify revisiting the
  no-generator decision.

---

## ADR-002 — Clean Architecture deferred, not in this repo

**Status:** Accepted   **Date:** 2026-05-18

### Context

Clean Architecture rules (the Dependency Rule, SOLID, ADP) were considered for
inclusion alongside Clean Code. Analysis showed their *review* value does not
stand on its own:

- The Dependency Rule and ADP are structural — best enforced by import-graph
  linters (`import-linter`, `madge --circular`), not an LLM reviewer.
- SOLID's judgment rules overlap with, or extend, the Clean Code reviewer
  (SRP / OCP / DIP / polymorphism already overlap; LSP / ISP would just be more
  rows in its table).

What remains distinctive about Clean Architecture is **design-time** guidance —
laying out layers and ports when scaffolding an app. That is generative, not
review. The standard is already maintained outside this repo.

### Decision

Do not include Clean Architecture in this repo. Keeping an unused
`CLEAN-ARCHITECTURE.md` here would be dead code (Rule 15).

Revisit only when there is an actual need to **design or scaffold an app** — at
which point Clean Architecture enters as a generative `design-app` skill, not a
review plugin. If structural enforcement is wanted then, it goes to import-graph
linters; SOLID judgment rules go to the Clean Code reviewer's table.

This rejects the earlier idea of a sibling `clean-architecture` review plugin.

### Consequences

**Positive**

- The repo stays focused on Clean Code; no unused standard to maintain.

**Negative / trade-offs**

- Architecture decay (layer violations, import cycles) is not enforced by this
  repo until the decision is revisited; it relies on the externally maintained
  copy.
