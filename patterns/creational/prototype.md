# Prototype

**Category:** Creational
**Refactoring Guru:** https://refactoring.guru/design-patterns/prototype
**Priority:** P3 — full example pending

## Intent

Specify the kinds of objects to create using a prototypical instance, and create new objects by copying this prototype.

## When to Use

- When the classes to instantiate are specified at runtime (e.g., by dynamic loading)
- When you want to avoid building a class hierarchy of factories that parallels the class hierarchy of products
- When instances of a class can have only one of a few different combinations of state — it is more convenient to install a corresponding number of prototypes and clone them rather than instantiating the class manually each time with the appropriate state
- When object creation is expensive (e.g., requires a database lookup or heavy computation) and an existing object with the right state can be cloned instead

## When NOT to Use

- This pattern is rarely needed in typical web/backend TypeScript — prefer simpler alternatives unless the specific use case demands it
- When objects contain circular references or references to objects that cannot be cloned — deep cloning becomes complex and error-prone
- When constructors are cheap and the class hierarchy is stable — direct instantiation is simpler

## Full Example

See [Refactoring Guru](https://refactoring.guru/design-patterns/prototype) for a complete TypeScript walkthrough.

## Related Patterns

- **Abstract Factory** — often stores a set of prototypes and returns cloned products
- **Composite** and **Decorator** — designs that make heavy use of these patterns can often benefit from Prototype as well
- **Command** — Command objects are sometimes implemented as Prototypes so they can be stored and replayed later
