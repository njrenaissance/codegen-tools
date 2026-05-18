# Facade

**Category:** Structural
**Refactoring Guru:** https://refactoring.guru/design-patterns/facade

## Intent

Provide a unified, simplified interface to a set of interfaces in a subsystem, making the subsystem easier to use.

## When to Use

- You want to provide a simple interface to a complex subsystem
- There are many dependencies between clients and implementation classes — a facade decouples them
- You want to layer a subsystem: a facade entry point for high-level use, the full API still accessible for advanced use
- You are integrating multiple third-party services that must work together (e.g. notifications, payments, analytics)

## When NOT to Use

- The subsystem is already simple — adding a facade is pure indirection with no benefit
- Clients genuinely need fine-grained control over the subsystem — the facade would hide necessary options
- The facade becomes a "god object" accumulating unrelated responsibilities

## Structure

- **Facade** — knows which subsystem classes are responsible for a request; delegates client requests to appropriate subsystem objects
- **Subsystem classes** — implement subsystem functionality; handle work assigned by the Facade; have no knowledge of the Facade
- **Client** — communicates with the subsystem only through the Facade

## TypeScript Example

### ❌ Without the Pattern

```typescript
// Client must orchestrate 4 subsystems manually every time
async function registerUser(email: string, password: string) {
  const hasher = new PasswordHasher();
  const hash = await hasher.hash(password);

  const db = new UserRepository();
  const user = await db.create({ email, passwordHash: hash });

  const mailer = new EmailClient();
  await mailer.connect();
  await mailer.send({
    to: email,
    subject: 'Welcome!',
    template: 'welcome',
    data: { userId: user.id },
  });
  await mailer.disconnect();

  const analytics = new AnalyticsClient();
  analytics.track('user_registered', { userId: user.id });

  return user;
}
```

### ✅ With the Pattern

```typescript
// Each subsystem class stays focused
class PasswordHasher {
  async hash(password: string): Promise<string> { /* bcrypt */ return ''; }
}

class UserRepository {
  async create(data: { email: string; passwordHash: string }) { /* db insert */ }
}

class WelcomeMailer {
  async send(email: string, userId: string): Promise<void> { /* smtp */ }
}

class AnalyticsTracker {
  track(event: string, props: Record<string, string>): void { /* segment */ }
}

// Facade — single entry point for "register a user"
class UserRegistrationFacade {
  constructor(
    private hasher: PasswordHasher,
    private users: UserRepository,
    private mailer: WelcomeMailer,
    private analytics: AnalyticsTracker,
  ) {}

  async register(email: string, password: string) {
    const passwordHash = await this.hasher.hash(password);
    const user = await this.users.create({ email, passwordHash });
    await this.mailer.send(email, user.id);
    this.analytics.track('user_registered', { userId: user.id });
    return user;
  }
}

// Client: one call, no knowledge of the subsystems
const registration = new UserRegistrationFacade(
  new PasswordHasher(),
  new UserRepository(),
  new WelcomeMailer(),
  new AnalyticsTracker(),
);
await registration.register('alice@example.com', 's3cret');
```

## Python Example

### ❌ Without the Pattern

```python
async def register_user(email: str, password: str):
    hash_ = await PasswordHasher().hash(password)
    user = await UserRepository().create(email=email, password_hash=hash_)
    mailer = EmailClient()
    await mailer.connect()
    await mailer.send(to=email, template='welcome', data={'user_id': user.id})
    await mailer.disconnect()
    AnalyticsClient().track('user_registered', user_id=user.id)
    return user
```

### ✅ With the Pattern

```python
class UserRegistrationFacade:
    def __init__(
        self,
        hasher: PasswordHasher,
        users: UserRepository,
        mailer: WelcomeMailer,
        analytics: AnalyticsTracker,
    ) -> None:
        self._hasher    = hasher
        self._users     = users
        self._mailer    = mailer
        self._analytics = analytics

    async def register(self, email: str, password: str):
        password_hash = await self._hasher.hash(password)
        user = await self._users.create(email=email, password_hash=password_hash)
        await self._mailer.send(email=email, user_id=user.id)
        self._analytics.track('user_registered', user_id=user.id)
        return user

facade = UserRegistrationFacade(
    PasswordHasher(), UserRepository(), WelcomeMailer(), AnalyticsTracker()
)
user = await facade.register('alice@example.com', 's3cret')
```

## Real-World Analogy

When you call a hotel's concierge to "book a dinner reservation and arrange a taxi," you are using a facade. The concierge coordinates the restaurant booking system, the taxi dispatch system, and possibly the calendar system on your behalf. You speak one simple language ("arrange my evening"); the concierge handles the complexity of the subsystems underneath.

## Related Patterns

- **Adapter** — converts an existing interface to match what a client expects; Facade defines a new simplified interface over multiple subsystems
- **Mediator** — also abstracts collaboration between classes, but Mediator adds two-way communication; Facade is one-directional (client → facade → subsystems)
- **Singleton** — Facades are often implemented as Singletons since only one facade instance is typically needed
