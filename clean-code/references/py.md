# Clean Code Standards — Python Examples

Python ❌ BAD / ✅ GOOD examples for the Clean Code rules. Each section heading
matches a rule name in [`CLEAN-CODE.md`](../CLEAN-CODE.md), which links here
by that name.

---

## Boy Scout Rule — leave code cleaner than you found it

```python
# ❌ BAD — left as-is when you touched this function
def proc(x, y):
    return x*y

# ✅ GOOD — cleaned up while you were here
def calculate_total_price(unit_price: float, quantity: int) -> float:
    return unit_price * quantity
```

---

## Use descriptive, unambiguous names

```python
# ❌ BAD — single-letter names say nothing
def proc(d, f):
    return d * f

# ✅ GOOD
def calculate_total_cost(unit_price: Decimal, quantity: int) -> Decimal:
    return unit_price * quantity
```

---

## Use pronounceable names

```python
# ❌ BAD
genymdhms = datetime.now()
modymdhms = datetime.now()

# ✅ GOOD
generation_timestamp  = datetime.now()
modification_timestamp = datetime.now()
```

---

## Use searchable names — avoid magic numbers

```python
# ❌ BAD — what does 7 mean?
if days > 7:
    send_reminder()

# ✅ GOOD
REMINDER_THRESHOLD_DAYS = 7
if days > REMINDER_THRESHOLD_DAYS:
    send_reminder()
```

---

## Avoid encodings and type noise

```python
# ❌ BAD
str_user_name = "Jonathan"
i_user_age    = 51
lst_orders    = []

# ✅ GOOD
user_name = "Jonathan"
user_age  = 51
orders: list[Order] = []
```

---

## Be consistent — same pattern everywhere

```python
# ❌ BAD — three styles for the same concept
def fetch_user_by_id(id): ...
def getUserEmail(user_id): ...
def get_profile(uid): ...

# ✅ GOOD
def get_user_by_id(user_id: int) -> User: ...
def get_user_by_email(email: str) -> User: ...
def get_user_profile(user_id: int) -> UserProfile: ...
```

---

## Functions should be small and do ONE thing

```python
# ❌ BAD — validates, creates, and notifies in one function
def register_user(data: dict) -> None:
    if not data.get("email"):
        raise ValueError("Email required")
    user = User(**data)
    db.add(user)
    send_welcome_email(user.email)

# ✅ GOOD — each function has one job
def validate_registration_data(data: dict) -> None:
    if not data.get("email"):
        raise ValueError("Email required")

def create_user(data: dict) -> User:
    user = User(**data)
    db.add(user)
    return user

def register_user(data: dict) -> None:
    validate_registration_data(data)
    user = create_user(data)
    send_welcome_email(user.email)
```

---

## One level of abstraction per function

```python
# ❌ BAD — high-level validate_user sits beside raw SQL cursor detail
def process_payment(payment: dict) -> Receipt:
    validate_user(payment["user_id"])
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO payments (amount, user_id) VALUES (%s, %s)",
        (payment["amount"], payment["user_id"]),
    )
    conn.commit()
    return Receipt(id=cursor.lastrowid)

# ✅ GOOD — all statements at business-intent level
def process_payment(payment: dict) -> Receipt:
    validate_user(payment["user_id"])
    return persist_payment(payment)

def persist_payment(payment: dict) -> Receipt:
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO payments (amount, user_id) VALUES (%s, %s)",
        (payment["amount"], payment["user_id"]),
    )
    conn.commit()
    return Receipt(id=cursor.lastrowid)
```

---

## Stepdown Rule — file reads top-to-bottom at decreasing abstraction levels

