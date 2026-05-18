# State

**Category:** Behavioral
**Refactoring Guru:** https://refactoring.guru/design-patterns/state

## Intent

Allow an object to alter its behavior when its internal state changes — the object will appear to change its class.

## When to Use

- An object's behavior depends on its state, and it must change its behavior at runtime depending on that state
- Operations have large, multi-part conditional statements that depend on the object's state, and the same conditionals appear in multiple operations — State puts each branch of the conditional in a separate class
- State transitions are complex or numerous and need to be explicit and centralized rather than scattered through if/else chains
- You want to avoid state-mutation bugs where an object accidentally ends up in an illegal combination of flag values

## When NOT to Use

- When the object only has two or three states and the transitions are trivially simple — a plain boolean or enum flag suffices and is far less code
- When the state machine is unlikely to change — the pattern is most valuable when new states or transitions are anticipated
- When performance is critical and the overhead of object creation per state transition is unacceptable

## Structure

- **Context** — Defines the interface of interest to clients. Maintains an instance of a ConcreteState subclass that defines the current state, and delegates state-specific requests to the current ConcreteState object.
- **State** — Defines an interface for encapsulating the behavior associated with a particular state of the Context.
- **ConcreteState** — Each subclass (or class implementing State) implements the behavior associated with a state of the Context. May also be responsible for triggering transitions by calling `setState` on the Context.

## TypeScript Example

### Without the Pattern

```typescript
// Without State, every method on TrafficLight is a wall of if/else
// that grows with every new state or rule change.

type LightState = "red" | "yellow" | "green";

class TrafficLight {
  private state: LightState = "red";

  next(): void {
    if (this.state === "red") {
      this.state = "green";
    } else if (this.state === "green") {
      this.state = "yellow";
    } else if (this.state === "yellow") {
      this.state = "red";
    }
  }

  canCross(): boolean {
    if (this.state === "green") return true;
    if (this.state === "yellow") return false;
    if (this.state === "red") return false;
    return false; // unreachable, but compiler demands it
  }

  toString(): string {
    if (this.state === "red") return "STOP";
    if (this.state === "green") return "GO";
    if (this.state === "yellow") return "CAUTION";
    return "";
  }
}
// Adding a "flashing red" state means touching every method above.
```

### With the Pattern

```typescript
// State interface
interface TrafficLightState {
  next(light: TrafficLight): void;
  canCross(): boolean;
  toString(): string;
}

// Concrete States
class RedState implements TrafficLightState {
  next(light: TrafficLight): void {
    light.setState(new GreenState());
  }
  canCross(): boolean { return false; }
  toString(): string { return "STOP"; }
}

class GreenState implements TrafficLightState {
  next(light: TrafficLight): void {
    light.setState(new YellowState());
  }
  canCross(): boolean { return true; }
  toString(): string { return "GO"; }
}

class YellowState implements TrafficLightState {
  next(light: TrafficLight): void {
    light.setState(new RedState());
  }
  canCross(): boolean { return false; }
  toString(): string { return "CAUTION"; }
}

// Adding FlashingRedState is a new class — no existing code changes
class FlashingRedState implements TrafficLightState {
  next(light: TrafficLight): void {
    light.setState(new RedState());
  }
  canCross(): boolean { return false; }
  toString(): string { return "FLASHING RED — STOP THEN PROCEED"; }
}

// Context
class TrafficLight {
  private state: TrafficLightState;

  constructor() {
    this.state = new RedState();
  }

  setState(state: TrafficLightState): void {
    this.state = state;
  }

  next(): void { this.state.next(this); }
  canCross(): boolean { return this.state.canCross(); }
  toString(): string { return this.state.toString(); }
}

// Client
const light = new TrafficLight();
console.log(light.toString());   // STOP
light.next();
console.log(light.toString());   // GO
console.log(light.canCross());   // true
light.next();
console.log(light.toString());   // CAUTION
light.next();
console.log(light.toString());   // STOP
```

## Python Example

### Without the Pattern

```python
from typing import Literal

LightState = Literal["red", "yellow", "green"]

class TrafficLight:
    def __init__(self) -> None:
        self._state: LightState = "red"

    def next(self) -> None:
        if self._state == "red":
            self._state = "green"
        elif self._state == "green":
            self._state = "yellow"
        elif self._state == "yellow":
            self._state = "red"

    def can_cross(self) -> bool:
        return self._state == "green"

    def __str__(self) -> str:
        return {"red": "STOP", "green": "GO", "yellow": "CAUTION"}[self._state]
```

### With the Pattern

```python
from __future__ import annotations
from abc import ABC, abstractmethod

class TrafficLightState(ABC):
    @abstractmethod
    def next(self, light: "TrafficLight") -> None: ...

    @abstractmethod
    def can_cross(self) -> bool: ...

    @abstractmethod
    def __str__(self) -> str: ...

class RedState(TrafficLightState):
    def next(self, light: "TrafficLight") -> None:
        light.set_state(GreenState())

    def can_cross(self) -> bool:
        return False

    def __str__(self) -> str:
        return "STOP"

class GreenState(TrafficLightState):
    def next(self, light: "TrafficLight") -> None:
        light.set_state(YellowState())

    def can_cross(self) -> bool:
        return True

    def __str__(self) -> str:
        return "GO"

class YellowState(TrafficLightState):
    def next(self, light: "TrafficLight") -> None:
        light.set_state(RedState())

    def can_cross(self) -> bool:
        return False

    def __str__(self) -> str:
        return "CAUTION"

class FlashingRedState(TrafficLightState):
    def next(self, light: "TrafficLight") -> None:
        light.set_state(RedState())

    def can_cross(self) -> bool:
        return False

    def __str__(self) -> str:
        return "FLASHING RED — STOP THEN PROCEED"

# Context
class TrafficLight:
    def __init__(self) -> None:
        self._state: TrafficLightState = RedState()

    def set_state(self, state: TrafficLightState) -> None:
        self._state = state

    def next(self) -> None:
        self._state.next(self)

    def can_cross(self) -> bool:
        return self._state.can_cross()

    def __str__(self) -> str:
        return str(self._state)

# Client
light = TrafficLight()
print(light)          # STOP
light.next()
print(light)          # GO
print(light.can_cross())  # True
light.next()
print(light)          # CAUTION
```

## Real-World Analogy

Consider a vending machine. When it is in the "idle" state, inserting money moves it to "has credit." When it has credit, selecting a product moves it to "dispensing." After dispensing, it returns to "idle." The machine's buttons behave differently depending on its current state — pressing "dispense" when idle does nothing, but pressing it when credit has been inserted delivers the item. Each state defines a complete and self-contained set of valid behaviors; the machine's overall behavior is the sum of its current state's rules.

## Related Patterns

- **Flyweight** — explains when and how State objects can be shared (when states carry no instance-specific data)
- **Singleton** — State objects are often implemented as Singletons when they have no instance data
- **Strategy** — both patterns use delegation to change behavior; in Strategy the client typically chooses the algorithm, while in State the Context (or the state itself) drives transitions automatically
