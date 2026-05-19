# /apply-pattern

Apply a named GoF design pattern to the current file or selection.

**Usage:**

```bash
/apply-pattern strategy
/apply-pattern factory-method
/apply-pattern observer src/lib/orderService.ts
```

## What to do

1. **Identify the pattern and target**
   - Parse the pattern name from the arguments (e.g. `strategy`, `factory-method`, `observer`)
   - If a file path is provided, use it; otherwise use the currently open file
   - Map the pattern name to its file:
     - Creational: `abstract-factory`, `builder`, `factory-method`, `prototype`, `singleton`
     - Structural: `adapter`, `bridge`, `composite`, `decorator`, `facade`, `flyweight`, `proxy`
     - Behavioral: `chain-of-responsibility`, `command`, `iterator`, `mediator`, `memento`,
       `observer`, `state`, `strategy`, `template-method`, `visitor`

2. **Read the pattern file**
   - Load `patterns/<category>/<pattern-name>.md`
   - Study Intent, When to Use, When NOT to Use, Structure, and ✅ example

3. **Read the target file**

4. **Assess fit**
   Before making any changes, explain:
   - **Why this pattern fits** (map the pattern's "When to Use" bullets to specific lines in the file)
   - **Participants mapping** — identify which existing classes/functions become which pattern participants
     (e.g. "OrderService becomes the Context; StripeProvider and PayPalProvider become ConcreteStrategies")
   - **What will change** — list the specific structural changes required

   If the pattern does NOT fit, say so clearly and suggest the pattern that does fit instead.
   Do not apply a pattern that is a poor fit just because the user asked for it.

5. **Apply the pattern**

   Follow the ✅ example structure from the pattern file. Produce the refactored code:

   - **Extract interfaces first** — define the abstract role (Strategy, Component, Command, etc.)
   - **Rename existing classes** to match their new participant role if needed
   - **Introduce new participants** (Factories, Decorators, Observers, etc.) as required
   - **Update the call site** — show how the context/client wires everything together
   - Keep all existing behaviour intact — this is a structural refactor, not a feature change
   - Follow CLEAN-CODE.md rules in any new code written (no magic numbers, descriptive names, etc.)
   - Follow the Dependency Rule — new interfaces belong to the layer that uses them

6. **Add pattern TODOs for anything deferred**
   If the full refactor would touch files not currently open, add a `TODO [PATTERN:name]` comment
   at each touch point listing what needs to change, so work can continue incrementally.

7. **Summarize**
   After producing the refactored code, output a one-paragraph summary:
   - Which participant maps to what
   - What the concrete benefit is (testability, extensibility, SRP, etc.)
   - What to do next (e.g. "Add a ConcreteStrategy per new payment provider without touching OrderService")