```python
# ❌ BAD — orchestration and implementation mixed at the same level
def create_order(data: dict) -> Order:
    if not data.get("customer_id") or not data.get("items"):
        raise ValueError("customer_id and items required")
    rows = db.execute("SELECT COUNT(*) FROM orders WHERE customer_id = ?", data["customer_id"])
    if rows[0][0] >= 50:
        raise ValueError("Order limit reached")
    order = Order(customer_id=data["customer_id"])
    for item in data["items"]:
        order.lines.append(OrderLine(sku=item["sku"], qty=item["qty"]))
    db.save(order)
    email_client.send(order.customer.email, "Your order was placed")
    return order

# ✅ GOOD — top-level names each step; sub-functions immediately follow
def create_order(data: dict) -> Order:
    validated = validate_order_input(data)
    enforce_order_limit(validated.customer_id)
    order = build_order_with_lines(validated)
    notify_customer(order)
    return order

def validate_order_input(data: dict) -> OrderInput: ...
def enforce_order_limit(customer_id: int) -> None: ...
def build_order_with_lines(input: OrderInput) -> Order: ...
def notify_customer(order: Order) -> None: ...
```

---

## Prefer fewer arguments — use parameter objects when needed

```python
# ❌ BAD — six positional arguments are easy to transpose
def create_report(title, author, start_date, end_date, include_charts, format):
    ...

# ✅ GOOD
@dataclass
class ReportConfig:
    title: str
    author: str
    start_date: date
    end_date: date
    include_charts: bool = True
    format: str = "pdf"

def create_report(config: ReportConfig) -> Report:
    ...
```

---

## Don't use flag arguments — split into separate functions

```python
# ❌ BAD — caller must know what True/False means
def render_page(include_header: bool) -> str:
    if include_header:
        return render_with_header()
    return render_without_header()

# ✅ GOOD
def render_page_with_header() -> str: ...
def render_page() -> str: ...
```

---

## No side effects — a function should do what its name says and nothing else

```python
# ❌ BAD — name says "read", but function also writes
def get_user(user_id: int) -> User:
    user = db.query(user_id)
    user.last_accessed = datetime.now()   # hidden side effect
    db.save(user)
    return user

# ✅ GOOD — separate read from write
def get_user(user_id: int) -> User:
    return db.query(user_id)

def record_access(user: User) -> None:
    user.last_accessed = datetime.now()
    db.save(user)
```

---

## Explain yourself in code, not in comments

```python
# ❌ BAD — comment re-states what well-named code would say
# Check if the user is old enough to purchase alcohol
if user.age >= 21:
    allow_purchase()

# ✅ GOOD
MINIMUM_ALCOHOL_PURCHASE_AGE = 21

def is_eligible_to_purchase_alcohol(user: User) -> bool:
    return user.age >= MINIMUM_ALCOHOL_PURCHASE_AGE

if is_eligible_to_purchase_alcohol(user):
    allow_purchase()
```

---

## Use comments to explain INTENT, WARNINGS, and non-obvious decisions

```python
# ❌ BAD — restates the obvious
# Add item to list
items.append(item)

# ✅ GOOD — explains a non-obvious performance trade-off
# Sorting on every insert (O(n log n)) rather than at read time because
# reads outnumber writes 100:1 in the order processing pipeline.
items.append(item)
items.sort(key=lambda x: x.priority)

# ✅ GOOD — safety warning
# WARNING: Permanently deletes the user and all associated data.
# No soft-delete. Caller must present a confirmation dialog first.
def hard_delete_user(user_id: int) -> None:
    db.execute("DELETE FROM users WHERE id = ?", user_id)
```

---

## Never comment out dead code — delete it

```python
# ❌ BAD
def process_payment(amount: Decimal) -> Receipt:
    # old_charge(amount)
    # legacy_receipt = old_receipt_service.create()
    return new_payment_service.charge(amount)

# ✅ GOOD — git history preserves the old code
def process_payment(amount: Decimal) -> Receipt:
    return new_payment_service.charge(amount)
```

---

## Declare variables close to their usage

```python
# ❌ BAD — tax_rate declared far from use
def process_order(order: Order) -> None:
    tax_rate = Decimal("0.08")
    # ... 30 lines of unrelated logic ...
    subtotal = sum(item.price for item in order.items)
    total = subtotal * (1 + tax_rate)

# ✅ GOOD
def process_order(order: Order) -> None:
    # ... other logic ...
    TAX_RATE = Decimal("0.08")
    subtotal = sum(item.price for item in order.items)
    total    = subtotal * (1 + TAX_RATE)
```

