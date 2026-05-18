# Visitor

**Category:** Behavioral
**Refactoring Guru:** https://refactoring.guru/design-patterns/visitor
**Priority:** P3 — full example pending

## Intent

Represent an operation to be performed on the elements of an object structure; Visitor lets you define a new operation without changing the classes of the elements on which it operates.

## When to Use

- An object structure contains many classes of objects with differing interfaces, and you want to perform operations on these objects that depend on their concrete classes
- Many distinct and unrelated operations need to be performed on objects in an object structure, and you want to avoid polluting their classes with these operations — Visitor lets you keep related operations together by defining them in one Visitor class
- The classes defining the object structure rarely change, but you often want to define new operations over the structure — changing the object structure classes requires redefining the Visitor interface and all its implementations, which may be costly
- You want to gather related operations into a single class rather than forcing you to change or subclass multiple element classes

## When NOT to Use

- This pattern is rarely needed in typical web/backend TypeScript — prefer simpler alternatives unless the specific use case demands it
- When the object structure classes change frequently — every new element type requires updating all Visitor implementations, which can be an ongoing maintenance burden
- When double dispatch (the mechanism Visitor relies on) is not available in the language without workarounds — modern TypeScript handles this via method overloading on the visitor, but the verbosity is high

## Full Example

See [Refactoring Guru](https://refactoring.guru/design-patterns/visitor) for a complete TypeScript walkthrough.

## Related Patterns

- **Composite** — Visitor is often used to apply an operation across a Composite tree; the `accept` method on each node propagates the visitor through the structure
- **Interpreter** — Visitor may be applied to do the interpretation step in the Interpreter pattern; each node in the AST accepts a visitor that evaluates or transforms it
- **Iterator** — Visitors can be used with Iterators to traverse a structure and apply the operation to each element
