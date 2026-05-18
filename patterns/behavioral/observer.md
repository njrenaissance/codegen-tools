# Observer

**Category:** Behavioral
**Refactoring Guru:** https://refactoring.guru/design-patterns/observer

## Intent

Define a one-to-many dependency between objects so that when one object (the subject) changes state, all its dependents (observers) are notified and updated automatically.

## When to Use

- A change to one object requires changing others, and you don't know how many objects need to change.
- An object should be able to notify other objects without making assumptions about who those objects are — you want loose coupling between the subject and its observers.
- You are building a distributed event-handling system where multiple subsystems must react to the same domain event (e.g., "order placed", "user registered").
- An abstraction has two dependent aspects, and encapsulating these aspects in separate objects lets you vary and reuse them independently.
- You need to support broadcast communication, where a notification sent by one object can be received by an unlimited number of observers.

## When NOT to Use

- The update chain is long or cascading — Observer can trigger unexpected chains of updates that are difficult to trace and debug.
- Observers need to be notified in a specific order — Observer does not guarantee ordering; if order matters, consider a simpler event queue or mediator.
- The subject and observer are tightly coupled by necessity (same module, same team, simple relationship) — the indirection adds complexity without benefit.
- Memory leaks are a concern in long-lived processes — forgotten observer references keep subjects alive; careful lifecycle management is required.
- Real-time performance is critical — notification overhead across many observers may introduce unacceptable latency.

## Structure

**Subject** (also called Publisher or Observable) knows its observers and provides an interface for attaching and detaching them. It notifies observers when its state changes.

**Observer** (also called Subscriber or Listener) defines an update interface that subjects use to notify it of a change.

**ConcreteSubject** stores state of interest and sends a notification to its observers when its state changes.

**ConcreteObserver** maintains a reference to the ConcreteSubject, stores state that is consistent with the subject's, and implements the Observer update interface to keep its state consistent.

The subject notifies observers by calling their `update` (or equivalent) method, optionally passing itself or the changed state as an argument (push vs. pull model).

## TypeScript Example

### ❌ Without the Pattern

```typescript
// Order processing with direct, hardcoded cross-module calls.
// OrderService must import and call every downstream system explicitly.
// Adding a new reaction (e.g., loyalty points) means editing OrderService.

interface Order {
  id: string;
  userId: string;
  total: number;
  items: string[];
}

// Downstream services — imagine these are real service classes
class EmailService {
  sendOrderConfirmation(order: Order): void {
    console.log(`[Email] Confirmation sent to user ${order.userId} for order ${order.id}`);
  }
}

class InventoryService {
  reserveItems(order: Order): void {
    order.items.forEach(item =>
      console.log(`[Inventory] Reserved "${item}" for order ${order.id}`)
    );
  }
}

class AnalyticsService {
  trackPurchase(order: Order): void {
    console.log(`[Analytics] Tracked $${order.total} purchase for user ${order.userId}`);
  }
}

// OrderService is tightly coupled to every downstream system.
// Each new reaction requires importing and wiring a new service here.
class OrderService {
  private emailService = new EmailService();
  private inventoryService = new InventoryService();
  private analyticsService = new AnalyticsService();

  placeOrder(order: Order): void {
    console.log(`[Order] Order ${order.id} placed`);

    // Direct calls — every consumer hardcoded here
    this.emailService.sendOrderConfirmation(order);
    this.inventoryService.reserveItems(order);
    this.analyticsService.trackPurchase(order);
    // To add loyalty points: add another field + another direct call here
  }
}

const svc = new OrderService();
svc.placeOrder({ id: "ord_001", userId: "usr_42", total: 129.99, items: ["Widget", "Gadget"] });
```

### ✅ With the Pattern

