# Strategy

**Category:** Behavioral
**Refactoring Guru:** https://refactoring.guru/design-patterns/strategy

## Intent

Define a family of algorithms, encapsulate each one, and make them interchangeable so that the algorithm can vary independently from the clients that use it.

## When to Use

- Many related classes differ only in their behavior — strategies let you configure a class with one of many behaviors.
- You need different variants of an algorithm (e.g., different sort orders, payment methods, discount rules) and want to switch between them at runtime.
- An algorithm uses data that clients shouldn't know about — use Strategy to avoid exposing complex, algorithm-specific data structures.
- A class defines many conditional branches that select different behaviors; move each branch into its own strategy class.
- You want to eliminate large `if/else` or `switch` blocks that choose between algorithmic variations.

## When NOT to Use

- You only have two or three strategies that will never change — the extra abstraction adds complexity without benefit.
- The algorithms are trivially simple (one-liners); the interface overhead outweighs the flexibility.
- Clients must be aware of all available strategies to select one — if the selection logic is already complex, Strategy doesn't simplify it.
- The strategy objects need to share a lot of private state with the context — tight coupling defeats the purpose of the pattern.

## Structure

**Context** maintains a reference to a `Strategy` object and delegates the algorithm call to it. It may define an interface for Strategy to access its data.

**Strategy** declares a common interface for all supported algorithms. Context uses this interface to call the algorithm defined by a ConcreteStrategy.

**ConcreteStrategy** implements the algorithm using the Strategy interface. Each represents a distinct variation.

Clients create the ConcreteStrategy and pass it to the Context; thereafter the Context and the Strategy interact without the client being involved.

## TypeScript Example

### ❌ Without the Pattern

```typescript
// Payment processing with hardcoded conditionals.
// Every new payment provider requires modifying the checkout function.

type PaymentMethod = "stripe" | "paypal" | "bank_transfer";

interface Order {
  id: string;
  amount: number;
  currency: string;
}

function processPayment(order: Order, method: PaymentMethod): string {
  if (method === "stripe") {
    // Stripe-specific logic embedded directly
    const fee = order.amount * 0.029 + 0.30;
    console.log(`[Stripe] Charging ${order.amount + fee} with API key sk_live_...`);
    return `stripe_charge_${order.id}`;
  } else if (method === "paypal") {
    // PayPal-specific logic embedded directly
    const fee = order.amount * 0.034 + 0.30;
    console.log(`[PayPal] Redirecting to PayPal for ${order.amount + fee}`);
    return `paypal_order_${order.id}`;
  } else if (method === "bank_transfer") {
    // Bank transfer-specific logic embedded directly
    console.log(`[Bank] Generating IBAN transfer reference for ${order.amount}`);
    return `bank_ref_${order.id}`;
  }
  throw new Error(`Unknown payment method: ${method}`);
}

// Usage — callers must know all method strings
const order: Order = { id: "ord_001", amount: 99.99, currency: "USD" };
const ref = processPayment(order, "stripe");
console.log("Payment reference:", ref);

// Adding "crypto" payment requires editing processPayment — violates Open/Closed.
```

### ✅ With the Pattern

