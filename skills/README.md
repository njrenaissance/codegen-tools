# Skills

Claude Code skills (slash commands) that enforce engineering standards across all projects.

---

## One-Time Setup

Clone this repo once to a stable global location, then symlink the skills into Claude's global
commands directory.

```bash
# 1. Clone to a permanent location
git clone git@github.com:<your-org>/engineering-standards.git ~/engineering-standards

# 2. Create Claude's global commands directory
mkdir -p ~/.claude/commands

# 3. Symlink all skills
ln -s ~/engineering-standards/skills/clean-review.md       ~/.claude/commands/clean-review.md
ln -s ~/engineering-standards/skills/apply-pattern.md      ~/.claude/commands/apply-pattern.md
ln -s ~/engineering-standards/skills/architecture-check.md ~/.claude/commands/architecture-check.md
ln -s ~/engineering-standards/skills/refactor.md           ~/.claude/commands/refactor.md

# 4. Verify
ls -la ~/.claude/commands/
```

Once symlinked, the skills are available in **every project** via Claude Code.

---

## Skills

### `/clean-review` — [`clean-review.md`](clean-review.md)

Review a file against the full engineering standards suite.

**What it checks:**


1. GoF pattern opportunities and misuses
2. All 32 CLEAN-CODE.md rules (function size, naming, single responsibility, etc.)
3. Clean Architecture layer boundary violations (Dependency Rule)


**Output:** Prioritised violation report grouped by severity (🔴 High / 🟡 Medium / 🟢 Low),
with rule references and suggested fixes.

```bash
/clean-review
/clean-review src/lib/orderService.ts
```

---

### `/apply-pattern <name>` — [`apply-pattern.md`](apply-pattern.md)

Apply a named GoF design pattern to the current file or selection.

**What it does:**


1. Reads the pattern file from `~/engineering-standards/patterns/`
2. Maps the pattern's participants to the existing code
3. Explains why the pattern fits (or doesn't) before making any changes
4. Produces the refactored code with all participants in place
5. Adds `TODO [PATTERN:name]` comments at any touch points in other files


**Available pattern names:**

| Creational | Structural | Behavioral |
|---|---|---|
| `abstract-factory` | `adapter` | `chain-of-responsibility` |
| `builder` | `bridge` | `command` |
| `factory-method` | `composite` | `iterator` |
| `prototype` | `decorator` | `mediator` |
| `singleton` | `facade` | `memento` |
| | `flyweight` | `observer` |
| | `proxy` | `state` |
| | | `strategy` |
| | | `template-method` |
| | | `visitor` |

```bash
/apply-pattern strategy
/apply-pattern factory-method
/apply-pattern observer src/lib/orderService.ts
```

---

### `/architecture-check` — [`architecture-check.md`](architecture-check.md)

Verify that a file respects Clean Architecture layer boundaries.

**What it checks:**


- Detects which layer the file belongs to (Entity, Use Case, Interface Adapter, Framework/Driver)
- Scans all imports and classifies each as valid or a Dependency Rule violation
- Suggests the interface/port that should replace each concrete cross-layer import


**Output:** List of clean imports + violations with specific fix instructions.

```bash
/architecture-check
/architecture-check src/lib/orderService.ts
/architecture-check src/app/api/orders/route.ts
```

---

### `/refactor` — [`refactor.md`](refactor.md)

Full refactor pass on a file — the highest-level skill. Combines all three others into a
structured multi-phase workflow.

**Phases:**


1. Honour existing `TODO [PATTERN:*]` and `TODO [ARCH]` comments
2. Detect and apply new pattern opportunities
3. Fix architecture boundary violations
4. Apply Clean Code pass (function size, naming, guard clauses, magic numbers)
5. Output complete refactored file + diff summary


Use this when you want a comprehensive clean-up, not just one specific fix.

```bash
/refactor
/refactor src/lib/orderService.ts
```

---

## How Pattern TODOs Work

When any skill identifies a pattern opportunity in **existing** code it did not write, it adds a
structured comment rather than making an unrequested change:

```typescript
// TODO [PATTERN:strategy]: Replace switch-on-type with Strategy pattern.
// Each payment provider should be a ConcreteStrategy implementing PaymentGateway.
// Reference: ~/engineering-standards/patterns/behavioral/strategy.md
```

```python
# TODO [ARCH]: orderService imports `prisma` directly — violates Dependency Rule.
# Introduce IOrderRepository interface and inject via constructor.
```

These TODOs are:


- Searchable across the codebase with `grep "TODO \[PATTERN"` or `grep "TODO \[ARCH"`
- Automatically processed by `/refactor` (Phase 1)
- Addressable one at a time with `/apply-pattern <name>`

---

## Per-Project Integration

Add this block to any project's `CLAUDE.md` to activate all standards and auto-detection:

```markdown
## Engineering Standards

All code must comply with the organisation engineering standards.

Read and apply the following on every task:


- **CLAUDE.md (main rules):** `~/engineering-standards/CLAUDE.md`
- **Clean Code:** `~/engineering-standards/CLEAN-CODE.md`
- **Clean Architecture:** `~/engineering-standards/CLEAN-ARCHITECTURE.md`
- **Pattern index:** `~/engineering-standards/patterns/PATTERNS.md`

Available skills (install with symlinks — see `~/engineering-standards/skills/README.md`):
- `/clean-review` — check a file against all standards
- `/apply-pattern <name>` — apply a GoF pattern to selected code
- `/architecture-check` — verify layer boundary compliance
- `/refactor` — full refactor pass
```
