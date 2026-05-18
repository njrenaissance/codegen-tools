# Factory Method

**Category:** Creational
**Refactoring Guru:** https://refactoring.guru/design-patterns/factory-method

## Intent

Define an interface for creating an object, but let subclasses (or implementations) decide which class to instantiate — deferring instantiation to the point where the concrete type is known.

## When to Use

- A class cannot anticipate the class of objects it must create
- A class wants its subclasses or callers to specify the objects it creates
- You want to provide extension hooks so subclasses can override which concrete type is produced
- You need to encapsulate `new ConcreteClass()` calls to avoid hard-coding them in business logic

## When NOT to Use

- The type of object to create is always the same — just use `new`
- You're creating a one-off object with no need for substitution
- The factory hierarchy becomes deeper than the product hierarchy — the indirection costs more than it saves

## Structure

- **Product** — the interface or abstract class for the created object
- **ConcreteProduct** — a specific implementation of Product
- **Creator** — declares the factory method returning a Product; may provide a default implementation
- **ConcreteCreator** — overrides the factory method to return a specific ConcreteProduct

## TypeScript Example

### ❌ Without the Pattern

```typescript
class NotificationService {
  send(channel: string, message: string): void {
    if (channel === 'email') {
      const client = new EmailClient();   // hard-coded dependency
      client.sendMail(message);
    } else if (channel === 'sms') {
      const client = new TwilioClient();  // hard-coded dependency
      client.sendSms(message);
    } else if (channel === 'push') {
      const client = new FirebaseClient();
      client.sendPush(message);
    }
    // Adding Slack requires editing this class
  }
}
```

### ✅ With the Pattern

```typescript
interface Notifier {
  send(message: string): Promise<void>;
}

class EmailNotifier implements Notifier {
  async send(message: string) { /* smtp logic */ }
}
class SmsNotifier implements Notifier {
  async send(message: string) { /* twilio logic */ }
}
class PushNotifier implements Notifier {
  async send(message: string) { /* firebase logic */ }
}

// Factory method: the only place that knows concrete types
function createNotifier(channel: string): Notifier {
  switch (channel) {
    case 'email': return new EmailNotifier();
    case 'sms':   return new SmsNotifier();
    case 'push':  return new PushNotifier();
    default: throw new Error(`Unknown channel: ${channel}`);
  }
}

class NotificationService {
  async send(channel: string, message: string): Promise<void> {
    const notifier = createNotifier(channel); // one seam to extend
    await notifier.send(message);
  }
}
```

## Python Example

### ❌ Without the Pattern

```python
class NotificationService:
    def send(self, channel: str, message: str) -> None:
        if channel == 'email':
            EmailClient().send_mail(message)
        elif channel == 'sms':
            TwilioClient().send_sms(message)
        elif channel == 'push':
            FirebaseClient().send_push(message)
        # Adding Slack requires modifying this class
```

### ✅ With the Pattern

```python
from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> None: ...

class EmailNotifier(Notifier):
    def send(self, message: str) -> None: ...  # smtp logic

class SmsNotifier(Notifier):
    def send(self, message: str) -> None: ...  # twilio logic

class PushNotifier(Notifier):
    def send(self, message: str) -> None: ...  # firebase logic

_registry: dict[str, type[Notifier]] = {
    'email': EmailNotifier,
    'sms':   SmsNotifier,
    'push':  PushNotifier,
}

def create_notifier(channel: str) -> Notifier:
    cls = _registry.get(channel)
    if cls is None:
        raise ValueError(f'Unknown channel: {channel}')
    return cls()

class NotificationService:
    def send(self, channel: str, message: str) -> None:
        create_notifier(channel).send(message)
```

## Real-World Analogy

A logistics company ships by truck or ship depending on the destination. The logistics manager (Creator) says "create a transport" — the land division (ConcreteCreator) returns a truck, the sea division returns a ship. The shipping workflow (business logic) is the same regardless of transport type; the factory method is the single decision point that produces the right vehicle.

## Related Patterns

- **Abstract Factory** — often implemented using Factory Methods; Abstract Factory is for product families, Factory Method is for a single product
- **Template Method** — Factory Methods are frequently called inside Template Methods to let subclasses plug in the concrete type
- **Prototype** — alternative to Factory Method when you want to avoid subclassing; copy a prototype instead of subclassing Creator
