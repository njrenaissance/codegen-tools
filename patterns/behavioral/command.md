# Command

**Category:** Behavioral
**Refactoring Guru:** https://refactoring.guru/design-patterns/command

## Intent

Encapsulate a request as an object, thereby letting you parameterize clients with different requests, queue or log requests, and support undoable operations.

## When to Use

- You want to parameterize objects with an action to perform — Command is an object-oriented replacement for a callback function.
- You need to specify, queue, and execute requests at different times — the Command object can have a lifetime independent of the original request.
- You need to support undo/redo — a Command object stores the state needed to reverse the operation, and a history stack replays or reverses commands.
- You want to support transactions: a sequence of operations that must all succeed or all be rolled back together.
- You need to log changes so they can be reapplied after a crash or system restart (command log / audit trail).
- You want to build a macro system where a user can record a sequence of operations and replay them.

## When NOT to Use

- The operations are simple, one-off, and never need to be undone or queued — wrapping them in command objects adds indirection without benefit.
- The system doesn't require history, audit logging, or deferred execution — a direct method call is clearer.
- The command object would need to reference the receiver so heavily that it becomes tightly coupled — at that point, a plain function or method is simpler.
- Undo/redo is needed but state snapshots (Memento) are a better fit because reversal logic is prohibitively complex.

## Structure

**Command** declares an interface for executing an operation, typically just `execute()`, and optionally `undo()`.

**ConcreteCommand** defines a binding between a Receiver object and an action. It implements `execute()` by invoking the corresponding operation(s) on the Receiver, and stores any state needed to reverse the action.

**Receiver** knows how to perform the operations associated with carrying out a request. Any class may serve as a Receiver.

**Invoker** asks the Command to carry out the request. It holds a reference to a Command and may maintain a command history.

**Client** creates a ConcreteCommand object and sets its Receiver, then passes the command to the Invoker.

## TypeScript Example

### ❌ Without the Pattern

```typescript
// A text editor with direct method calls for every action.
// Undo is impossible because no history is kept.
// Each toolbar button calls editor methods directly — no abstraction.

class TextBuffer {
  private content = "";

  insert(position: number, text: string): void {
    this.content =
      this.content.slice(0, position) + text + this.content.slice(position);
  }

  delete(position: number, length: number): void {
    this.content =
      this.content.slice(0, position) + this.content.slice(position + length);
  }

  getContent(): string {
    return this.content;
  }
}

// Toolbar buttons call methods directly — no way to undo
class EditorToolbar {
  constructor(private buffer: TextBuffer) {}

  onTypeCharacter(char: string, position: number): void {
    this.buffer.insert(position, char);  // lost immediately — can't undo
  }

  onDeleteCharacter(position: number): void {
    this.buffer.delete(position, 1);  // gone — no record kept
  }

  onPaste(text: string, position: number): void {
    this.buffer.insert(position, text);  // same problem
  }
}

const buffer = new TextBuffer();
const toolbar = new EditorToolbar(buffer);

toolbar.onTypeCharacter("H", 0);
toolbar.onTypeCharacter("e", 1);
toolbar.onTypeCharacter("l", 2);
toolbar.onPaste("lo!", 3);
console.log(buffer.getContent()); // "Hello!"
// User hits Ctrl+Z — nothing happens. No history.
```

### ✅ With the Pattern

