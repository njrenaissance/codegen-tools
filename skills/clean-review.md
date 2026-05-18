# /clean-review

Review the current file (or a specified file) against the organisation's engineering standards.
Produces a prioritised list of violations with rule references and suggested fixes.

## What to do

1. **Identify the target file**
   - If the user passed a file path as an argument, use that
   - Otherwise use the file currently open in the editor (from IDE context)
   - If neither is clear, ask the user which file to review

2. **Read the standards**
   - Read `~/engineering-standards/CLEAN-CODE.md` — 40 Clean Code rules
   - Read `~/engineering-standards/CLEAN-ARCHITECTURE.md` — SOLID + architecture rules
   - Read `~/engineering-standards/patterns/README.md` — pattern decision table

3. **Read the target file**

4. **Run three passes — in order**

   ### Pass 1 — Pattern Detection
   Using the pattern detection table in `~/engineering-standards/CLAUDE.md` (Part 2), scan for:
   - Code that SHOULD use a pattern but doesn't (opportunity)
   - Code that uses a pattern incorrectly (misuse)

   For each finding, record:
   - Location (line number or function name)
   - Which pattern applies
   - One sentence describing the fix
   - Reference path to the pattern file

   ### Pass 2 — Clean Code Rules
   Check against CLEAN-CODE.md. Prioritise in this order:
   1. Function size (> 20 lines is a warning, > 40 is a violation)
   2. Naming (non-descriptive names, abbreviations, type-in-name)
   3. Function does more than one thing (side-effects + return, multiple levels of abstraction)
   4. Magic numbers / unexplained literals
   5. Flag arguments (bool params that change behaviour)
   6. Deeply nested conditionals (> 3 levels — suggest guard clauses)
   7. Dead code or commented-out code
   8. Comments that explain WHAT instead of WHY

   ### Pass 3 — Architecture Check
   Determine the file's layer from its path:
   - `entities/` or `domain/` → Entity layer
   - `use-cases/`, `usecases/`, `lib/` → Use Case layer
   - `controllers/`, `routes/`, `api/` → Interface Adapter layer
   - `services/` (infrastructure), `adapters/`, `repositories/` → Framework/Driver layer

   Then check every `import` statement:
   - Flag any import from a more-outer layer into a more-inner layer (Dependency Rule violation)
   - Flag any framework import (`next/`, `express`, `prisma`) in a Use Case or Entity file
   - Suggest the interface/port that should replace the concrete import

5. **Output format**

   Group findings by severity. Use this structure:

   ```
   ## Pattern Opportunities
   - Line 42 [PATTERN:strategy]: `processPayment` uses a switch on `provider` type.
     → Apply Strategy: each provider becomes a ConcreteStrategy implementing `PaymentGateway`.
     → Reference: ~/engineering-standards/patterns/behavioral/strategy.md

   ## Clean Code Violations
   ### 🔴 High
   - Line 12 [CC-19 Function Size]: `handleOrder` is 87 lines. Max recommended: 20.
     → Extract: `validateInventory()`, `applyDiscounts()`, `persistOrder()`

   ### 🟡 Medium
   - Line 34 [CC-07 Naming]: `d` should be `discountAmount`
   - Line 58 [CC-22 Flag Argument]: `send(message, true)` — split into `sendNow()` / `queue()`

   ### 🟢 Low
   - Line 91 [CC-33 Comments]: Comment explains what the code does, not why.

   ## Architecture Violations
   - Line 3 [DEP-RULE]: Use case imports `NextResponse` from `next/server`.
     → Return a plain object; let the controller convert it to NextResponse.
   ```

6. **After outputting the report**
   - Ask the user: "Would you like me to apply any of these fixes?"
   - If yes for a pattern fix, invoke the logic from `/apply-pattern`
   - If yes for a clean code fix, apply the specific change inline
