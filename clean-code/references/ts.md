# Clean Code Standards — TypeScript Examples

TypeScript ❌ BAD / ✅ GOOD examples for the Clean Code rules. Each section
heading matches a rule name in [`CLEAN-CODE.md`](../CLEAN-CODE.md), which
links here by that name.

---

## Boy Scout Rule — leave code cleaner than you found it

```typescript
// ❌ BAD — left as-is
function proc(x: number, y: number) { return x * y; }

// ✅ GOOD — cleaned up while you were here
function calculateTotalPrice(unitPrice: number, quantity: number): number {
  return unitPrice * quantity;
}
```

---

## Use descriptive, unambiguous names

```typescript
// ❌ BAD
function proc(d: number, f: number): number { return d * f; }

// ✅ GOOD
function calculateTotalCost(unitPrice: number, quantity: number): number {
  return unitPrice * quantity;
}
```

---

## Use pronounceable names

```typescript
// ❌ BAD
const genymdhms = new Date();
const modymdhms = new Date();

// ✅ GOOD
const generationTimestamp  = new Date();
const modificationTimestamp = new Date();
```

---

## Use searchable names — avoid magic numbers

```typescript
// ❌ BAD
if (days > 7) sendReminder();

// ✅ GOOD
const REMINDER_THRESHOLD_DAYS = 7;
if (days > REMINDER_THRESHOLD_DAYS) sendReminder();
```

---

## Avoid encodings and type noise

```typescript
// ❌ BAD
const strUserName = "Jonathan";
const iUserAge    = 51;
const lstOrders: Order[] = [];

// ✅ GOOD
const userName = "Jonathan";
const userAge  = 51;
const orders: Order[] = [];
```

---

## Be consistent — same pattern everywhere

```typescript
// ❌ BAD
function fetchUserById(id: number) { ... }
function get_user_email(userId: number) { ... }
function loadProfile(uid: number) { ... }

// ✅ GOOD
function getUserById(userId: number): User { ... }
function getUserByEmail(email: string): User { ... }
function getUserProfile(userId: number): UserProfile { ... }
```

---

## Functions should be small and do ONE thing

```typescript
// ❌ BAD — validates, creates, and notifies in one function
function registerUser(data: Record<string, string>): void {
  if (!data.email) throw new Error("Email required");
  const user = new User(data);
  db.add(user);
  sendWelcomeEmail(user.email);
}

// ✅ GOOD — each function has one job
function validateRegistrationData(data: Record<string, string>): void {
  if (!data.email) throw new Error("Email required");
}

function createUser(data: Record<string, string>): User {
  const user = new User(data);
  db.add(user);
  return user;
}

function registerUser(data: Record<string, string>): void {
  validateRegistrationData(data);
  const user = createUser(data);
  sendWelcomeEmail(user.email);
}
```

---

## One level of abstraction per function

```typescript
// ❌ BAD — high-level validateUser() beside raw SQL string
async function processPayment(payment: PaymentInput): Promise<Receipt> {
  validateUser(payment.userId);
  const row = await db.query(
    "INSERT INTO payments (amount, user_id) VALUES ($1, $2) RETURNING *",
    [payment.amount, payment.userId],
  );
  return { id: row.rows[0].id };
}

// ✅ GOOD — every statement at the same abstraction level
async function processPayment(payment: PaymentInput): Promise<Receipt> {
  validateUser(payment.userId);
  return persistPayment(payment);
}

async function persistPayment(payment: PaymentInput): Promise<Receipt> {
  const row = await db.query(
    "INSERT INTO payments (amount, user_id) VALUES ($1, $2) RETURNING *",
    [payment.amount, payment.userId],
  );
  return { id: row.rows[0].id };
}
```

---

## Stepdown Rule — file reads top-to-bottom at decreasing abstraction levels

