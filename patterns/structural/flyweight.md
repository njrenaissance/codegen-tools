# Flyweight

**Category:** Structural
**Refactoring Guru:** https://refactoring.guru/design-patterns/flyweight
**Priority:** P3 — full example pending

## Intent

Use sharing to support large numbers of fine-grained objects efficiently.

## When to Use

- An application uses a large number of objects (hundreds of thousands or millions)
- Storage costs are high because of the sheer quantity of objects
- Most object state can be made extrinsic (moved outside the object and passed in by the caller)
- Many groups of objects may be replaced by relatively few shared objects once extrinsic state is removed
- The application does not depend on object identity — since Flyweight objects are shared, identity tests will return `true` for what are conceptually distinct objects

## When NOT to Use

- This pattern is rarely needed in typical web/backend TypeScript — prefer simpler alternatives unless the specific use case demands it
- When the number of objects is small or memory is not a concern — the complexity of separating intrinsic and extrinsic state is not worth it
- When most of the object's state is intrinsic (unique per instance) — there is little sharing to be done

## Full Example

See [Refactoring Guru](https://refactoring.guru/design-patterns/flyweight) for a complete TypeScript walkthrough.

## Related Patterns

- **Composite** — Flyweight is often combined with Composite to implement shared leaf nodes in a tree structure
- **State** and **Strategy** — State and Strategy objects are good candidates for Flyweights when they carry no instance-specific data
- **Singleton** — a Flyweight factory is often implemented as a Singleton so there is one canonical registry of shared flyweights