```typescript
// Each payment provider is encapsulated behind a common interface.
// New providers can be added without touching existing code.

interface Order {
  id: string;
  amount: number;
  currency: string;
}

interface PaymentResult {
  reference: string;
  provider: string;
  totalCharged: number;
}

// Strategy interface
interface PaymentStrategy {
  readonly name: string;
  process(order: Order): PaymentResult;
}

// ConcreteStrategy: Stripe
class StripePayment implements PaymentStrategy {
  readonly name = "Stripe";

  constructor(private readonly apiKey: string) {}

  process(order: Order): PaymentResult {
    const fee = order.amount * 0.029 + 0.30;
    const total = order.amount + fee;
    console.log(`[Stripe] Charging ${total.toFixed(2)} ${order.currency}`);
    return {
      reference: `stripe_ch_${order.id}_${Date.now()}`,
      provider: this.name,
      totalCharged: total,
    };
  }
}

// ConcreteStrategy: PayPal
class PayPalPayment implements PaymentStrategy {
  readonly name = "PayPal";

  constructor(private readonly clientId: string) {}

  process(order: Order): PaymentResult {
    const fee = order.amount * 0.034 + 0.30;
    const total = order.amount + fee;
    console.log(`[PayPal] Redirecting for ${total.toFixed(2)} ${order.currency}`);
    return {
      reference: `paypal_ord_${order.id}_${Date.now()}`,
      provider: this.name,
      totalCharged: total,
    };
  }
}

// ConcreteStrategy: Bank Transfer (no fee)
class BankTransferPayment implements PaymentStrategy {
  readonly name = "BankTransfer";

  process(order: Order): PaymentResult {
    console.log(`[Bank] Generating transfer for ${order.amount} ${order.currency}`);
    return {
      reference: `bank_ref_${order.id}`,
      provider: this.name,
      totalCharged: order.amount,
    };
  }
}

// Context
class CheckoutService {
  private strategy: PaymentStrategy;

  constructor(strategy: PaymentStrategy) {
    this.strategy = strategy;
  }

  // Strategy can be swapped at runtime (e.g., fallback on failure)
  setPaymentStrategy(strategy: PaymentStrategy): void {
    this.strategy = strategy;
  }

  checkout(order: Order): PaymentResult {
    console.log(`Processing order ${order.id} via ${this.strategy.name}`);
    const result = this.strategy.process(order);
    console.log(`Payment complete. Reference: ${result.reference}`);
    return result;
  }
}

// Usage
const order: Order = { id: "ord_001", amount: 99.99, currency: "USD" };

const checkout = new CheckoutService(new StripePayment("sk_live_abc123"));
checkout.checkout(order);

// Swap to PayPal at runtime — no changes to CheckoutService
checkout.setPaymentStrategy(new PayPalPayment("client_xyz789"));
checkout.checkout({ id: "ord_002", amount: 49.99, currency: "USD" });

// Adding crypto payments requires only a new class — CheckoutService is untouched.
class CryptoPayment implements PaymentStrategy {
  readonly name = "Crypto";
  process(order: Order): PaymentResult {
    console.log(`[Crypto] Generating wallet address for ${order.amount} USD`);
    return {
      reference: `btc_tx_${order.id}`,
      provider: this.name,
      totalCharged: order.amount,
    };
  }
}

checkout.setPaymentStrategy(new CryptoPayment());
checkout.checkout({ id: "ord_003", amount: 199.00, currency: "USD" });
```

## Python Example

### ❌ Without the Pattern

```python
# Discount calculation with if/else chains.
# Each new discount type requires modifying the core function.

from dataclasses import dataclass

@dataclass
class CartItem:
    name: str
    price: float
    quantity: int

def calculate_discount(items: list[CartItem], discount_type: str) -> float:
    subtotal = sum(i.price * i.quantity for i in items)

    if discount_type == "none":
        return 0.0
    elif discount_type == "percentage_10":
        return subtotal * 0.10
    elif discount_type == "percentage_20":
        return subtotal * 0.20
    elif discount_type == "flat_15":
        return min(15.0, subtotal)
    elif discount_type == "buy_two_get_one":
        # Complex logic entangled with other types
        total_items = sum(i.quantity for i in items)
        free_items = total_items // 3
        cheapest = sorted(i.price for i in items)
        return sum(cheapest[:free_items])
    else:
        raise ValueError(f"Unknown discount type: {discount_type}")

# Adding "loyalty_points" discount means editing this function
items = [CartItem("Widget", 29.99, 2), CartItem("Gadget", 49.99, 1)]
print(calculate_discount(items, "percentage_10"))
```

### ✅ With the Pattern

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class CartItem:
    name: str
    price: float
    quantity: int

# Strategy interface
class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, items: list[CartItem]) -> float:
        """Return the discount amount (not the final price)."""
        ...

    @property
    @abstractmethod
    def label(self) -> str: ...