```typescript
// ❌ BAD — orchestration and raw implementation interleaved
export async function POST(request: Request) {
  const body = await request.json();
  if (!body.title || !body.signers?.length) throw new Error("Invalid input");
  const existing = await db.query(
    "SELECT COUNT(*) FROM envelopes WHERE user_id = $1", [userId]
  );
  if (existing.rows[0].count >= 10) throw new Error("Plan limit reached");
  const envelope = await db.query(
    "INSERT INTO envelopes (title, user_id) VALUES ($1, $2) RETURNING *",
    [body.title, userId],
  );
  for (const signer of body.signers) await sendEmail(signer.email, "Please sign");
  return Response.json(envelope.rows[0]);
}

// ✅ GOOD — top-level reads as a plain-English sequence; detail lives one level down
export async function POST(request: Request) {
  const data = await parseRequestBody(request);
  await validateCreateEnvelopeInput(data);
  await enforceEnvelopePlanLimit(auth.userId);
  const envelope = await createEnvelopeWithSigners(data, auth.userId);
  await dispatchSignerNotifications(envelope);
  return envelopeCreatedResponse(envelope);
}

async function parseRequestBody(request: Request): Promise<CreateEnvelopeInput> { ... }
async function validateCreateEnvelopeInput(data: CreateEnvelopeInput): Promise<void> { ... }
async function enforceEnvelopePlanLimit(userId: string): Promise<void> { ... }
async function createEnvelopeWithSigners(data: CreateEnvelopeInput, userId: string): Promise<Envelope> { ... }
async function dispatchSignerNotifications(envelope: Envelope): Promise<void> { ... }
function envelopeCreatedResponse(envelope: Envelope): Response { ... }
```

---

## Prefer fewer arguments — use parameter objects when needed

```typescript
// ❌ BAD — six positional arguments
function createReport(
  title: string, author: string,
  startDate: Date, endDate: Date,
  includeCharts: boolean, format: string,
): Report { ... }

// ✅ GOOD
interface ReportConfig {
  title: string;
  author: string;
  startDate: Date;
  endDate: Date;
  includeCharts?: boolean;
  format?: "pdf" | "csv";
}

function createReport(config: ReportConfig): Report { ... }
```

---

## Don't use flag arguments — split into separate functions

```typescript
// ❌ BAD
function renderPage(includeHeader: boolean): string {
  return includeHeader ? renderWithHeader() : renderWithoutHeader();
}

// ✅ GOOD
function renderPageWithHeader(): string { ... }
function renderPage(): string { ... }
```

---

## No side effects — a function should do what its name says and nothing else

```typescript
// ❌ BAD — name says "read", but function also writes
async function getUser(userId: string): Promise<User> {
  const user = await db.find(userId);
  user.lastAccessed = new Date();   // hidden side effect
  await db.save(user);
  return user;
}

// ✅ GOOD
async function getUser(userId: string): Promise<User> {
  return db.find(userId);
}

async function recordAccess(user: User): Promise<void> {
  user.lastAccessed = new Date();
  await db.save(user);
}
```

---

## Explain yourself in code, not in comments

```typescript
// ❌ BAD
// Check if the user is old enough to purchase alcohol
if (user.age >= 21) allowPurchase();

// ✅ GOOD
const MINIMUM_ALCOHOL_PURCHASE_AGE = 21;

function isEligibleToPurchaseAlcohol(user: User): boolean {
  return user.age >= MINIMUM_ALCOHOL_PURCHASE_AGE;
}

if (isEligibleToPurchaseAlcohol(user)) allowPurchase();
```

---

## Use comments to explain INTENT, WARNINGS, and non-obvious decisions

```typescript
// ❌ BAD
// Add item to array
items.push(item);

// ✅ GOOD — explains a non-obvious trade-off
// Sorting on every insert rather than at read time because reads
// outnumber writes 100:1 in the order processing pipeline.
items.push(item);
items.sort((a, b) => a.priority - b.priority);

// ✅ GOOD — safety warning
// WARNING: Permanently deletes the user and all associated data.
// No soft-delete. Caller must present a confirmation dialog first.
async function hardDeleteUser(userId: string): Promise<void> {
  await db.execute("DELETE FROM users WHERE id = $1", [userId]);
}
```

---

## Never comment out dead code — delete it

```typescript
// ❌ BAD
async function processPayment(amount: number): Promise<Receipt> {
  // await oldChargeService.charge(amount);
  // const legacyReceipt = oldReceiptService.create();
  return newPaymentService.charge(amount);
}

// ✅ GOOD
async function processPayment(amount: number): Promise<Receipt> {
  return newPaymentService.charge(amount);
}
```

