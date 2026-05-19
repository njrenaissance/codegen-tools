# patterns

GoF design patterns reference for Python and TypeScript. Bundles all 23 pattern
files and an `/apply-pattern` skill that maps a named pattern onto existing code.

## Contents

- **[PATTERNS.md](PATTERNS.md)** — the routing file: "How to Choose a Pattern"
  tables (by problem type, by code smell) and the index of all 23 pattern files.
- **`creational/`, `structural/`, `behavioral/`** — one file per pattern, each
  with Intent, When to Use / When NOT to Use, Structure, and worked examples.
- **`skills/apply-pattern/`** — the `/apply-pattern` skill.

## Usage

```text
/apply-pattern strategy
/apply-pattern factory-method
/apply-pattern observer src/lib/orderService.ts
```

Start with [PATTERNS.md](PATTERNS.md) if you are not sure which pattern you need.