# ConcreteStrategies
class NoDiscount(DiscountStrategy):
    label = "No Discount"

    def calculate(self, items: list[CartItem]) -> float:
        return 0.0

class PercentageDiscount(DiscountStrategy):
    def __init__(self, rate: float) -> None:
        self._rate = rate

    @property
    def label(self) -> str:
        return f"{int(self._rate * 100)}% Off"

    def calculate(self, items: list[CartItem]) -> float:
        subtotal = sum(i.price * i.quantity for i in items)
        return round(subtotal * self._rate, 2)

class FlatDiscount(DiscountStrategy):
    def __init__(self, amount: float) -> None:
        self._amount = amount

    @property
    def label(self) -> str:
        return f"${self._amount:.2f} Off"

    def calculate(self, items: list[CartItem]) -> float:
        subtotal = sum(i.price * i.quantity for i in items)
        return min(self._amount, subtotal)

class BuyTwoGetOneDiscount(DiscountStrategy):
    label = "Buy 2 Get 1 Free"

    def calculate(self, items: list[CartItem]) -> float:
        all_prices = sorted(
            (i.price for i in items for _ in range(i.quantity))
        )
        free_count = len(all_prices) // 3
        return round(sum(all_prices[:free_count]), 2)

# Context
class ShoppingCart:
    def __init__(self, strategy: DiscountStrategy = NoDiscount()) -> None:
        self._items: list[CartItem] = []
        self._strategy = strategy

    def add_item(self, item: CartItem) -> None:
        self._items.append(item)

    def set_discount(self, strategy: DiscountStrategy) -> None:
        self._strategy = strategy

    def total(self) -> float:
        subtotal = sum(i.price * i.quantity for i in self._items)
        discount = self._strategy.calculate(self._items)
        return round(subtotal - discount, 2)

    def summary(self) -> None:
        subtotal = sum(i.price * i.quantity for i in self._items)
        discount = self._strategy.calculate(self._items)
        print(f"Subtotal:  ${subtotal:.2f}")
        print(f"Discount ({self._strategy.label}): -${discount:.2f}")
        print(f"Total:     ${self.total():.2f}")

# Usage
cart = ShoppingCart()
cart.add_item(CartItem("Widget", 29.99, 2))
cart.add_item(CartItem("Gadget", 49.99, 1))

cart.set_discount(PercentageDiscount(0.10))
cart.summary()

print()
cart.set_discount(BuyTwoGetOneDiscount())
cart.summary()

# Adding loyalty discount: just a new class, nothing else changes.
class LoyaltyDiscount(DiscountStrategy):
    label = "Loyalty 15% Off"

    def calculate(self, items: list[CartItem]) -> float:
        subtotal = sum(i.price * i.quantity for i in items)
        return round(subtotal * 0.15, 2)

cart.set_discount(LoyaltyDiscount())
cart.summary()
```

## Real-World Analogy

Think of a GPS navigation app that can calculate routes using different strategies: fastest route, shortest distance, or avoid highways. The destination and start point (the context) remain the same — only the routing algorithm (the strategy) changes. You can switch from "fastest" to "avoid tolls" mid-trip without redesigning the app. Each routing engine is interchangeable because they all answer the same question: given start and end, what is the path? The Strategy pattern captures exactly this: the context doesn't need to know how the algorithm works, only that it conforms to the agreed-upon interface.

## Related Patterns

- **Flyweight** — Strategy objects often make good flyweights when they carry no state; a single instance can be shared across many contexts.
- **State** — Strategy and State have similar structures, but different intent. State allows an object to alter its behavior when its internal state changes (transitions are managed by the object itself); Strategy provides a family of interchangeable algorithms where the client chooses which to use.
- **Template Method** — both define a skeleton of behavior, but Template Method uses inheritance (subclasses override steps) while Strategy uses composition (the algorithm is entirely delegated to a separate object). Prefer Strategy when you want to switch algorithms at runtime; prefer Template Method when the invariant skeleton is the priority.
- **Decorator** — Decorator changes the skin of an object; Strategy changes its guts. Use Decorator to add responsibilities, Strategy to swap core algorithms.
