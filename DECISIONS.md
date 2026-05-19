# Decisions

Architecture Decision Records (ADRs) for the Clean Code standards. Newest last.

---

## ADR-001 — Clean Code enforcement architecture

**Status:** Superseded by ADR-002   **Date:** 2026-05-18

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

#### Positive

- Each rule is enforced by the cheapest mechanism that can handle it; the
  linter and the review subagent never duplicate work.
- One source of truth; the table's language columns give per-language behavior
  with zero duplication.
- The plugin keeps skill, agent, and standards together and installable.

#### Negative / trade-offs

- The table and linter configs are hand-maintained — they can drift. Acceptable
  at solo, two-language scale.
- The reviewer reads all of `CLEAN-CODE.md` (~6k tokens) each run rather than
  lazy-loading. Acceptable because it runs in a throwaway subagent context.
- A third language, or moving to a team / CI, may justify revisiting the
  no-generator decision.

---

## ADR-002 — Drop the bundled standard; rely on the model's training

**Status:** Accepted   **Date:** 2026-05-18

### Context

ADR-001 made `CLEAN-CODE.md` — a hand-maintained restatement of ~35 Clean Code
rules plus BAD/GOOD examples — the source of truth. Testing the reviewer
against files with known violations showed Claude identifies and fixes those
violations correctly *without* the bundled file: *Clean Code* (Martin, 2008) is
already in the model's training corpus. The bundled standard was re-encoding
knowledge the model already has.

What the file added over the model's own knowledge was not the rules but their
*calibration* — thresholds, which rules to enforce, the routing of each rule to
a mechanism. The thresholds, though, already live in each project's own
`pyproject.toml` (the lint hook reads that, not `CLEAN-CODE.md`). So the file's
unique contribution was small relative to its size (~6k tokens read every run)
and its maintenance cost.

### Decision

1. **Delete the bundled standard.** `CLEAN-CODE.md` and `references/py.md` /
   `ts.md` are removed. The standard is the book itself, cited by name in the
   agent and skill: *Clean Code* (Robert C. Martin, Prentice Hall, 2008).

2. **Self-contained reviewer.** The reviewer agent carries its own short scope
   (the Clean Code rule areas) inline. It no longer reads an external standards
   file or a routing table.

3. **Review the full standard, every language.** The reviewer is no longer
   restricted to the judgment tier or to Python/TypeScript. It reviews any
   source file against the whole standard and reports every violation —
   accepting overlap with the lint hook rather than risking gaps.

4. **No severity tiers.** Findings are a flat list; each states its concrete
   consequence. Clean Code has no canonical High/Medium/Low ranking, so invented
   per-run tiers were inconsistent and added false precision.

5. **Keep the lint hook.** The `PostToolUse` hook (`lint_on_edit.py`) stays — it
   is the one piece that does something a prompt cannot. Thresholds remain owned
   by each project's `pyproject.toml`.

### Consequences

#### Positive

- No restatement of a copyrighted book to maintain, and nothing to drift out of
  sync with the book.
- The reviewer is smaller, portable, and language-agnostic with no per-language
  table lookup.
- The plugin's value is honestly scoped: a lint hook and a short reviewer
  prompt, not re-supplied knowledge.

#### Negative / trade-offs

- The team's calibration — which rules matter, where the line sits — is no
  longer written down; it lives only in the agent's brief scope list and the
  project lint configs. Less explicit than the old table.
- The reviewer may flag issues the lint hook also catches. Redundancy accepted
  over the risk of gaps.
- The review reflects the model's interpretation of *Clean Code*, which can
  shift between model versions. Accepted at current scale.

This decision rests on a single round of testing; a regression in review
quality would justify revisiting it.