```typescript
// OrderService publishes domain events. Observers subscribe independently.
// New reactions are added by registering a new observer — OrderService never changes.

interface Order {
  id: string;
  userId: string;
  total: number;
  items: string[];
}

// Domain event payload
interface OrderPlacedEvent {
  readonly type: "ORDER_PLACED";
  readonly order: Order;
  readonly timestamp: Date;
}

type DomainEvent = OrderPlacedEvent; // extend union for more events

// Observer interface
interface EventObserver<T extends DomainEvent = DomainEvent> {
  readonly eventType: T["type"];
  handle(event: T): void;
}

// Subject (EventBus) — generic, reusable across the application
class EventBus {
  private observers = new Map<string, EventObserver[]>();

  subscribe(observer: EventObserver): void {
    const list = this.observers.get(observer.eventType) ?? [];
    list.push(observer);
    this.observers.set(observer.eventType, list);
    console.log(`[EventBus] Subscribed ${observer.constructor.name} to "${observer.eventType}"`);
  }

  unsubscribe(observer: EventObserver): void {
    const list = this.observers.get(observer.eventType) ?? [];
    this.observers.set(
      observer.eventType,
      list.filter(o => o !== observer)
    );
  }

  publish(event: DomainEvent): void {
    const observers = this.observers.get(event.type) ?? [];
    if (observers.length === 0) {
      console.warn(`[EventBus] No observers for event "${event.type}"`);
      return;
    }
    observers.forEach(o => o.handle(event));
  }
}

// ConcreteObservers — each lives in its own module, independently maintained

class OrderConfirmationEmailObserver implements EventObserver<OrderPlacedEvent> {
  readonly eventType = "ORDER_PLACED" as const;

  handle(event: OrderPlacedEvent): void {
    console.log(
      `[Email] Sending confirmation to user ${event.order.userId} ` +
      `for order ${event.order.id} ($${event.order.total})`
    );
  }
}

class InventoryReservationObserver implements EventObserver<OrderPlacedEvent> {
  readonly eventType = "ORDER_PLACED" as const;

  handle(event: OrderPlacedEvent): void {
    event.order.items.forEach(item =>
      console.log(`[Inventory] Reserving "${item}" for order ${event.order.id}`)
    );
  }
}

class PurchaseAnalyticsObserver implements EventObserver<OrderPlacedEvent> {
  readonly eventType = "ORDER_PLACED" as const;

  handle(event: OrderPlacedEvent): void {
    console.log(
      `[Analytics] Purchase tracked — user ${event.order.userId}, ` +
      `amount $${event.order.total}, at ${event.timestamp.toISOString()}`
    );
  }
}

// OrderService now only knows about the EventBus — zero direct dependencies on consumers
class OrderService {
  constructor(private readonly eventBus: EventBus) {}

  placeOrder(order: Order): void {
    console.log(`\n[Order] Placing order ${order.id}...`);
    // Business logic: persist, validate, charge payment, etc.
    this.eventBus.publish({
      type: "ORDER_PLACED",
      order,
      timestamp: new Date(),
    });
  }
}

// Bootstrap — wire observers at composition root
const bus = new EventBus();
bus.subscribe(new OrderConfirmationEmailObserver());
bus.subscribe(new InventoryReservationObserver());
bus.subscribe(new PurchaseAnalyticsObserver());

const orderService = new OrderService(bus);
orderService.placeOrder({ id: "ord_001", userId: "usr_42", total: 129.99, items: ["Widget", "Gadget"] });

// Adding loyalty points: just register a new observer — OrderService untouched.
class LoyaltyPointsObserver implements EventObserver<OrderPlacedEvent> {
  readonly eventType = "ORDER_PLACED" as const;
  handle(event: OrderPlacedEvent): void {
    const points = Math.floor(event.order.total * 10);
    console.log(`[Loyalty] Awarded ${points} points to user ${event.order.userId}`);
  }
}

bus.subscribe(new LoyaltyPointsObserver());
orderService.placeOrder({ id: "ord_002", userId: "usr_42", total: 49.99, items: ["Doohickey"] });
```

## Python Example

### ❌ Without the Pattern

```python
# UserService directly calls every downstream system on registration.
# Adding a new welcome step requires editing UserService.

from dataclasses import dataclass

@dataclass
class User:
    id: str
    email: str
    name: str
    plan: str = "free"

class EmailService:
    def send_welcome(self, user: User) -> None:
        print(f"[Email] Welcome email sent to {user.email}")

class SlackService:
    def notify_team(self, user: User) -> None:
        print(f"[Slack] New signup: {user.name} ({user.plan} plan)")

class CrmService:
    def create_contact(self, user: User) -> None:
        print(f"[CRM] Contact created for {user.email}")

class UserService:
    def __init__(self) -> None:
        self._email = EmailService()
        self._slack = SlackService()
        self._crm = CrmService()

    def register(self, user: User) -> None:
        print(f"[User] Registered {user.email}")
        # Adding a trial provisioner? Edit this method.
        self._email.send_welcome(user)
        self._slack.notify_team(user)
        self._crm.create_contact(user)

svc = UserService()
svc.register(User(id="u1", email="alice@example.com", name="Alice", plan="pro"))
```

