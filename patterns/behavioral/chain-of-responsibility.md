# Chain of Responsibility

**Category:** Behavioral
**Refactoring Guru:** https://refactoring.guru/design-patterns/chain-of-responsibility

## Intent

Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle the request, chaining the receiving objects and passing the request along the chain until an object handles it.

## When to Use

- More than one object may handle a request, and the handler isn't known a priori — the handler should be determined automatically at runtime.
- You want to issue a request to one of several objects without specifying the receiver explicitly.
- The set of objects that can handle a request should be specified dynamically — handlers can be added, removed, or reordered at runtime without changing the sender.
- You are building a pipeline where each stage transforms or validates a request before passing it to the next (e.g., HTTP middleware, event processing pipelines, validation chains).
- Fallback and priority behavior is needed: try the most specific handler first, fall back to general handlers if none match.

## When NOT to Use

- Every request must always be handled — unhandled requests silently falling off the end of the chain is a likely bug. Add a catch-all handler or use a different pattern.
- The handler order is complex, branching, or dependent on the request's runtime state — a strategy map or rules engine is clearer.
- Performance is critical and the chain is long — each handler adds overhead, and the worst-case traversal visits every link.
- You need guaranteed single-handler semantics and the exact handler must be deterministic from the sender's perspective — direct invocation is more appropriate.

## Structure

**Handler** defines the interface for handling requests and optionally holds a reference to the next handler in the chain (successor). It may implement a default behavior of forwarding the request to the successor.

**ConcreteHandler** handles requests it is responsible for. If it can handle the request, it does so; otherwise it forwards the request to its successor.

**Client** initiates the request to a ConcreteHandler object on the chain. The client does not know which handler will ultimately service the request.

Handlers are typically linked in a singly linked list. Each handler decides whether to handle the request, transform it and pass it on, or terminate the chain with an error response.

## TypeScript Example

### ❌ Without the Pattern

```typescript
// API request processing with all validation logic in a single monolithic function.
// Adding a new check requires editing processRequest and risks breaking existing logic.

interface ApiRequest {
  method: string;
  path: string;
  headers: Record<string, string>;
  body: unknown;
  clientIp: string;
  userId?: string;
}

interface ApiResponse {
  status: number;
  body: unknown;
}

// All concerns (auth, rate limiting, validation, routing) collapsed into one function.
// This grows unboundedly and is impossible to reorder or selectively apply.
function processRequest(req: ApiRequest): ApiResponse {
  // 1. Authentication check
  const token = req.headers["authorization"];
  if (!token || !token.startsWith("Bearer ")) {
    return { status: 401, body: { error: "Unauthorized" } };
  }
  // Simulate token validation
  if (token === "Bearer invalid") {
    return { status: 401, body: { error: "Invalid token" } };
  }
  req.userId = "usr_42"; // decoded from token

  // 2. Rate limiting check — embedded inline
  const requestCount = Math.floor(Math.random() * 150); // simulated
  if (requestCount > 100) {
    return { status: 429, body: { error: "Too Many Requests" } };
  }

  // 3. Input validation — also inline
  if (req.method === "POST" && !req.body) {
    return { status: 400, body: { error: "Request body required" } };
  }
  if (req.path.includes("..")) {
    return { status: 400, body: { error: "Invalid path" } };
  }

  // 4. Actual handler logic
  return { status: 200, body: { message: `Handled ${req.method} ${req.path}` } };
}

const req: ApiRequest = {
  method: "POST",
  path: "/api/orders",
  headers: { authorization: "Bearer sk_live_abc" },
  body: { item: "Widget" },
  clientIp: "203.0.113.5",
};

console.log(processRequest(req));
// Adding CORS, logging, or schema validation: edit this function again.
```

### ✅ With the Pattern