```typescript
// Each editing action is a Command object.
// The Invoker maintains a history stack enabling full undo/redo.

// Receiver
class TextBuffer {
  private content = "";

  insert(position: number, text: string): void {
    this.content =
      this.content.slice(0, position) + text + this.content.slice(position);
  }

  delete(position: number, length: number): string {
    const deleted = this.content.slice(position, position + length);
    this.content =
      this.content.slice(0, position) + this.content.slice(position + length);
    return deleted;
  }

  getContent(): string {
    return this.content;
  }
}

// Command interface
interface EditorCommand {
  execute(): void;
  undo(): void;
  readonly description: string;
}

// ConcreteCommand: Insert text
class InsertCommand implements EditorCommand {
  readonly description: string;

  constructor(
    private readonly buffer: TextBuffer,
    private readonly position: number,
    private readonly text: string
  ) {
    this.description = `Insert "${text}" at position ${position}`;
  }

  execute(): void {
    this.buffer.insert(this.position, this.text);
  }

  undo(): void {
    this.buffer.delete(this.position, this.text.length);
  }
}

// ConcreteCommand: Delete text
class DeleteCommand implements EditorCommand {
  readonly description: string;
  private deletedText = "";

  constructor(
    private readonly buffer: TextBuffer,
    private readonly position: number,
    private readonly length: number
  ) {
    this.description = `Delete ${length} char(s) at position ${position}`;
  }

  execute(): void {
    this.deletedText = this.buffer.delete(this.position, this.length);
  }

  undo(): void {
    this.buffer.insert(this.position, this.deletedText);
  }
}

// ConcreteCommand: Macro — composes multiple commands into one undoable unit
class MacroCommand implements EditorCommand {
  readonly description: string;

  constructor(
    private readonly commands: EditorCommand[],
    description: string
  ) {
    this.description = description;
  }

  execute(): void {
    this.commands.forEach(c => c.execute());
  }

  undo(): void {
    // Reverse order
    [...this.commands].reverse().forEach(c => c.undo());
  }
}

// Invoker — manages history
class EditorHistory {
  private history: EditorCommand[] = [];
  private redoStack: EditorCommand[] = [];

  execute(command: EditorCommand): void {
    command.execute();
    this.history.push(command);
    this.redoStack = []; // new action clears redo stack
    console.log(`  [History] Executed: ${command.description}`);
  }

  undo(): void {
    const command = this.history.pop();
    if (!command) {
      console.log("  [History] Nothing to undo.");
      return;
    }
    command.undo();
    this.redoStack.push(command);
    console.log(`  [History] Undid: ${command.description}`);
  }

  redo(): void {
    const command = this.redoStack.pop();
    if (!command) {
      console.log("  [History] Nothing to redo.");
      return;
    }
    command.execute();
    this.history.push(command);
    console.log(`  [History] Redid: ${command.description}`);
  }

  getHistoryLog(): string[] {
    return this.history.map(c => c.description);
  }
}

// Usage
const buffer = new TextBuffer();
const history = new EditorHistory();

history.execute(new InsertCommand(buffer, 0, "Hello"));
history.execute(new InsertCommand(buffer, 5, ", World"));
console.log("Content:", buffer.getContent()); // "Hello, World"

history.execute(new DeleteCommand(buffer, 5, 7)); // removes ", World"
console.log("Content:", buffer.getContent()); // "Hello"

history.undo(); // restores ", World"
console.log("After undo:", buffer.getContent()); // "Hello, World"

history.redo(); // removes it again
console.log("After redo:", buffer.getContent()); // "Hello"

// Macro: bold selection = insert "**" before and after
const boldCommand = new MacroCommand(
  [
    new InsertCommand(buffer, 0, "**"),
    new InsertCommand(buffer, 7, "**"),
  ],
  "Bold selection"
);
history.execute(boldCommand);
console.log("After bold:", buffer.getContent()); // "**Hello**"

history.undo(); // removes both markers in one undo
console.log("After undo bold:", buffer.getContent()); // "Hello"

console.log("\nHistory log:", history.getHistoryLog());
```

## Python Example

### ❌ Without the Pattern

```python
# HTTP request queue with direct execution — no retry, no audit, no deferred dispatch.

import time

class HttpClient:
    def post(self, url: str, body: dict) -> dict:
        print(f"[HTTP] POST {url} body={body}")
        return {"status": 200, "url": url}

    def delete(self, url: str) -> dict:
        print(f"[HTTP] DELETE {url}")
        return {"status": 204, "url": url}

client = HttpClient()

# Operations fire immediately, inline — can't queue, retry, or replay
client.post("/api/orders", {"item": "Widget", "qty": 1})
client.post("/api/payments", {"amount": 29.99})
client.delete("/api/sessions/abc")
# If the payment fails mid-way, there's no rollback record.
```

### ✅ With the Pattern

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

# Receiver
class ApiClient:
    def __init__(self, base_url: str) -> None:
        self._base_url = base_url
        self._store: dict[str, Any] = {}  # simulated DB

    def post(self, path: str, body: dict) -> dict:
        resource_id = f"id_{len(self._store) + 1}"
        self._store[resource_id] = body
        print(f"[API] POST {self._base_url}{path} → created {resource_id}")
        return {"id": resource_id, **body}

    def delete(self, path: str, resource_id: str) -> None:
        removed = self._store.pop(resource_id, None)
        print(f"[API] DELETE {self._base_url}{path}/{resource_id} → {'ok' if removed else 'not found'}")

    def get_all(self) -> dict:
        return dict(self._store)

