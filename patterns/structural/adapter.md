# Adapter

**Category:** Structural
**Refactoring Guru:** https://refactoring.guru/design-patterns/adapter

## Intent

Convert the interface of a class into another interface that clients expect, allowing classes with incompatible interfaces to work together.

## When to Use

- You want to use an existing class but its interface does not match what your code expects
- You are wrapping a third-party SDK or library to protect your core code from its API details
- You need several existing subclasses to share a common interface without modifying each one

## When NOT to Use

- You control both sides — just align the interfaces directly
- The mismatch is trivial (a single method rename) — an adapter adds unnecessary indirection
- The adapter would have to translate so much state that it becomes a rewrite

## Structure

- **Target** — the interface your client code expects
- **Adaptee** — the existing class with an incompatible interface (e.g. a third-party SDK)
- **Adapter** — wraps the Adaptee and implements the Target interface
- **Client** — works only with the Target interface; unaware of the Adaptee

## TypeScript Example

### ❌ Without the Pattern

```typescript
// Stripe SDK leaks into business logic
class OrderService {
  async charge(orderId: string, amount: number): Promise<void> {
    const stripe = new Stripe(process.env.STRIPE_KEY!);
    await stripe.paymentIntents.create({   // Stripe-specific API
      amount: amount * 100,                // Stripe needs cents
      currency: 'usd',
      metadata: { orderId },
    });
    // Switching to PayPal means rewriting OrderService
  }
}
```

### ✅ With the Pattern

```typescript
// Target interface — domain language, not payment SDK language
interface PaymentGateway {
  charge(orderId: string, amountInDollars: number): Promise<string>;
}

// Adapter: wraps Stripe, speaks PaymentGateway
class StripeAdapter implements PaymentGateway {
  private stripe = new Stripe(process.env.STRIPE_KEY!);

  async charge(orderId: string, amountInDollars: number): Promise<string> {
    const intent = await this.stripe.paymentIntents.create({
      amount: Math.round(amountInDollars * 100),
      currency: 'usd',
      metadata: { orderId },
    });
    return intent.id;
  }
}

// Adapter: wraps PayPal
class PayPalAdapter implements PaymentGateway {
  async charge(orderId: string, amountInDollars: number): Promise<string> {
    const result = await paypalSdk.orders.capture({ amount: amountInDollars });
    return result.id;
  }
}

// Business logic works only with the Target interface
class OrderService {
  constructor(private gateway: PaymentGateway) {}

  async checkout(orderId: string, amount: number): Promise<void> {
    const transactionId = await this.gateway.charge(orderId, amount);
    console.log(`Charged ${transactionId}`);
  }
}

const service = new OrderService(new StripeAdapter());
```

## Python Example

### ❌ Without the Pattern

```python
import boto3

class DocumentService:
    def store(self, key: str, content: bytes) -> None:
        s3 = boto3.client('s3')
        s3.put_object(Bucket='my-bucket', Key=key, Body=content)
        # Switching storage means rewriting DocumentService
```

### ✅ With the Pattern

```python
from abc import ABC, abstractmethod
import boto3

class StoragePort(ABC):
    @abstractmethod
    def save(self, key: str, content: bytes) -> None: ...
    @abstractmethod
    def load(self, key: str) -> bytes: ...

class S3Adapter(StoragePort):
    def __init__(self, bucket: str) -> None:
        self._client = boto3.client('s3')
        self._bucket = bucket

    def save(self, key: str, content: bytes) -> None:
        self._client.put_object(Bucket=self._bucket, Key=key, Body=content)

    def load(self, key: str) -> bytes:
        return self._client.get_object(Bucket=self._bucket, Key=key)['Body'].read()

class LocalFsAdapter(StoragePort):
    def __init__(self, base_dir: str) -> None:
        self._base = base_dir

    def save(self, key: str, content: bytes) -> None:
        (Path(self._base) / key).write_bytes(content)

    def load(self, key: str) -> bytes:
        return (Path(self._base) / key).read_bytes()

class DocumentService:
    def __init__(self, storage: StoragePort) -> None:
        self._storage = storage

    def store(self, key: str, content: bytes) -> None:
        self._storage.save(key, content)
```

## Real-World Analogy

A travel power adapter lets your laptop plug (expecting UK pins) connect to a European socket (offering EU pins). Neither the laptop nor the wall socket changes — the adapter sits in between translating one physical interface to another. The Adapter pattern does the same in code: it sits between an existing class and the interface your code expects, translating calls without changing either side.

## Related Patterns

- **Facade** — simplifies a complex subsystem behind one interface; Adapter converts one existing interface to another
- **Decorator** — also wraps an object, but to add behaviour rather than convert an interface
- **Proxy** — also wraps an object, but to control access (caching, auth) rather than adapt an interface