```typescript
// Each concern is an independent middleware handler.
// The pipeline is composed at startup and trivially reordered or extended.

interface ApiRequest {
  method: string;
  path: string;
  headers: Record<string, string>;
  body: unknown;
  clientIp: string;
  userId?: string;
  requestId: string;
}

interface ApiResponse {
  status: number;
  body: unknown;
}

// Handler interface
abstract class Middleware {
  private next: Middleware | null = null;

  setNext(handler: Middleware): Middleware {
    this.next = handler;
    return handler; // allows fluent chaining: a.setNext(b).setNext(c)
  }

  protected passToNext(req: ApiRequest): ApiResponse {
    if (this.next) {
      return this.next.handle(req);
    }
    // End of chain with no handler — should not happen if chain is well-formed
    return { status: 500, body: { error: "No handler found" } };
  }

  abstract handle(req: ApiRequest): ApiResponse;
}

// ConcreteHandler: Authentication
class AuthMiddleware extends Middleware {
  private readonly validTokens = new Set(["Bearer sk_live_abc", "Bearer sk_test_xyz"]);

  handle(req: ApiRequest): ApiResponse {
    const token = req.headers["authorization"] ?? "";
    if (!token.startsWith("Bearer ")) {
      return { status: 401, body: { error: "Missing Authorization header" } };
    }
    if (!this.validTokens.has(token)) {
      return { status: 401, body: { error: "Invalid or expired token" } };
    }
    req.userId = "usr_42"; // decoded from token in real impl
    console.log(`[Auth] Request ${req.requestId} authenticated as user ${req.userId}`);
    return this.passToNext(req);
  }
}

// ConcreteHandler: Rate Limiter
class RateLimitMiddleware extends Middleware {
  private readonly windowMs = 60_000;
  private readonly maxRequests = 100;
  private hits = new Map<string, { count: number; windowStart: number }>();

  handle(req: ApiRequest): ApiResponse {
    const key = req.userId ?? req.clientIp;
    const now = Date.now();
    const entry = this.hits.get(key) ?? { count: 0, windowStart: now };

    if (now - entry.windowStart > this.windowMs) {
      entry.count = 0;
      entry.windowStart = now;
    }
    entry.count++;
    this.hits.set(key, entry);

    if (entry.count > this.maxRequests) {
      console.log(`[RateLimit] ${key} exceeded limit (${entry.count}/${this.maxRequests})`);
      return { status: 429, body: { error: "Rate limit exceeded. Retry after 60s." } };
    }

    console.log(`[RateLimit] ${key}: ${entry.count}/${this.maxRequests} requests`);
    return this.passToNext(req);
  }
}

// ConcreteHandler: Input Validation
class ValidationMiddleware extends Middleware {
  handle(req: ApiRequest): ApiResponse {
    if (req.path.includes("..") || req.path.includes("%2e")) {
      return { status: 400, body: { error: "Path traversal detected" } };
    }
    if (["POST", "PUT", "PATCH"].includes(req.method) && req.body === null) {
      return { status: 400, body: { error: "Request body is required" } };
    }
    console.log(`[Validation] Request ${req.requestId} passed validation`);
    return this.passToNext(req);
  }
}

// ConcreteHandler: Request Logger
class LoggingMiddleware extends Middleware {
  handle(req: ApiRequest): ApiResponse {
    const start = Date.now();
    console.log(`[Log] --> ${req.method} ${req.path} (${req.requestId})`);
    const response = this.passToNext(req);
    console.log(`[Log] <-- ${response.status} in ${Date.now() - start}ms`);
    return response;
  }
}

// ConcreteHandler: Actual business logic (terminal handler)
class OrderRouteHandler extends Middleware {
  handle(req: ApiRequest): ApiResponse {
    console.log(`[Handler] Processing order for user ${req.userId}`);
    return {
      status: 201,
      body: { message: "Order created", orderId: `ord_${Date.now()}` },
    };
  }
}

// Compose the pipeline
function buildPipeline(): Middleware {
  const logging = new LoggingMiddleware();
  const auth = new AuthMiddleware();
  const rateLimit = new RateLimitMiddleware();
  const validation = new ValidationMiddleware();
  const handler = new OrderRouteHandler();

  logging.setNext(auth).setNext(rateLimit).setNext(validation).setNext(handler);
  return logging; // entry point
}

const pipeline = buildPipeline();

// Valid request
const req1: ApiRequest = {
  method: "POST",
  path: "/api/orders",
  headers: { authorization: "Bearer sk_live_abc" },
  body: { item: "Widget", quantity: 2 },
  clientIp: "203.0.113.5",
  requestId: "req_001",
};
console.log("Response:", pipeline.handle(req1));

console.log();

// Invalid token — chain stops at AuthMiddleware
const req2: ApiRequest = {
  method: "GET",
  path: "/api/orders",
  headers: { authorization: "Bearer invalid" },
  body: null,
  clientIp: "203.0.113.10",
  requestId: "req_002",
};
console.log("Response:", pipeline.handle(req2));
```

## Python Example

### ❌ Without the Pattern

```python
# Support ticket routing with nested if/else — all routing logic in one function.

from dataclasses import dataclass

@dataclass
class Ticket:
    id: str
    priority: str          # "critical", "high", "medium", "low"
    category: str          # "billing", "technical", "general"
    description: str
    resolved: bool = False

def route_ticket(ticket: Ticket) -> str:
    """All routing logic hardcoded in one place."""
    if ticket.priority == "critical":
        # Escalate immediately — but what if critical + billing? buried below
        return f"[L3 Engineering] Handling critical ticket {ticket.id}"
    elif ticket.priority == "high" and ticket.category == "billing":
        return f"[Billing Team] Handling high-priority billing ticket {ticket.id}"
    elif ticket.category == "technical":
        if ticket.priority in ("high", "medium"):
            return f"[L2 Support] Handling technical ticket {ticket.id}"
        else:
            return f"[L1 Support] Handling low-priority technical ticket {ticket.id}"
    elif ticket.category == "general":
        return f"[L1 Support] Handling general ticket {ticket.id}"
    else:
        return f"[Unhandled] Ticket {ticket.id} fell through routing"

t = Ticket("t1", "high", "billing", "Invoice mismatch")
print(route_ticket(t))
# Adding a new category or SLA escalation rule: edit this function.
```

