# Codegen Tools

A Claude Code **plugin marketplace** holding the code-generation standards used across projects:
Clean Code enforcement, a design-pattern reference, and a Conventional Commits skill.

It ships three plugins:

|Component|Type|What it does|
|---|---|---|
|`clean-code`|Plugin|Enforces Clean Code rules for Python and TypeScript|
|`patterns`|Plugin|GoF design-pattern reference with an `/apply-pattern` skill|
|`git-workflow`|Plugin|`/refresh` command plus a Conventional Commits skill|

---

## Plugins

### `clean-code`

Clean Code standards for Python and TypeScript, enforced in three tiers — each rule is routed to
the cheapest mechanism that can enforce it:

- **Linter (`builtin` / `custom`)** — a `PostToolUse` hook runs `ruff` on every edited `.py`
  file. It uses *the project's own* ruff config — it never overrides your settings — and feeds
  any findings back to Claude to fix in-loop.
- **Review (`review`)** — the judgment-based rules a linter cannot check (Single Responsibility,
  one level of abstraction, KISS, meaningful comments). Handled by the bundled
  `clean-code-reviewer` subagent, invoked through the `clean-code-review` skill.

Contents:

- `CLEAN-CODE.md` — the standard: ~35 rules as detection-signal / fix pairs, plus the
  **Enforcement** routing table (mechanism per rule per language).
- `agents/clean-code-reviewer.md` — the review subagent.
- `skills/clean-code-review/` — skill that dispatches a diff or named files to the reviewer.
- `hooks/` — the `PostToolUse` lint hook (`lint_on_edit.py`).
- `references/py.md`, `references/ts.md` — BAD/GOOD code examples per rule.

### `patterns`

All 23 Gang of Four design patterns, adapted for modern TypeScript and Python.

- `PATTERNS.md` — the routing file: "How to Choose a Pattern" tables (by problem, by code smell).
- `README.md` — plugin overview.
- `creational/`, `structural/`, `behavioral/` — one file per pattern: Intent, When to Use,
  When NOT to Use, Structure, and worked examples.
- `skills/apply-pattern/` — the `/apply-pattern <name>` skill: maps a named pattern onto your
  existing code, explains the fit first, then refactors.

### `git-workflow`

Git workflow helpers.

- `commands/refresh.md` — the `/refresh` command: syncs the working branch back to an
  up-to-date `main` after branch work.
- `skills/commit/` — the `commit` skill: writes Conventional Commits v1.0.0 messages. Claude
  invokes it automatically when you say "commit this" — no slash command needed.

---

## Setup

### 1. Register the marketplace

From Claude Code, point it at this repo once:

```text
/plugin marketplace add njrenaissance/codegen-tools
```

Or, for a local clone:

```text
/plugin marketplace add c:/Users/jon_m/github/codegen-tools
```

### 2. Install the plugins

```text
/plugin install clean-code@codegen-tools
/plugin install patterns@codegen-tools
/plugin install git-workflow@codegen-tools
```

All three are now available in every project where Claude Code runs.

### 3. Wire up ruff for the `clean-code` lint hook

The hook runs `ruff` with **your project's** config — so the Clean Code linter rules only fire
if your project opts into them. Add this block to each project's `pyproject.toml`. It is
**additive** (`extend-select`) — it does not replace your existing `select`:

```toml
[tool.ruff.lint]
extend-select = ["PLR2004", "PLR0915", "C901", "PLR0913", "PLR1702", "ERA001", "N", "S110", "BLE001"]

[tool.ruff.lint.mccabe]
max-complexity = 10

[tool.ruff.lint.pylint]
max-args = 4
max-statements = 40
max-nested-blocks = 3

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["PLR2004", "S101"]
```

The hook invokes ruff via `uv run ruff` (your project's pinned version), falling back to a
`ruff` on `PATH`, then `uvx ruff`.

---

## Repository layout

```text
.claude-plugin/marketplace.json   Marketplace manifest (lists all three plugins)
clean-code/                       The clean-code plugin
patterns/                         The patterns plugin
git-workflow/                     The git-workflow plugin (/refresh + commit skill)
DECISIONS.md                      Architecture Decision Records
```

## Decisions

The "why" behind this architecture — three-tier enforcement, plugin packaging, ruff config
ownership — is recorded in [DECISIONS.md](DECISIONS.md).
