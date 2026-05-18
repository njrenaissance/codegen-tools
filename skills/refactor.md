# /refactor

Full refactor pass on the current file: fix pattern violations, apply clean code rules,
and correct architecture boundary issues — in the right order.

**Usage:**

```bash
/refactor
/refactor src/lib/orderService.ts
```

## What to do

Work through the following phases in order. Do not skip phases. Do not batch all changes into one
output — walk through each phase so the user can follow the reasoning.

---

### Phase 0 — Read everything needed

- Read the target file
- Read `~/engineering-standards/CLAUDE.md` (Part 2 — Standing Instructions)
- Read `~/engineering-standards/CLEAN-CODE.md`
- Read `~/engineering-standards/CLEAN-ARCHITECTURE.md`

---

### Phase 1 — Honour existing TODOs

Grep the file for `TODO [PATTERN:`. For each one found:
- Read the referenced pattern file
- Apply the pattern as described in `/apply-pattern` logic
- Remove the TODO comment once applied

---

### Phase 2 — Detect new pattern opportunities

Using the detection table from CLAUDE.md Part 2, scan for signals not already covered by Phase 1.
For each new opportunity:
- Apply the pattern if it is clearly the right call and the change is contained to this file
- Add a `TODO [PATTERN:name]` if the fix requires touching other files (to avoid scope creep)

---

### Phase 3 — Architecture fixes

Run the logic from `/architecture-check` on the file.
For each violation:
1. Define the missing interface/port (in the correct layer)
2. Update the import to use the interface
3. Add a `TODO [ARCH]` on any concrete implementation file that needs to be created or moved

```typescript
// TODO [ARCH]: Create PrismaOrderRepository implementing IOrderRepository
// in src/repositories/prismaOrderRepository.ts and wire it in the DI root.
```

---

### Phase 4 — Clean Code pass

Apply CLEAN-CODE.md rules in this priority order:

1. **Function size** — extract any function over 20 lines into named sub-functions
   - Use the stepdown rule: high-level function at top, helpers below
   - Name each extracted function after what it does (verb phrase)

2. **One level of abstraction per function** — mix of high-level and low-level logic in one function = split

3. **Guard clauses** — replace nested `if/else` with early returns
   ```typescript
   // Before
   if (user) { if (user.active) { ... } }
   // After
   if (!user) return;
   if (!user.active) return;
   ```

4. **Flag arguments** — split `send(message, true)` into `sendNow(message)` / `queue(message)`

5. **Magic numbers** — extract to named constants at the top of the file

6. **Naming** — rename anything where you had to read the body to understand the name

7. **Dead code** — remove commented-out blocks; remove unused variables and imports

8. **Comments** — delete comments that say WHAT; keep only comments that say WHY (non-obvious constraint, workaround, invariant)

---

### Phase 5 — Final output

Produce the complete refactored file. Then output a brief diff summary:

```
## What changed

### Patterns applied
- Strategy: extracted PaymentProvider logic from switch-on-type (lines 34–58)
  → PaymentGateway interface + StripeProvider, PayPalProvider ConcreteStrategies

### Architecture fixes
- Removed `prisma` import from Use Case layer
  → Introduced IOrderRepository interface; concrete impl deferred (TODO [ARCH] added)

### Clean Code
- Extracted `validateOrder()`, `applyDiscounts()`, `persistOrder()` from 89-line `handleOrder`
- Removed 3 magic numbers → ORDER_EXPIRY_DAYS, MAX_ITEMS, MIN_AMOUNT
- Replaced 2 flag arguments with explicit method names
```

Do not produce the summary until the full refactored file is shown.