### ✅ With the Pattern

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

@dataclass
class Ticket:
    id: str
    priority: str       # "critical", "high", "medium", "low"
    category: str       # "billing", "technical", "general"
    description: str
    assigned_to: str = field(default="", init=False)
    resolved: bool = field(default=False, init=False)

    def resolve(self, team: str, note: str = "") -> None:
        self.assigned_to = team
        self.resolved = True
        print(f"  [{team}] Resolved ticket {self.id}: {note or self.description}")

# Handler interface
class SupportHandler(ABC):
    def __init__(self) -> None:
        self._next: SupportHandler | None = None

    def set_next(self, handler: SupportHandler) -> SupportHandler:
        self._next = handler
        return handler

    def pass_to_next(self, ticket: Ticket) -> bool:
        if self._next:
            return self._next.handle(ticket)
        print(f"  [Unhandled] No handler could resolve ticket {ticket.id}")
        return False

    @abstractmethod
    def handle(self, ticket: Ticket) -> bool: ...

# ConcreteHandler: Critical escalation (highest priority — first in chain)
class CriticalEscalationHandler(SupportHandler):
    def handle(self, ticket: Ticket) -> bool:
        if ticket.priority == "critical":
            ticket.resolve("L3 Engineering", "Critical — immediate escalation")
            return True
        return self.pass_to_next(ticket)

# ConcreteHandler: Billing team
class BillingHandler(SupportHandler):
    def handle(self, ticket: Ticket) -> bool:
        if ticket.category == "billing":
            ticket.resolve("Billing Team", f"Billing issue ({ticket.priority} priority)")
            return True
        return self.pass_to_next(ticket)

# ConcreteHandler: L2 technical support
class L2TechnicalHandler(SupportHandler):
    _handled_priorities = {"high", "medium"}

    def handle(self, ticket: Ticket) -> bool:
        if ticket.category == "technical" and ticket.priority in self._handled_priorities:
            ticket.resolve("L2 Support", "Technical issue, escalated from L1")
            return True
        return self.pass_to_next(ticket)

# ConcreteHandler: L1 general support (catch-all)
class L1GeneralHandler(SupportHandler):
    def handle(self, ticket: Ticket) -> bool:
        ticket.resolve("L1 Support", "General or low-priority issue")
        return True

# Build the chain
def build_support_chain() -> SupportHandler:
    critical = CriticalEscalationHandler()
    billing = BillingHandler()
    l2 = L2TechnicalHandler()
    l1 = L1GeneralHandler()

    critical.set_next(billing).set_next(l2).set_next(l1)
    return critical

chain = build_support_chain()

tickets = [
    Ticket("t1", "critical", "technical", "Production database down"),
    Ticket("t2", "high", "billing", "Invoice charged twice"),
    Ticket("t3", "medium", "technical", "API returning 502 intermittently"),
    Ticket("t4", "low", "general", "Question about documentation"),
    Ticket("t5", "high", "general", "Feature request submission"),
]

print("--- Processing Support Tickets ---")
for ticket in tickets:
    print(f"\nTicket {ticket.id} [{ticket.priority}|{ticket.category}]: {ticket.description}")
    chain.handle(ticket)

# Inserting a new handler (e.g., VIP customers) requires only adding a new class
# and inserting it at the correct position in build_support_chain().
class VipCustomerHandler(SupportHandler):
    VIP_CUSTOMERS = {"acme-corp", "globex"}

    def __init__(self, vip_account_id: str) -> None:
        super().__init__()
        self._account = vip_account_id

    def handle(self, ticket: Ticket) -> bool:
        if self._account in self.VIP_CUSTOMERS:
            ticket.resolve("VIP Concierge", "VIP account — priority handling")
            return True
        return self.pass_to_next(ticket)
```

## Real-World Analogy

When you call a company's customer support line, your call is first handled by an automated IVR system — if it can resolve your issue (e.g., check a balance), it does. If not, it transfers you to a first-level agent. If that agent can't help, they escalate to a specialist. If the specialist still can't resolve it, a senior manager gets involved. Each level in this support hierarchy is a handler in a chain: it either resolves the request or passes it up. The caller doesn't choose who handles the call — the chain decides. This is exactly Chain of Responsibility: a request travels along a chain of handlers until one takes ownership, giving each level the chance to handle before escalating.

## Related Patterns

- **Composite** — Chain of Responsibility is often applied in conjunction with Composite. A handler's successor may itself be a Composite node (a group of handlers), enabling tree-structured pipelines.
- **Command** — Chain of Responsibility and Command both decouple senders from receivers. Command binds a request to a specific known receiver; Chain lets the receiver be determined by the chain at runtime.
- **Decorator** — Decorator and Chain of Responsibility both use linked wrapping, but Decorator always calls its wrapped component (the chain never terminates); a Chain handler may stop the request at any point. Use Decorator for enrichment, Chain for conditional dispatch.
- **Strategy** — each handler in a chain is essentially a Strategy for how to process a particular type of request. The difference is that Strategy selects one algorithm; Chain tries handlers in sequence until one matches.
