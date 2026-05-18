# Memento

**Category:** Behavioral
**Refactoring Guru:** https://refactoring.guru/design-patterns/memento
**Priority:** P3 — full example pending

## Intent

Without violating encapsulation, capture and externalize an object's internal state so that the object can be restored to this state later.

## When to Use

- A snapshot of (some portion of) an object's state must be saved so that it can be restored to that state later, and a direct interface to obtaining the state would expose implementation details and break encapsulation
- When you need to implement undo/redo functionality, transactional rollback, or checkpoint-and-restore behavior
- When the object producing the snapshot (the Originator) should be the only one that can write to a Memento — other objects may only read from it (or hold it opaquely)

## When NOT to Use

- This pattern is rarely needed in typical web/backend TypeScript — prefer simpler alternatives unless the specific use case demands it
- When saving the entire state is expensive and only incremental diffs are practical — Memento stores a full snapshot; consider a Command-based approach that stores inverse operations instead
- When the Originator's state is already exposed (e.g., a plain data object) — you can just clone it with `structuredClone` or `JSON.parse(JSON.stringify(...))` without a formal pattern

## Full Example

See [Refactoring Guru](https://refactoring.guru/design-patterns/memento) for a complete TypeScript walkthrough.

## Related Patterns

- **Command** — Commands can use Mementos to maintain undo state for undoable operations
- **Iterator** — Mementos can capture the state of an iteration so it can be rewound
- **Prototype** — Prototypes can sometimes be used instead of Mementos when the Originator is easily cloneable