---

## Place caller above callee — high-level first

```python
# ✅ GOOD — public API at top, private helpers below
class ReportService:
    def generate_report(self, config: ReportConfig) -> Report:
        data    = self._fetch_data(config)
        summary = self._summarize(data)
        return self._format(summary, config)

    def _fetch_data(self, config: ReportConfig) -> list: ...
    def _summarize(self, data: list) -> dict: ...
    def _format(self, summary: dict, config: ReportConfig) -> Report: ...
```

---

## Hide internal structure — expose behavior, not data

```python
# ❌ BAD — caller bypasses business rules
class BankAccount:
    balance: Decimal = Decimal(0)

account.balance += Decimal("100")   # no validation

# ✅ GOOD
class BankAccount:
    def __init__(self) -> None:
        self._balance = Decimal(0)

    def deposit(self, amount: Decimal) -> None:
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount

    @property
    def balance(self) -> Decimal:
        return self._balance
```

---

## Follow the Law of Demeter — talk only to direct neighbors

```python
# ❌ BAD — chains through two levels of internals
def print_customer_city(order: Order) -> None:
    print(order.customer.address.city)

# ✅ GOOD — Order exposes a method for what callers need
class Order:
    def customer_city(self) -> str:
        return self.customer.address.city

def print_customer_city(order: Order) -> None:
    print(order.customer_city())
```

---

## Always find the root cause — don't suppress errors silently

```python
# ❌ BAD — silent swallow masks the real problem
def get_user(user_id: int):
    try:
        return db.query(user_id)
    except Exception:
        return None

# ✅ GOOD — log and re-raise so callers and ops can see the failure
def get_user(user_id: int) -> User:
    try:
        return db.query(user_id)
    except DatabaseError as e:
        logger.error("DB failure fetching user %s: %s", user_id, e)
        raise
```

---

## One logical assertion per test

```python
# ❌ BAD — four concepts, but the name says "creation"
def test_user_creation():
    user = create_user("jonathan@example.com", "Jonathan")
    assert user.email == "jonathan@example.com"
    assert user.name == "Jonathan"
    assert user.is_active is True
    assert user.created_at is not None

# ✅ GOOD — one concept each
def test_user_stores_correct_email():
    assert create_user("jonathan@example.com", "Jonathan").email == "jonathan@example.com"

def test_new_user_is_active_by_default():
    assert create_user("jonathan@example.com", "Jonathan").is_active is True
```

---

## Fast — tests should run in milliseconds; no real I/O

```python
# ❌ BAD — hits real database, brittle and slow
def test_get_user():
    user = UserService().get_user(1)
    assert user.name == "Jonathan"

# ✅ GOOD — mocked dependency, millisecond execution
def test_get_user(mocker):
    mock_repo = mocker.Mock()
    mock_repo.find_by_id.return_value = User(id=1, name="Jonathan")
    service = UserService(repo=mock_repo)
    assert service.get_user(1).name == "Jonathan"
```

---

## Independent — tests must not depend on each other

```python
# ❌ BAD — test_total fails if run without test_add_item
shared_cart = ShoppingCart()

def test_add_item():
    shared_cart.add(Item("book", 10))

def test_total():
    assert shared_cart.total() == 10

# ✅ GOOD — each test owns its setup
def test_total():
    cart = ShoppingCart()
    cart.add(Item("book", 10))
    assert cart.total() == 10
```

---

## Readable — test names describe behavior, not implementation

```python
# ❌ BAD
def test_func1():
    assert calc(2, 3) == 5

# ✅ GOOD
def test_add_returns_sum_of_two_positive_integers():
    assert calculator.add(2, 3) == 5

def test_add_with_negative_addend_returns_correct_sum():
    assert calculator.add(-1, 5) == 4
```

---

