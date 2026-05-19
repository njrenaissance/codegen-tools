# Design Patterns Reference

This directory contains documentation for all 23 GoF (Gang of Four) design patterns, adapted
for modern TypeScript and Python with realistic domain examples.

---

## Attribution

The pattern definitions, structure descriptions, and applicability criteria in these files are
derived from:

> **Design Patterns: Elements of Reusable Object-Oriented Software**
> Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides
> Addison-Wesley, 1994 — ISBN 978-0201633610

Code examples and "When to Use / When NOT to Use" guidance have been augmented and cross-checked
against:

> **Refactoring Guru — Design Patterns**
> Alexander Shvets
> https://refactoring.guru/design-patterns

The TypeScript and Python examples in this directory are original implementations written to
reflect real-world web/backend scenarios rather than abstract toy examples, while remaining
faithful to the structural definitions in the original GoF book.

---

## How to Choose a Pattern

### By Problem Type

| Problem | Pattern(s) to consider |
|---|---|
| Creating objects without specifying the exact class | Factory Method, Abstract Factory |
| Building complex objects step by step | Builder |
| Sharing a single instance across the system | Singleton |
| Making incompatible interfaces work together | Adapter |
| Simplifying a complex subsystem | Facade |
| Adding behaviour to objects without subclassing | Decorator |
| Defining a family of algorithms, making them interchangeable | Strategy |
| Notifying multiple objects about state changes | Observer |
| Passing requests along a chain of handlers | Chain of Responsibility |
| Encapsulating a request as an object (undo, queue, log) | Command |
| Defining a skeleton algorithm, letting subclasses fill in steps | Template Method |
| Allowing an object to alter its behaviour when state changes | State |
| Composing objects into tree structures | Composite |
| Controlling access to an object | Proxy |
| Decoupling many objects from communicating directly | Mediator |
| Copying objects without coupling to their classes | Prototype |
| Saving and restoring object state | Memento |
| Traversing a collection without exposing its structure | Iterator |
| Separating abstraction from implementation | Bridge |
| Supporting many fine-grained objects efficiently | Flyweight |
| Adding operations to an object structure without changing classes | Visitor |

### By Code Smell

| Code smell | Pattern that fixes it |
|---|---|
| `switch`/`if-else` dispatching on a type string or enum | Strategy or Factory Method |
| Objects that know too much about other objects | Facade or Mediator |
| Adding features via subclass explosion | Decorator |
| God class doing everything | Split with Command + Facade |
| Tight coupling to a third-party SDK | Adapter |
| Hard-coded `new ConcreteClass()` in business logic | Factory Method |
| Repeated algorithm with varying steps | Template Method |
| Objects polling for state changes in another object | Observer |
| Long validation or processing pipelines | Chain of Responsibility |
| Constructor with too many parameters | Builder |
| Cross-cutting concerns (logging, caching, auth, retry) | Decorator |

### Strategy vs Template Method

Both define families of algorithms. Choose based on how the variation is introduced:

| | Strategy | Template Method |
|---|---|---|
| Variation via | Composition (inject an object) | Inheritance (override a method) |
| Swap at runtime? | Yes | No |
| Algorithm skeleton | Fully replaced | Partially replaced |
| Prefer when | You need runtime flexibility | Subclasses share most of the algorithm |

### Adapter vs Decorator vs Proxy

All three wrap an object. The intent differs:

| Pattern | Wraps to... | Interface changes? |
|---|---|---|
| Adapter | Convert an incompatible interface | Yes — different before and after |
| Decorator | Add behaviour | No — same interface |
| Proxy | Control access | No — same interface |

### Factory Method vs Abstract Factory

| | Factory Method | Abstract Factory |
|---|---|---|
| Creates | One product type | A family of related product types |
| Extension point | Override a method | Provide a new factory class |
| Use when | Subclasses decide the type | Families must be used together |

---

## Pattern Files

### Creational

| Pattern | Priority | File |
|---|---|---|
| Factory Method | P1 | [creational/factory-method.md](creational/factory-method.md) |
| Abstract Factory | P1 | [creational/abstract-factory.md](creational/abstract-factory.md) |
| Builder | P1 | [creational/builder.md](creational/builder.md) |
| Singleton | P2 | [creational/singleton.md](creational/singleton.md) |
| Prototype | P3 (stub) | [creational/prototype.md](creational/prototype.md) |

### Structural

| Pattern | Priority | File |
|---|---|---|
| Adapter | P1 | [structural/adapter.md](structural/adapter.md) |
| Decorator | P1 | [structural/decorator.md](structural/decorator.md) |
| Facade | P1 | [structural/facade.md](structural/facade.md) |
| Composite | P2 | [structural/composite.md](structural/composite.md) |
| Proxy | P2 | [structural/proxy.md](structural/proxy.md) |
| Bridge | P3 (stub) | [structural/bridge.md](structural/bridge.md) |
| Flyweight | P3 (stub) | [structural/flyweight.md](structural/flyweight.md) |

### Behavioral

| Pattern | Priority | File |
|---|---|---|
| Strategy | P1 | [behavioral/strategy.md](behavioral/strategy.md) |
| Observer | P1 | [behavioral/observer.md](behavioral/observer.md) |
| Command | P1 | [behavioral/command.md](behavioral/command.md) |
| Chain of Responsibility | P1 | [behavioral/chain-of-responsibility.md](behavioral/chain-of-responsibility.md) |
| Template Method | P1 | [behavioral/template-method.md](behavioral/template-method.md) |
| State | P2 | [behavioral/state.md](behavioral/state.md) |
| Iterator | P2 | [behavioral/iterator.md](behavioral/iterator.md) |
| Mediator | P2 | [behavioral/mediator.md](behavioral/mediator.md) |
| Memento | P3 (stub) | [behavioral/memento.md](behavioral/memento.md) |
| Visitor | P3 (stub) | [behavioral/visitor.md](behavioral/visitor.md) |

---

## Sources

- Refactoring Guru: https://refactoring.guru/design-patterns
- Refactoring Guru TypeScript examples: https://refactoring.guru/design-patterns/typescript