---

## Declare variables close to their usage

```typescript
// ❌ BAD
function processOrder(order: Order): void {
  const TAX_RATE = 0.08;
  // ... 30 lines of unrelated logic ...
  const subtotal = order.items.reduce((s, i) => s + i.price, 0);
  const total    = subtotal * (1 + TAX_RATE);
}

// ✅ GOOD
function processOrder(order: Order): void {
  // ... other logic ...
  const TAX_RATE = 0.08;
  const subtotal = order.items.reduce((s, i) => s + i.price, 0);
  const total    = subtotal * (1 + TAX_RATE);
}
```

---

## Place caller above callee — high-level first

```typescript
// ✅ GOOD — public method at top, private helpers below
class ReportService {
  generateReport(config: ReportConfig): Report {
    const data    = this.fetchData(config);
    const summary = this.summarize(data);
    return this.format(summary, config);
  }

  private fetchData(config: ReportConfig): Row[] { ... }
  private summarize(data: Row[]): Summary { ... }
  private format(summary: Summary, config: ReportConfig): Report { ... }
}
```

---

## Hide internal structure — expose behavior, not data

```typescript
// ❌ BAD — caller bypasses business rules
class BankAccount { balance = 0; }
account.balance += 100;   // no validation

// ✅ GOOD
class BankAccount {
  private _balance = 0;

  deposit(amount: number): void {
    if (amount <= 0) throw new Error("Deposit must be positive");
    this._balance += amount;
  }

  get balance(): number { return this._balance; }
}
```

---

## Follow the Law of Demeter — talk only to direct neighbors

```typescript
// ❌ BAD — chains through two levels of internals
function printCustomerCity(order: Order): void {
  console.log(order.customer.address.city);
}

// ✅ GOOD
class Order {
  customerCity(): string { return this.customer.address.city; }
}

function printCustomerCity(order: Order): void {
  console.log(order.customerCity());
}
```

---

## Always find the root cause — don't suppress errors silently

```typescript
// ❌ BAD — silent catch hides the real problem
async function getUser(userId: string): Promise<User | null> {
  try {
    return await db.find(userId);
  } catch {
    return null;
  }
}

// ✅ GOOD
async function getUser(userId: string): Promise<User> {
  try {
    return await db.find(userId);
  } catch (err) {
    logger.error({ userId, err }, "DB failure fetching user");
    throw err;
  }
}
```

---

## One logical assertion per test

```typescript
// ❌ BAD
it("creates a user", () => {
  const user = createUser("jonathan@example.com", "Jonathan");
  expect(user.email).toBe("jonathan@example.com");
  expect(user.isActive).toBe(true);
});

// ✅ GOOD
it("stores the correct email", () => {
  expect(createUser("jonathan@example.com", "Jonathan").email).toBe("jonathan@example.com");
});

it("activates new users by default", () => {
  expect(createUser("jonathan@example.com", "Jonathan").isActive).toBe(true);
});
```

---

## Fast — tests should run in milliseconds; no real I/O

```typescript
// ❌ BAD — hits real database
it("gets a user", async () => {
  const user = await new UserService().getUser("1");
  expect(user.name).toBe("Jonathan");
});

// ✅ GOOD
it("gets a user", async () => {
  const repo = { findById: jest.fn().mockResolvedValue({ id: "1", name: "Jonathan" }) };
  const user = await new UserService(repo).getUser("1");
  expect(user.name).toBe("Jonathan");
});
```

---

## Independent — tests must not depend on each other

```typescript
// ❌ BAD — shared state between tests
const sharedCart = new ShoppingCart();
it("adds an item", () => sharedCart.add({ name: "book", price: 10 }));
it("totals items",  () => expect(sharedCart.total()).toBe(10));   // fails if run alone

// ✅ GOOD
it("totals items", () => {
  const cart = new ShoppingCart();
  cart.add({ name: "book", price: 10 });
  expect(cart.total()).toBe(10);
});
```

---

## Readable — test names describe behavior, not implementation

```typescript
// ❌ BAD
it("test1", () => expect(calc(2, 3)).toBe(5));

// ✅ GOOD
it("returns the sum of two positive integers", () => {
  expect(calculator.add(2, 3)).toBe(5);
});

it("handles a negative addend correctly", () => {
  expect(calculator.add(-1, 5)).toBe(4);
});
```

