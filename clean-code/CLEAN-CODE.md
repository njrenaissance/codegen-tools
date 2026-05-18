# Clean Code Standards (Robert C. Martin)

Rules for writing clean code, distilled from *Clean Code* (Martin, 2008). Each
rule is stated as a **detection signal** (how to spot the violation) and a
**fix** (what to change).

> **How to use this file when reviewing code**
> When code violates a rule, follow that rule's **Examples** link to the
> ❌ BAD / ✅ GOOD code and fix it to match the ✅ GOOD version.
>
> **Examples** live in [`references/`](references/) —
> Python in [`py.md`](references/py.md) and TypeScript in
> [`ts.md`](references/ts.md).
>
> **Enforcement** — the [Enforcement](#enforcement) section maps
> each rule to a linter rule or the review subagent.

---

## Naming

### Use descriptive, unambiguous names

- **Detection signal:**
  - A name forces the reader to look elsewhere to learn what it holds or does — single letters outside tiny scopes, vague nouns (`data`, `info`, `tmp`, `obj`, `manager`), or names that could mean several things.
  - A name is ambiguous — `rename` that also verifies, or any name that doesn't say what the code does.
  - A name sits at the wrong abstraction level — `phoneNumber` on a generic connection interface.
  - A short name is used across a long scope (single letters belong only in tiny scopes).
  - A name hides a side effect — `getObjectManager` that also creates a singleton.
- **Fix:** Rename to state intent directly and at the right abstraction level (`connectionLocator`); split or rename ambiguous functions (`renameOrVerify`); name side effects (`createObjectManagerIfAbsent`); expand names as scope grows.
- **Examples:** [Python](references/py.md#use-descriptive-unambiguous-names) · [TypeScript](references/ts.md#use-descriptive-unambiguous-names)

---

### Use pronounceable names

- **Detection signal:** A name cannot be said aloud — compressed or vowel-stripped identifiers like `genymdhms`, `pszqint`, `dtRcrd`.
- **Fix:** Replace with real, pronounceable words (`generationTimestamp`) so the name can be spoken in discussion.
- **Examples:** [Python](references/py.md#use-pronounceable-names) · [TypeScript](references/ts.md#use-pronounceable-names)

---

### Use searchable names — avoid magic numbers

- **Detection signal:** A bare numeric or string literal appears in logic, or a single-character name is used where it must be grep-able.
- **Fix:** Extract the literal into a named constant that describes its meaning, so it is both searchable and self-explanatory.
- **Examples:** [Python](references/py.md#use-searchable-names--avoid-magic-numbers) · [TypeScript](references/ts.md#use-searchable-names--avoid-magic-numbers)

---

### Avoid encodings and type noise

- **Detection signal:** A name carries a type or scope prefix — `str_name`, `lst_items`, `i`, `m_count`, interface `IShape`, Hungarian notation.
- **Fix:** Drop the encoding and let the type system carry the type; name the variable for its role.
- **Examples:** [Python](references/py.md#avoid-encodings-and-type-noise) · [TypeScript](references/ts.md#avoid-encodings-and-type-noise)

---

### Be consistent — same pattern everywhere

- **Detection signal:** One concept is named differently across the codebase — `fetch`/`get`/`retrieve` for the same operation, mixed casing for the same kind of thing, or a known pattern (Decorator, Factory, Iterator) applied but not named for it.
- **Fix:** Choose one term per concept and apply it everywhere; use standard nomenclature in the name when a recognized pattern is used.
- **Examples:** [Python](references/py.md#be-consistent--same-pattern-everywhere) · [TypeScript](references/ts.md#be-consistent--same-pattern-everywhere)

---

## Functions

### Functions should be small and do ONE thing

- **Detection signal:** You can extract another function whose name is not merely a restatement of its implementation; the function spans more than a screen; or the function is never called at all.
- **Fix:** Extract sub-functions until each one does a single thing at a single level; delete functions that are dead.
- **Examples:** [Python](references/py.md#functions-should-be-small-and-do-one-thing) · [TypeScript](references/ts.md#functions-should-be-small-and-do-one-thing)

---

### One level of abstraction per function

- **Detection signal:** A function mixes high-level intent with low-level detail — a policy decision sits next to byte-level string manipulation.
- **Fix:** Extract the lower-level steps into named sub-functions so every statement in the function reads at the same conceptual level.
- **Examples:** [Python](references/py.md#one-level-of-abstraction-per-function) · [TypeScript](references/ts.md#one-level-of-abstraction-per-function)

---

### Stepdown Rule — file reads top-to-bottom at decreasing abstraction levels

- **Detection signal:** The reader must jump around the file to follow the flow; a function is not followed by the functions it calls.
- **Fix:** Order functions so each is followed by those one level lower; the top-level function names each step in plain English.
- **Examples:** [Python](references/py.md#stepdown-rule--file-reads-top-to-bottom-at-decreasing-abstraction-levels) · [TypeScript](references/ts.md#stepdown-rule--file-reads-top-to-bottom-at-decreasing-abstraction-levels)

---

### Prefer fewer arguments — use parameter objects when needed

- **Detection signal:** A function takes four or more arguments (more than three is already very questionable), or several arguments that clearly travel together.
- **Fix:** Group related arguments into a typed parameter object.
- **Examples:** [Python](references/py.md#prefer-fewer-arguments--use-parameter-objects-when-needed) · [TypeScript](references/ts.md#prefer-fewer-arguments--use-parameter-objects-when-needed)

---

### Don't use flag arguments — split into separate functions

- **Detection signal:** A boolean or enum parameter selects which behavior the function performs.
- **Fix:** Split into separate, explicitly named functions — one per behavior.
- **Examples:** [Python](references/py.md#dont-use-flag-arguments--split-into-separate-functions) · [TypeScript](references/ts.md#dont-use-flag-arguments--split-into-separate-functions)

---

### No side effects — a function should do what its name says and nothing else

- **Detection signal:** A function does something its name does not advertise — `get_user` also writes to the database, a query also mutates state, or an argument is mutated and used as an output rather than an input.
- **Fix:** Remove the hidden effect, return a value instead of writing through an argument, or rename the function so the effect is declared.
- **Examples:** [Python](references/py.md#no-side-effects--a-function-should-do-what-its-name-says-and-nothing-else) · [TypeScript](references/ts.md#no-side-effects--a-function-should-do-what-its-name-says-and-nothing-else)

---

## Comments

### Explain yourself in code, not in comments

- **Detection signal:** A comment restates what the next lines of code do.
- **Fix:** Delete the redundant comment and make the code self-explanatory — rename identifiers or extract a well-named function.
- **Examples:** [Python](references/py.md#explain-yourself-in-code-not-in-comments) · [TypeScript](references/ts.md#explain-yourself-in-code-not-in-comments)

---

### Use comments to explain INTENT, WARNINGS, and non-obvious decisions

- **Detection signal:**
  - A non-obvious decision, hidden constraint, performance trade-off, or hazard has no explanation the code itself cannot express.
  - A comment holds change history, author metadata, or ticket numbers.
  - A comment no longer matches the code, or is grammatically unclear or rambling.
- **Fix:** Keep only comments that explain *why* — intent, constraint, or warning. Move history and metadata to source control / the issue tracker. Update or delete comments that have drifted from the code; rewrite unclear ones clearly or delete them.
- **Examples:** [Python](references/py.md#use-comments-to-explain-intent-warnings-and-non-obvious-decisions) · [TypeScript](references/ts.md#use-comments-to-explain-intent-warnings-and-non-obvious-decisions)

---

### Never comment out dead code — delete it

- **Detection signal:** Blocks of code are disabled with comment markers instead of removed.
- **Fix:** Delete the commented-out code immediately; source control preserves the history.
- **Examples:** [Python](references/py.md#never-comment-out-dead-code--delete-it) · [TypeScript](references/ts.md#never-comment-out-dead-code--delete-it)

---

## Tests

### One logical assertion per test

- **Detection signal:** A single test exercises and asserts multiple unrelated concepts, so a failure does not say which concept broke.
- **Fix:** Split into one test per concept so each failure is self-diagnosing.
- **Examples:** [Python](references/py.md#one-logical-assertion-per-test) · [TypeScript](references/ts.md#one-logical-assertion-per-test)

---

### Fast — tests should run in milliseconds; no real I/O *(F.I.R.S.T.)*

- **Detection signal:** A test touches a real database, HTTP endpoint, or filesystem; the suite takes seconds or longer.
- **Fix:** Replace real I/O with in-memory fakes, stubs, or mocks so tests run in milliseconds.
- **Examples:** [Python](references/py.md#fast--tests-should-run-in-milliseconds-no-real-io) · [TypeScript](references/ts.md#fast--tests-should-run-in-milliseconds-no-real-io)

---

### Independent — tests must not depend on each other *(F.I.R.S.T.)*

- **Detection signal:** A test fails when run alone or in a different order; it relies on state left by another test.
- **Fix:** Have each test set up its own state and clean up after itself.
- **Examples:** [Python](references/py.md#independent--tests-must-not-depend-on-each-other) · [TypeScript](references/ts.md#independent--tests-must-not-depend-on-each-other)

---

### Readable — test names describe behavior, not implementation *(F.I.R.S.T.)*

- **Detection signal:** A test name describes implementation detail or is generic (`test1`, `testFoo`), so a failure message says nothing about what broke.
- **Fix:** Name the test after the behavior and expected outcome it verifies.
- **Examples:** [Python](references/py.md#readable--test-names-describe-behavior-not-implementation) · [TypeScript](references/ts.md#readable--test-names-describe-behavior-not-implementation)

---

### Test every condition that could break

- **Detection signal:** Test coverage was chosen by "it seems like enough"; no coverage tool is in use, so untested lines are invisible; trivial behavior is left untested.
- **Fix:** Test every condition that could possibly break, including trivial ones — they document behavior cheaply. Run a coverage tool and treat uncovered lines as untested assumptions.

---

### Test boundary conditions and around known bugs

- **Detection signal:** Boundary cases are untested; a bug was found in an area but neighboring behavior was not re-tested.
- **Fix:** Write a test for every boundary condition. Where you find one bug, exhaustively test the surrounding behavior — bugs cluster.

---

### Treat ignored tests and failure patterns as signals

- **Detection signal:** A test is marked ignored or skipped; a group of tests fails together; untested lines are always executed together.
- **Fix:** Treat an ignored test as an unresolved question — resolve the ambiguity, then delete or enable it. Read a shared failure pattern for a common cause instead of fixing tests one by one. Consider extracting always-together untested lines into their own unit.

---

## Design Principles

### Hide internal structure — expose behavior, not data

- **Detection signal:** A class exposes raw fields or plain getters/setters that let callers read and mutate state directly, bypassing invariants.
- **Fix:** Hide the data and expose behavior methods that operate on it.
- **Examples:** [Python](references/py.md#hide-internal-structure--expose-behavior-not-data) · [TypeScript](references/ts.md#hide-internal-structure--expose-behavior-not-data)

---

### Follow the Law of Demeter — talk only to direct neighbors

- **Detection signal:** A train-wreck chain — `a.getB().getC().doD()` — reaches through objects the function does not directly own.
- **Fix:** Ask the direct neighbor to do the work; add a method on it instead of navigating its internals.
- **Examples:** [Python](references/py.md#follow-the-law-of-demeter--talk-only-to-direct-neighbors) · [TypeScript](references/ts.md#follow-the-law-of-demeter--talk-only-to-direct-neighbors)

---

### Single Responsibility — classes should have one reason to change

- **Detection signal:** A class can be forced to change by more than one domain — it handles persistence, notifications, and validation together.
- **Fix:** Split it into one class per responsibility.
- **Examples:** [Python](references/py.md#single-responsibility--classes-should-have-one-reason-to-change) · [TypeScript](references/ts.md#single-responsibility--classes-should-have-one-reason-to-change)

---

### Use dependency injection — don't instantiate collaborators inside classes

- **Detection signal:** A class constructs its own collaborators — `new ConcreteRepo()` hard-coded inside it — making it impossible to test without the real dependency.
- **Fix:** Inject collaborators through the constructor or parameters.
- **Examples:** [Python](references/py.md#use-dependency-injection--dont-instantiate-collaborators-inside-classes) · [TypeScript](references/ts.md#use-dependency-injection--dont-instantiate-collaborators-inside-classes)

---

### Separate multi-threading / async code from business logic

- **Detection signal:** Locks, queues, or async plumbing are interleaved with business logic, so the logic can't be tested without concurrency infrastructure.
- **Fix:** Move concurrency into a thin wrapper layer and keep the business logic free of it.
- **Examples:** [Python](references/py.md#separate-multi-threading--async-code-from-business-logic) · [TypeScript](references/ts.md#separate-multi-threading--async-code-from-business-logic)

---

### Keep it simple (KISS) — reduce complexity

- **Detection signal:** The solution is more elaborate than the problem requires.
- **Fix:** Replace it with the simplest thing that solves the actual problem.
- **Examples:** [Python](references/py.md#keep-it-simple-kiss--reduce-complexity) · [TypeScript](references/ts.md#keep-it-simple-kiss--reduce-complexity)

---

### Prefer value objects over primitives

- **Detection signal:** Raw strings or numbers are passed around carrying implicit rules that nothing enforces (a "valid email", a "positive amount").
- **Fix:** Wrap the primitive in a value object that validates on construction, making illegal states unrepresentable.
- **Examples:** [Python](references/py.md#prefer-value-objects-over-primitives) · [TypeScript](references/ts.md#prefer-value-objects-over-primitives)

---

### Rigidity — don't make changes that cascade everywhere

- **Detection signal:** Satisfying one requirement change forces edits across many files — adding a payment type means editing five modules.
- **Fix:** Localize the concept so a single change ripples through as few modules as possible.
- **Examples:** [Python](references/py.md#rigidity--dont-make-changes-that-cascade-everywhere) · [TypeScript](references/ts.md#rigidity--dont-make-changes-that-cascade-everywhere)

---

### Opacity — deeply nested code is hard to read; flatten it

- **Detection signal:** Deeply nested conditionals or loops force the reader to hold many levels of context at once.
- **Fix:** Apply guard clauses / early returns to handle exceptional cases first and flatten the body.
- **Examples:** [Python](references/py.md#opacity--deeply-nested-code-is-hard-to-read-flatten-it) · [TypeScript](references/ts.md#opacity--deeply-nested-code-is-hard-to-read-flatten-it)

---

### Needless complexity — don't over-engineer

- **Detection signal:** An abstraction or generality exists for a hypothetical future need, not a current one.
- **Fix:** Remove it; keep the concrete code until real duplication justifies the abstraction.
- **Examples:** [Python](references/py.md#needless-complexity--dont-over-engineer) · [TypeScript](references/ts.md#needless-complexity--dont-over-engineer)

---

## Miscellaneous

Rules that don't fall under naming, functions, comments, tests, or design —
code formatting, error handling, and the general/environment heuristics.

### Boy Scout Rule — leave code cleaner than you found it

- **Detection signal:** You are editing a file that still contains dead or unreachable code, unused variables, dead functions, meaningless comments, poor names, or missing type hints.
- **Fix:** Clean up that clutter as part of the change, so the file leaves your hands cleaner than it arrived.
- **Examples:** [Python](references/py.md#boy-scout-rule--leave-code-cleaner-than-you-found-it) · [TypeScript](references/ts.md#boy-scout-rule--leave-code-cleaner-than-you-found-it)

---

### Declare variables close to their usage

- **Detection signal:** A variable is declared well above its first use, forcing the reader to scroll and remember.
- **Fix:** Move the declaration to just above its first use.
- **Examples:** [Python](references/py.md#declare-variables-close-to-their-usage) · [TypeScript](references/ts.md#declare-variables-close-to-their-usage)

---

### Place caller above callee — high-level first

- **Detection signal:** A function is defined above the function that calls it, so the file does not read top-down.
- **Fix:** Reorder so every function appears above the functions it calls — headline first, detail below.
- **Examples:** [Python](references/py.md#place-caller-above-callee--high-level-first) · [TypeScript](references/ts.md#place-caller-above-callee--high-level-first)

---

### Always find the root cause — don't suppress errors silently

- **Detection signal:** An empty catch block, a swallowed exception, or a generic error that hides whether it was "not found" or "database down".
- **Fix:** Handle or propagate a specific error, and fix the underlying cause rather than masking the failure.
- **Examples:** [Python](references/py.md#always-find-the-root-cause--dont-suppress-errors-silently) · [TypeScript](references/ts.md#always-find-the-root-cause--dont-suppress-errors-silently)

---

### Build and tests run in one step

- **Detection signal:** Building the project, or running its tests, requires more than one command or manual step.
- **Fix:** Automate each to a single command.

---

### Implement obvious and boundary behavior

- **Detection signal:** A function ignores edge cases callers would reasonably expect, or behaves incorrectly at the boundaries because those cases are untested.
- **Fix:** Implement the behavior callers expect, and write a test for every boundary condition (wrap scattered `+1`/`-1` boundary arithmetic in a named function or constant).

---

### Don't override safeties

- **Detection signal:** Compiler warnings are disabled or tests are skipped to make the build pass.
- **Fix:** Re-enable them and fix the root cause.

---

### Remove duplication

- **Detection signal:** The same logic appears in more than one place.
- **Fix:** Extract it to a single source of truth (DRY).

---

### Keep code at one level of abstraction

- **Detection signal:** High-level intent and low-level detail are mixed in one place, or a function descends more than one level of abstraction.
- **Fix:** Extract detail into named sub-functions — see [*One level of abstraction per function*](#one-level-of-abstraction-per-function).

---

### Avoid base classes that depend on their derivatives

- **Detection signal:** A base class references or knows about its subclasses.
- **Fix:** Invert the dependency so the base class is independent of its derivatives.

---

### Narrow the public surface

- **Detection signal:** A class or module exposes a fat interface, many public fields, or more information than callers need.
- **Fix:** Reduce the public surface to the minimum callers actually require.

---

### Keep things in their natural home

- **Detection signal:** Unrelated things are coupled for convenience (artificial coupling); a method uses another class's data more than its own (feature envy); or code lives somewhere a reader would not look for it (misplaced responsibility).
- **Fix:** Move each piece of code and data to the place it naturally belongs.

---

### Make static methods polymorphic when behavior varies

- **Detection signal:** A static method should vary by type but cannot be overridden.
- **Fix:** Make it an instance method or virtual.

---

### Use explanatory variables and encapsulate conditionals

- **Detection signal:** A run-on or hard-to-read expression has no explanatory variable; a compound conditional like `if (timer.hasExpired() && !timer.isRecurrent())` states mechanics, not intent.
- **Fix:** Introduce a well-named intermediate variable or extract the condition, e.g. `if (shouldBeDeleted(timer))`.

---

### Functions and their names should say what they do

- **Detection signal:** A function does more than one thing, or its name doesn't match its behavior — `rename` that also verifies.
- **Fix:** Make the function do one thing and rename or split it so the name is exact — see [*Functions should be small and do ONE thing*](#functions-should-be-small-and-do-one-thing).

---

### Understand the algorithm

- **Detection signal:** Code works but you cannot explain why.
- **Fix:** Replace it with code you can reason about.

---

### Make logical dependencies physical

- **Detection signal:** Functions must be called in a specific order, but nothing enforces it (hidden temporal coupling).
- **Fix:** Chain return values — pass each call's result as the next call's argument — so out-of-order calls are impossible.

---

### Prefer polymorphism to if/else and switch chains

- **Detection signal:** If/else or switch/case chains branch on a type or kind.
- **Fix:** Replace the branching with polymorphism; flatten remaining nesting with guard clauses.

---

### Follow standard conventions

- **Detection signal:** The code ignores the language's or team's standard conventions.
- **Fix:** Follow them; don't solve a simple problem with a complex or non-standard solution.

---

### Replace magic numbers with named constants

- **Detection signal:** A bare numeric or string literal appears in logic.
- **Fix:** Replace it with a named constant — see [*Use searchable names — avoid magic numbers*](#use-searchable-names--avoid-magic-numbers).

---

### Be precise

- **Detection signal:** Vague types or ambiguous return values leave failure modes unclear.
- **Fix:** Use the most specific type available and be explicit about how and when the code fails.

---

### Enforce structure with types, not conventions

- **Detection signal:** Correctness relies on a naming convention that a developer can silently violate.
- **Fix:** Enforce the rule through types and the compiler, not naming alone.

---

### Avoid negative conditionals

- **Detection signal:** A conditional is expressed negatively and is harder to read.
- **Fix:** Rephrase it as a positive conditional — it reads more directly.

---

### Don't be arbitrary

- **Detection signal:** Code structure has no apparent reason.
- **Fix:** Document the reason or restructure it so the intent is clear.

---

### Keep configurable data at high levels

- **Detection signal:** Magic values and defaults are buried deep in low-level code.
- **Fix:** Hoist them into named constants at the top level.

---

### Avoid transitive navigation (train wrecks)

- **Detection signal:** Code navigates through objects it doesn't own — `a.getB().getC()`.
- **Fix:** Talk only to direct neighbors — see [*Follow the Law of Demeter — talk only to direct neighbors*](#follow-the-law-of-demeter--talk-only-to-direct-neighbors).

---

### Avoid multiple languages in one source file

- **Detection signal:** A source file mixes more than one language.
- **Fix:** Minimize it; aim for one language per file.

---

## Enforcement

Each rule is enforced by a **mechanism**, and the mechanism can differ by
language:

- **`builtin`** — an off-the-shelf linter rule; configure it, write no code. (Rule IDs live in the linter config, not here.)
- **`custom`** — deterministic, but no built-in rule exists; write a custom lint rule (an eslint plugin, or a flake8 plugin / `ast` script for Python — ruff is not plugin-extensible).
- **`review`** — semantic judgment no parser can decide; the Claude review pass handles it.
- A trailing **`*`** marks a *partial* rule — the linter catches the mechanical part, the review pass covers the remaining judgment.

`builtin` and `custom` run deterministically in the `PostToolUse` hook; `review`
is the backstop for everything else.

> **How Claude knows the detection, fix, and examples for a rule** — this table
> is only a router. Each rule name links to its full entry above, which already
> states the **Detection signal**, the **Fix**, and the **Examples** (linked
> Python / TypeScript code). The review pass follows that link for any `review`
> row; the detail is never duplicated here.

|Group|Rule|Python|TypeScript|
|---|---|---|---|
|Naming|[Use descriptive, unambiguous names](#use-descriptive-unambiguous-names)|`review`|`builtin*`|
|Naming|[Use pronounceable names](#use-pronounceable-names)|`review`|`review`|
|Naming|[Use searchable names — avoid magic numbers](#use-searchable-names--avoid-magic-numbers)|`builtin`|`builtin`|
|Naming|[Avoid encodings and type noise](#avoid-encodings-and-type-noise)|`builtin*`|`builtin`|
|Naming|[Be consistent — same pattern everywhere](#be-consistent--same-pattern-everywhere)|`builtin*`|`builtin*`|
|Functions|[Functions should be small and do ONE thing](#functions-should-be-small-and-do-one-thing)|`builtin*`|`builtin*`|
|Functions|[One level of abstraction per function](#one-level-of-abstraction-per-function)|`review`|`review`|
|Functions|[Stepdown Rule](#stepdown-rule--file-reads-top-to-bottom-at-decreasing-abstraction-levels)|`custom*`|`custom*`|
|Functions|[Prefer fewer arguments](#prefer-fewer-arguments--use-parameter-objects-when-needed)|`builtin`|`builtin`|
|Functions|[Don't use flag arguments](#dont-use-flag-arguments--split-into-separate-functions)|`custom`|`custom`|
|Functions|[No side effects](#no-side-effects--a-function-should-do-what-its-name-says-and-nothing-else)|`review`|`builtin*`|
|Comments|[Explain yourself in code, not in comments](#explain-yourself-in-code-not-in-comments)|`review`|`review`|
|Comments|[Use comments for intent / warnings](#use-comments-to-explain-intent-warnings-and-non-obvious-decisions)|`review`|`review`|
|Comments|[Never comment out dead code](#never-comment-out-dead-code--delete-it)|`builtin`|`builtin`|
|Tests|[One logical assertion per test](#one-logical-assertion-per-test)|`custom*`|`custom*`|
|Tests|[Fast — no real I/O](#fast--tests-should-run-in-milliseconds-no-real-io-first)|`custom`|`custom`|
|Tests|[Independent tests](#independent--tests-must-not-depend-on-each-other-first)|`custom*`|`custom*`|
|Tests|[Readable test names](#readable--test-names-describe-behavior-not-implementation-first)|`custom*`|`custom*`|
|Tests|[Test every condition that could break](#test-every-condition-that-could-break)|`review`|`review`|
|Tests|[Test boundary conditions and known bugs](#test-boundary-conditions-and-around-known-bugs)|`review`|`review`|
|Tests|[Treat ignored tests as signals](#treat-ignored-tests-and-failure-patterns-as-signals)|`review`|`review`|
|Design|[Hide internal structure](#hide-internal-structure--expose-behavior-not-data)|`review`|`review`|
|Design|[Follow the Law of Demeter](#follow-the-law-of-demeter--talk-only-to-direct-neighbors)|`custom`|`custom`|
|Design|[Single Responsibility](#single-responsibility--classes-should-have-one-reason-to-change)|`review`|`review`|
|Design|[Use dependency injection](#use-dependency-injection--dont-instantiate-collaborators-inside-classes)|`custom*`|`custom*`|
|Design|[Separate concurrency from business logic](#separate-multi-threading--async-code-from-business-logic)|`review`|`review`|
|Design|[Keep it simple (KISS)](#keep-it-simple-kiss--reduce-complexity)|`review`|`review`|
|Design|[Prefer value objects over primitives](#prefer-value-objects-over-primitives)|`review`|`review`|
|Design|[Rigidity — changes that cascade](#rigidity--dont-make-changes-that-cascade-everywhere)|`review`|`review`|
|Design|[Opacity — deep nesting](#opacity--deeply-nested-code-is-hard-to-read-flatten-it)|`builtin`|`builtin`|
|Design|[Needless complexity](#needless-complexity--dont-over-engineer)|`review`|`review`|
|Misc|[Boy Scout Rule](#boy-scout-rule--leave-code-cleaner-than-you-found-it)|`review`|`review`|
|Misc|[Declare variables close to usage](#declare-variables-close-to-their-usage)|`custom`|`custom`|
|Misc|[Place caller above callee](#place-caller-above-callee--high-level-first)|`custom`|`custom`|
|Misc|[Always find the root cause](#always-find-the-root-cause--dont-suppress-errors-silently)|`builtin*`|`builtin*`|

The remaining Miscellaneous heuristics in this file default to `review` for both
languages — most are judgment calls, and several restate a rule above.

**The linter** runs every `builtin` and `custom` cell in the `PostToolUse` hook.
**The review pass** handles every `review` cell — and the `*` (judgment) half of
every partial rule. Promoting a rule from `review` to `custom`/`builtin` is the
only way the review pass gets shorter.