### ✅ With the Pattern

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Generic, TypeVar

# Domain event
@dataclass(frozen=True)
class UserRegisteredEvent:
    type: str = field(default="USER_REGISTERED", init=False)
    user_id: str = ""
    email: str = ""
    name: str = ""
    plan: str = "free"
    registered_at: datetime = field(default_factory=datetime.utcnow)

DomainEvent = UserRegisteredEvent  # extend as Union for more events

# Observer interface
class EventObserver(ABC):
    @property
    @abstractmethod
    def event_type(self) -> str: ...

    @abstractmethod
    def handle(self, event: DomainEvent) -> None: ...

# Subject — simple synchronous event bus
class EventBus:
    def __init__(self) -> None:
        self._observers: dict[str, list[EventObserver]] = {}

    def subscribe(self, observer: EventObserver) -> None:
        bucket = self._observers.setdefault(observer.event_type, [])
        bucket.append(observer)
        print(f"[EventBus] {type(observer).__name__} subscribed to '{observer.event_type}'")

    def unsubscribe(self, observer: EventObserver) -> None:
        bucket = self._observers.get(observer.event_type, [])
        self._observers[observer.event_type] = [o for o in bucket if o is not observer]

    def publish(self, event: DomainEvent) -> None:
        observers = self._observers.get(event.type, [])
        for observer in observers:
            observer.handle(event)

# ConcreteObservers

class WelcomeEmailObserver(EventObserver):
    event_type = "USER_REGISTERED"

    def handle(self, event: UserRegisteredEvent) -> None:
        print(f"[Email] Welcome email sent to {event.email}")

class SlackNotificationObserver(EventObserver):
    event_type = "USER_REGISTERED"

    def handle(self, event: UserRegisteredEvent) -> None:
        print(f"[Slack] New signup: {event.name} ({event.plan} plan)")

class CrmContactObserver(EventObserver):
    event_type = "USER_REGISTERED"

    def handle(self, event: UserRegisteredEvent) -> None:
        print(f"[CRM] Contact created for {event.email} at {event.registered_at}")

# UserService — publishes events, knows nothing about downstream reactions
class UserService:
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

    def register(self, user_id: str, email: str, name: str, plan: str = "free") -> None:
        print(f"\n[User] Registering {email}...")
        # Business logic: validate, hash password, persist, etc.
        self._bus.publish(UserRegisteredEvent(
            user_id=user_id,
            email=email,
            name=name,
            plan=plan,
        ))

# Bootstrap
bus = EventBus()
bus.subscribe(WelcomeEmailObserver())
bus.subscribe(SlackNotificationObserver())
bus.subscribe(CrmContactObserver())

svc = UserService(bus)
svc.register("u1", "alice@example.com", "Alice", plan="pro")

# Adding trial provisioning: zero changes to UserService
class TrialProvisionObserver(EventObserver):
    event_type = "USER_REGISTERED"

    def handle(self, event: UserRegisteredEvent) -> None:
        if event.plan == "free":
            print(f"[Trial] 14-day trial provisioned for {event.email}")

bus.subscribe(TrialProvisionObserver())
svc.register("u2", "bob@example.com", "Bob", plan="free")
```

## Real-World Analogy

A newspaper subscription model captures the Observer pattern perfectly. The newspaper publisher (subject) maintains a subscriber list. When a new edition is printed (state change), the publisher delivers a copy to every subscriber (observer) — subscribers don't call the publisher to ask if there's news, the publisher pushes it to them. Subscribers can join or leave the list at any time without the publisher changing anything about how it prints or distributes papers. The publisher doesn't know what readers do with the paper (read it, recycle it, pass it on) — it only knows to deliver it. In software, a domain object like an `Order` plays the publisher role, and email services, inventory systems, and analytics dashboards are the subscribers who each react in their own way.

## Related Patterns

- **Mediator** — both decouple objects from each other, but Mediator centralizes communication through a single mediator object (objects don't reference each other at all), while Observer lets subjects broadcast to any number of observers without knowing who they are. Use Mediator when the interaction logic itself is complex; use Observer for simple broadcast notifications.
- **Event Sourcing** — Observer pairs well with event sourcing; the event log can replay to rebuild observer state.
- **Command** — Observers often execute commands in response to notifications, keeping a clean separation between the trigger and the action performed.
- **Singleton** — the event bus or subject is frequently implemented as a Singleton, though dependency injection is preferred for testability.