---

## Single Responsibility — classes should have one reason to change

```typescript
// ❌ BAD
class User {
  save(): void { ... }
  sendEmail(): void { ... }
  validate(): void { ... }
}

// ✅ GOOD
class User { ... }
class UserRepository { ... }
class UserNotificationService { ... }
class UserValidator { ... }
```

---

## Use dependency injection — don't instantiate collaborators inside classes

```typescript
// ❌ BAD — hard-coded, untestable
class OrderService {
  private repo = new PostgresOrderRepository();
}

// ✅ GOOD — injected, mockable
class OrderService {
  constructor(private readonly repo: OrderRepository) {}
}
```

---

## Separate multi-threading / async code from business logic

```typescript
// ❌ BAD — business rule tangled with mutex
async function processOrder(order: Order): Promise<void> {
  await mutex.acquire();
  try {
    const total = order.items.reduce((s, i) => s + i.price, 0);
    await db.save(order, total);
  } finally {
    mutex.release();
  }
}

// ✅ GOOD — pure function for business logic; wrapper handles concurrency
function calculateOrderTotal(order: Order): number {
  return order.items.reduce((s, i) => s + i.price, 0);
}

async function processOrder(order: Order): Promise<void> {
  await mutex.runExclusive(async () => {
    const total = calculateOrderTotal(order);
    await db.save(order, total);
  });
}
```

---

## Keep it simple (KISS) — reduce complexity

```typescript
// ❌ BAD
function calculateCircleArea(radius: number): number {
  let area = 0;
  for (let i = 0; i < 360; i++) area += (Math.PI / 180) * radius * radius;
  return area;
}

// ✅ GOOD
function calculateCircleArea(radius: number): number {
  return Math.PI * radius ** 2;
}
```

---

## Prefer value objects over primitives

```typescript
// ❌ BAD — nothing stops the caller from transposing email and age
function createAccount(email: string, age: number): void { ... }

// ✅ GOOD — branded types prevent transposition at compile time
type Email = string & { readonly __brand: "Email" };
type Age   = number & { readonly __brand: "Age" };

function parseEmail(raw: string): Email {
  if (!raw.includes("@")) throw new Error(`Invalid email: ${raw}`);
  return raw as Email;
}

function parseAge(raw: number): Age {
  if (raw < 0) throw new Error("Age cannot be negative");
  return raw as Age;
}

function createAccount(email: Email, age: Age): void { ... }
```

---

## Rigidity — don't make changes that cascade everywhere

```typescript
// ❌ BAD — every new payment type requires editing this switch
function processPayment(type: string, amount: number): void {
  if (type === "credit") creditProcessor.charge(amount);
  else if (type === "crypto") cryptoProcessor.charge(amount);
}

// ✅ GOOD
interface PaymentProcessor {
  charge(amount: number): void;
}

function processPayment(processor: PaymentProcessor, amount: number): void {
  processor.charge(amount);
}
```

---

## Opacity — deeply nested code is hard to read; flatten it

```typescript
// ❌ BAD
function processInvoice(invoice: Invoice | null): void {
  if (invoice) {
    if (invoice.amount > 0) {
      if (invoice.status === "pending") {
        if (invoice.customer) charge(invoice);
      }
    }
  }
}

// ✅ GOOD — guard clauses
function processInvoice(invoice: Invoice | null): void {
  if (!invoice) return;
  if (invoice.amount <= 0) return;
  if (invoice.status !== "pending") return;
  if (!invoice.customer) return;
  charge(invoice);
}
```

---

## Needless complexity — don't over-engineer

```typescript
// ❌ BAD — Strategy pattern for a single, fixed greeting that will never vary
interface GreetingStrategy { execute(name: string): string; }
class FormalGreeting implements GreetingStrategy {
  execute(name: string) { return `Good day, ${name}.`; }
}
class GreetingContext {
  constructor(private strategy: GreetingStrategy) {}
  greet(name: string) { return this.strategy.execute(name); }
}

// ✅ GOOD
function greet(name: string): string { return `Good day, ${name}.`; }
```
