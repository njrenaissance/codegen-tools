# Decorator

**Category:** Structural
**Refactoring Guru:** https://refactoring.guru/design-patterns/decorator

## Intent

Attach additional responsibilities to an object dynamically, providing a flexible alternative to subclassing for extending functionality.

## When to Use

- You want to add behaviour to individual objects without affecting other objects of the same class
- Extension by subclassing is impractical because it produces an explosion of subclasses for every combination of behaviours
- You need to add/remove responsibilities at runtime
- Cross-cutting concerns like logging, caching, validation, or auth need to be layered onto services

## When NOT to Use

- The wrapped interface is complex — decorators must replicate every method, leading to maintenance burden
- You need to inspect or remove a specific decorator at runtime — the stack is opaque
- A simple boolean flag or strategy would do the job more clearly

## Structure

- **Component** — the interface shared by both the real object and all decorators
- **ConcreteComponent** — the base object being decorated
- **Decorator** — wraps a Component and delegates to it; subclasses add behaviour before/after delegation
- **ConcreteDecorator** — adds a specific responsibility (logging, caching, etc.)

## TypeScript Example

### ❌ Without the Pattern

```typescript
// Subclass explosion: CachedLoggingEmailNotifier, CachedSmsNotifier...
class LoggingEmailNotifier extends EmailNotifier {
  send(message: string) {
    console.log(`Sending: ${message}`);
    super.send(message);
  }
}
class CachedLoggingEmailNotifier extends LoggingEmailNotifier {
  // now we need caching too — another layer of inheritance
}
```

### ✅ With the Pattern

```typescript
interface Notifier {
  send(message: string): Promise<void>;
}

class EmailNotifier implements Notifier {
  async send(message: string) {
    // core email sending logic
  }
}

// Base decorator — delegates everything to the wrapped notifier
class NotifierDecorator implements Notifier {
  constructor(protected inner: Notifier) {}
  send(message: string): Promise<void> {
    return this.inner.send(message);
  }
}

class LoggingDecorator extends NotifierDecorator {
  async send(message: string): Promise<void> {
    console.log(`[${new Date().toISOString()}] Sending: ${message}`);
    await super.send(message);
    console.log('Send complete');
  }
}

class RetryDecorator extends NotifierDecorator {
  constructor(inner: Notifier, private maxAttempts = 3) { super(inner); }

  async send(message: string): Promise<void> {
    for (let attempt = 1; attempt <= this.maxAttempts; attempt++) {
      try {
        return await super.send(message);
      } catch (err) {
        if (attempt === this.maxAttempts) throw err;
      }
    }
  }
}

class RateLimitDecorator extends NotifierDecorator {
  private lastSent = 0;
  constructor(inner: Notifier, private minIntervalMs = 1000) { super(inner); }

  async send(message: string): Promise<void> {
    const now = Date.now();
    if (now - this.lastSent < this.minIntervalMs) {
      throw new Error('Rate limit exceeded');
    }
    this.lastSent = now;
    return super.send(message);
  }
}

// Compose behaviours freely at runtime — no subclass explosion
const notifier = new LoggingDecorator(
  new RetryDecorator(
    new RateLimitDecorator(
      new EmailNotifier()
    )
  )
);
```

## Python Example

### ❌ Without the Pattern

```python
class LoggingEmailNotifier(EmailNotifier):
    def send(self, message: str) -> None:
        print(f'Sending: {message}')
        super().send(message)

# Need caching too? Another subclass per combination.
class CachedLoggingEmailNotifier(LoggingEmailNotifier): ...
```

### ✅ With the Pattern

```python
from abc import ABC, abstractmethod
from functools import wraps

class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> None: ...

class EmailNotifier(Notifier):
    def send(self, message: str) -> None:
        print(f'Email sent: {message}')

class NotifierDecorator(Notifier):
    def __init__(self, inner: Notifier) -> None:
        self._inner = inner

    def send(self, message: str) -> None:
        self._inner.send(message)

class LoggingDecorator(NotifierDecorator):
    def send(self, message: str) -> None:
        print(f'[LOG] About to send: {message}')
        self._inner.send(message)
        print('[LOG] Send complete')

class RetryDecorator(NotifierDecorator):
    def __init__(self, inner: Notifier, max_attempts: int = 3) -> None:
        super().__init__(inner)
        self._max = max_attempts

    def send(self, message: str) -> None:
        for attempt in range(1, self._max + 1):
            try:
                self._inner.send(message)
                return
            except Exception:
                if attempt == self._max:
                    raise

# Compose at runtime
notifier = LoggingDecorator(RetryDecorator(EmailNotifier(), max_attempts=3))
notifier.send('Hello!')
```

## Real-World Analogy

A barista makes a plain espresso. A customer can add milk (latte), then add vanilla syrup, then add an extra shot — each addition wraps the previous drink. Each "decorator" costs extra and changes the flavour, but the underlying espresso remains unchanged. You can stack any combination of add-ons without the barista needing a separate recipe for every possible combination.

## Related Patterns

- **Adapter** — also wraps an object, but to convert interfaces rather than add behaviour
- **Composite** — Decorator can be viewed as a Composite with a single component; both use recursive composition
- **Strategy** — changes the guts of an object (the algorithm); Decorator changes the skin (adds behaviour around existing logic)
