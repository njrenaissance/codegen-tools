# Bridge

**Category:** Structural
**Refactoring Guru:** https://refactoring.guru/design-patterns/bridge
**Priority:** P3 — full example pending

## Intent

Decouple an abstraction from its implementation so that the two can vary independently.

## When to Use

- You want to avoid a permanent binding between an abstraction and its implementation — for example, when the implementation must be selected or switched at runtime
- Both the abstraction and its implementation should be extensible through subclassing; Bridge lets you combine different abstractions and implementations independently
- Changes in the implementation of an abstraction should have no impact on clients — their code should not need to be recompiled
- You have a proliferation of classes caused by coupling an abstraction with multiple implementations (the "Cartesian product" explosion: e.g., Shape × Color creates RedCircle, BlueCircle, RedSquare, BlueSquare...)
- You want to share an implementation among multiple objects (e.g., using reference counting) and this should be hidden from the client

## When NOT to Use

- This pattern is rarely needed in typical web/backend TypeScript — prefer simpler alternatives unless the specific use case demands it
- When the abstraction and implementation are unlikely to vary independently — the additional layer of indirection adds complexity without payoff
- When there is only one implementation — the pattern's separation provides no benefit

## Full Example

See [Refactoring Guru](https://refactoring.guru/design-patterns/bridge) for a complete TypeScript walkthrough.

## Related Patterns

- **Abstract Factory** — can create and configure a particular Bridge; the factory hides the details of how the implementation is connected to the abstraction
- **Adapter** — is geared towards making unrelated classes work together; Bridge is designed up-front to let abstraction and implementation vary independently
- **Strategy** — is similar in structure to Bridge; the difference is that Strategy focuses on interchangeable algorithms while Bridge separates an abstraction's interface from its implementation