# Command interface
class ApiCommand(ABC):
    @abstractmethod
    def execute(self) -> Any: ...

    @abstractmethod
    def undo(self) -> None: ...

    @property
    @abstractmethod
    def description(self) -> str: ...

# ConcreteCommand: Create resource
@dataclass
class CreateResourceCommand(ApiCommand):
    client: ApiClient
    path: str
    body: dict
    _created_id: str = field(default="", init=False, repr=False)

    def execute(self) -> dict:
        result = self.client.post(self.path, self.body)
        self._created_id = result["id"]
        return result

    def undo(self) -> None:
        if self._created_id:
            self.client.delete(self.path, self._created_id)

    @property
    def description(self) -> str:
        return f"CREATE {self.path} {self.body}"

# ConcreteCommand: Delete resource
@dataclass
class DeleteResourceCommand(ApiCommand):
    client: ApiClient
    path: str
    resource_id: str
    _backup: dict = field(default_factory=dict, init=False, repr=False)

    def execute(self) -> None:
        self._backup = self.client._store.get(self.resource_id, {})
        self.client.delete(self.path, self.resource_id)

    def undo(self) -> None:
        if self._backup:
            self.client._store[self.resource_id] = self._backup
            print(f"[API] Restored {self.resource_id} at {self.path}")

    @property
    def description(self) -> str:
        return f"DELETE {self.path}/{self.resource_id}"

# Invoker — command queue with audit log and undo support
class CommandQueue:
    def __init__(self) -> None:
        self._queue: list[ApiCommand] = []
        self._executed: list[tuple[datetime, ApiCommand]] = []
        self._undo_stack: list[ApiCommand] = []

    def enqueue(self, command: ApiCommand) -> None:
        self._queue.append(command)
        print(f"  [Queue] Enqueued: {command.description}")

    def flush(self) -> None:
        """Execute all queued commands in order."""
        print(f"\n  [Queue] Flushing {len(self._queue)} command(s)...")
        while self._queue:
            cmd = self._queue.pop(0)
            cmd.execute()
            self._executed.append((datetime.utcnow(), cmd))
            self._undo_stack.append(cmd)

    def undo_last(self) -> None:
        if not self._undo_stack:
            print("  [Queue] Nothing to undo.")
            return
        cmd = self._undo_stack.pop()
        cmd.undo()
        print(f"  [Queue] Undid: {cmd.description}")

    def audit_log(self) -> None:
        print("\n  [Audit Log]")
        for ts, cmd in self._executed:
            print(f"    {ts.strftime('%H:%M:%S')} — {cmd.description}")

# Usage
client = ApiClient("https://api.example.com")
queue = CommandQueue()

# Enqueue a batch of operations (deferred execution)
queue.enqueue(CreateResourceCommand(client, "/orders", {"item": "Widget", "qty": 2}))
queue.enqueue(CreateResourceCommand(client, "/orders", {"item": "Gadget", "qty": 1}))
queue.enqueue(CreateResourceCommand(client, "/payments", {"amount": 89.97, "method": "stripe"}))

# Execute all at once (e.g., after user confirms)
queue.flush()

print("\nCurrent store:", client.get_all())

# Undo the last operation (payment)
queue.undo_last()
print("After undo:", client.get_all())

# Audit trail
queue.audit_log()
```

## Real-World Analogy

Consider a restaurant. When a customer orders, the waiter writes the order on a ticket (the Command object). The ticket is passed to the kitchen (the Invoker's queue) — the waiter doesn't cook the food. The chef (the Receiver) reads the ticket and prepares the dish. The ticket can be held, re-ordered, cancelled, or even displayed on a board. This separation means the waiter never needs to know how each dish is prepared, the kitchen can process orders in any sequence it likes, and the restaurant can log every ticket for billing and analysis. The Command pattern gives software the same flexibility: requests become first-class objects that can be stored, queued, logged, and reversed.

## Related Patterns

- **Memento** — Command and Memento work together for undo. Command determines what to undo; Memento stores the state needed to reverse an operation. When reversal is based on restoring state rather than executing an inverse operation, prefer Memento.
- **Composite** — MacroCommand is a natural application of the Composite pattern: a command that is composed of sub-commands and treated uniformly.
- **Prototype** — Commands that must be copied before being placed on a history list can use Prototype.
- **Chain of Responsibility** — both decouple senders from receivers, but Chain passes a request along a chain until one handler processes it, while Command always binds a request to a specific receiver.