## Single Responsibility — classes should have one reason to change

```python
# ❌ BAD — three reasons to change
class User:
    def save(self): ...         # changes when persistence changes
    def send_email(self): ...   # changes when email changes
    def validate(self): ...     # changes when rules change

# ✅ GOOD
class User: ...                        # domain model only
class UserRepository: ...              # persistence
class UserNotificationService: ...     # email/notifications
class UserValidator: ...               # business rules
```

---

## Use dependency injection — don't instantiate collaborators inside classes

```python
# ❌ BAD — hard-coded, untestable
class OrderService:
    def __init__(self):
        self.repo = PostgresOrderRepository()

# ✅ GOOD — injected, mockable
class OrderService:
    def __init__(self, repo: OrderRepository) -> None:
        self.repo = repo
```

---

## Separate multi-threading / async code from business logic

```python
# ❌ BAD — business rule (sum) tangled with lock management
def process_order(order: Order) -> None:
    lock.acquire()
    try:
        total = sum(item.price for item in order.items)
        db.save(order, total)
    finally:
        lock.release()

# ✅ GOOD — pure function for business logic; async wrapper handles concurrency
def calculate_order_total(order: Order) -> Decimal:
    return sum(item.price for item in order.items)

async def process_order_async(order: Order) -> None:
    async with db_lock:
        total = calculate_order_total(order)
        await db.save(order, total)
```

---

## Keep it simple (KISS) — reduce complexity

```python
# ❌ BAD — approximates a known formula with unnecessary iteration
def calculate_circle_area(radius: float) -> float:
    area = 0.0
    for i in range(360):
        area += (math.pi / 180) * radius * radius
    return area

# ✅ GOOD
def calculate_circle_area(radius: float) -> float:
    return math.pi * radius ** 2
```

---

## Prefer value objects over primitives

```python
# ❌ BAD — nothing stops the caller from passing age where email is expected
def create_account(email: str, age: int) -> None: ...

# ✅ GOOD
@dataclass(frozen=True)
class Email:
    value: str
    def __post_init__(self):
        if "@" not in self.value:
            raise ValueError(f"Invalid email: {self.value}")

@dataclass(frozen=True)
class Age:
    value: int
    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Age cannot be negative")

def create_account(email: Email, age: Age) -> None: ...
```

---

## Rigidity — don't make changes that cascade everywhere

```python
# ❌ BAD — adding "ACH" means editing this function and re-testing everything
def process_payment(payment_type: str, amount: Decimal) -> None:
    if payment_type == "credit":
        credit_processor.charge(amount)
    elif payment_type == "crypto":
        crypto_processor.charge(amount)

# ✅ GOOD — open for extension, closed for modification (OCP)
class PaymentProcessor(Protocol):
    def charge(self, amount: Decimal) -> None: ...

def process_payment(processor: PaymentProcessor, amount: Decimal) -> None:
    processor.charge(amount)
# Adding ACH = new class only, no edits to existing code
```

---

## Opacity — deeply nested code is hard to read; flatten it

```python
# ❌ BAD — four levels of nesting to reach the action
def process_invoice(invoice):
    if invoice:
        if invoice.amount > 0:
            if invoice.status == "pending":
                if invoice.customer:
                    charge(invoice)

# ✅ GOOD — guard clauses; the happy path is obvious
def process_invoice(invoice: Invoice | None) -> None:
    if not invoice:
        return
    if invoice.amount <= 0:
        return
    if invoice.status != "pending":
        return
    if not invoice.customer:
        return
    charge(invoice)
```

---

## Needless complexity — don't over-engineer

```python
# ❌ BAD — abstract base class for a single, fixed greeting
from abc import ABC, abstractmethod

class GreetingStrategy(ABC):
    @abstractmethod
    def execute(self, name: str) -> str: ...

class FormalGreeting(GreetingStrategy):
    def execute(self, name: str) -> str:
        return f"Good day, {name}."

# ✅ GOOD
def greet(name: str) -> str:
    return f"Good day, {name}."
```
