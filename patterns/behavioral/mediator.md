# Mediator

**Category:** Behavioral
**Refactoring Guru:** https://refactoring.guru/design-patterns/mediator

## Intent

Define an object that encapsulates how a set of objects interact, promoting loose coupling by keeping objects from referring to each other explicitly and letting you vary their interaction independently.

## When to Use

- A set of objects communicate in well-defined but complex ways, and the resulting interdependencies are unstructured and difficult to understand (the "spaghetti of references" problem)
- Reusing an object is difficult because it refers to and communicates with many other objects
- A behavior that is distributed across several classes should be customizable without extensive subclassing — centralizing the behavior in a Mediator makes it easy to subclass
- You have a group of objects that could benefit from centralized control or coordination (e.g., a chat room, an air traffic controller, a UI dialog with many interdependent widgets)

## When NOT to Use

- When there are only two or three objects interacting — direct references are simpler and the mediator is unnecessary indirection
- When the mediator itself becomes a "God Object" that knows too much about too many things — this indicates the design needs decomposition, not just mediation
- When the interaction rules are stable and simple — a mediator adds a layer of abstraction that is only beneficial when the rules are complex or frequently changing

## Structure

- **Mediator** — Defines an interface for communicating with Colleague objects.
- **ConcreteMediator** — Implements cooperative behavior by coordinating Colleague objects. Knows and maintains its colleagues.
- **Colleague** — Each Colleague class knows its Mediator object. Each colleague communicates with its mediator whenever it would have otherwise communicated with another colleague.

## TypeScript Example

### Without the Pattern

```typescript
// Without Mediator, every UI widget holds direct references to all others.
// Adding a new widget means updating all existing widgets.

class CheckboxWidget {
  private submitButton!: ButtonWidget;
  private textInput!: TextInputWidget;

  setDependencies(btn: ButtonWidget, input: TextInputWidget): void {
    this.submitButton = btn;
    this.textInput = input;
  }

  onChange(checked: boolean): void {
    if (checked) {
      this.submitButton.enable();
      this.textInput.show();
    } else {
      this.submitButton.disable();
      this.textInput.hide();
    }
  }
}

class ButtonWidget {
  enable(): void { console.log("Button enabled"); }
  disable(): void { console.log("Button disabled"); }
}

class TextInputWidget {
  show(): void { console.log("Input shown"); }
  hide(): void { console.log("Input hidden"); }
}

// Tight coupling: every widget knows the others
const btn = new ButtonWidget();
const input = new TextInputWidget();
const checkbox = new CheckboxWidget();
checkbox.setDependencies(btn, input);
// Adding a DropdownWidget now requires modifying CheckboxWidget too.
```

### With the Pattern

```typescript
// Mediator interface
interface DialogMediator {
  notify(sender: Widget, event: string): void;
}

// Colleague base
abstract class Widget {
  constructor(protected mediator: DialogMediator) {}

  protected emit(event: string): void {
    this.mediator.notify(this, event);
  }
}

// Concrete Colleagues
class CheckboxWidget extends Widget {
  private checked = false;

  toggle(): void {
    this.checked = !this.checked;
    this.emit(this.checked ? "checked" : "unchecked");
  }

  isChecked(): boolean { return this.checked; }
}

class ButtonWidget extends Widget {
  private enabled = false;

  setEnabled(value: boolean): void {
    this.enabled = value;
    console.log(`Button is now ${value ? "enabled" : "disabled"}`);
  }

  click(): void {
    if (this.enabled) this.emit("clicked");
  }
}

class TextInputWidget extends Widget {
  private visible = false;

  setVisible(value: boolean): void {
    this.visible = value;
    console.log(`TextInput is now ${value ? "visible" : "hidden"}`);
  }
}

// ConcreteMediator — all coordination logic lives here
class RegistrationDialog implements DialogMediator {
  constructor(
    public checkbox: CheckboxWidget,
    public submitButton: ButtonWidget,
    public extraInfo: TextInputWidget
  ) {}

  notify(sender: Widget, event: string): void {
    if (sender === this.checkbox) {
      const checked = this.checkbox.isChecked();
      this.submitButton.setEnabled(checked);
      this.extraInfo.setVisible(checked);
    }

    if (sender === this.submitButton && event === "clicked") {
      console.log("Form submitted!");
    }
  }
}

// Wiring — only the mediator holds references to all widgets
const mediator = {} as DialogMediator; // placeholder for circular init
const checkbox = new CheckboxWidget(mediator);
const submitBtn = new ButtonWidget(mediator);
const extraInfo = new TextInputWidget(mediator);

const dialog = new RegistrationDialog(checkbox, submitBtn, extraInfo);
// Now patch the mediator reference (or use a factory/DI to avoid this)
Object.assign(mediator, dialog);

checkbox.toggle(); // Button enabled + TextInput visible
checkbox.toggle(); // Button disabled + TextInput hidden
// Adding a new DropdownWidget only requires a change in RegistrationDialog.notify()
```

## Python Example

### Without the Pattern

```python
class CheckboxWidget:
    def __init__(self) -> None:
        self._button: "ButtonWidget | None" = None
        self._input: "TextInputWidget | None" = None

    def set_dependencies(self, btn: "ButtonWidget", inp: "TextInputWidget") -> None:
        self._button = btn
        self._input = inp

    def on_change(self, checked: bool) -> None:
        if checked:
            self._button and self._button.enable()
            self._input and self._input.show()
        else:
            self._button and self._button.disable()
            self._input and self._input.hide()

class ButtonWidget:
    def enable(self) -> None: print("Button enabled")
    def disable(self) -> None: print("Button disabled")

class TextInputWidget:
    def show(self) -> None: print("Input shown")
    def hide(self) -> None: print("Input hidden")
```

### With the Pattern

```python
from __future__ import annotations
from abc import ABC, abstractmethod

class DialogMediator(ABC):
    @abstractmethod
    def notify(self, sender: "Widget", event: str) -> None: ...

class Widget(ABC):
    def __init__(self, mediator: DialogMediator) -> None:
        self._mediator = mediator

    def emit(self, event: str) -> None:
        self._mediator.notify(self, event)

class CheckboxWidget(Widget):
    def __init__(self, mediator: DialogMediator) -> None:
        super().__init__(mediator)
        self._checked = False

    def toggle(self) -> None:
        self._checked = not self._checked
        self.emit("checked" if self._checked else "unchecked")

    def is_checked(self) -> bool:
        return self._checked

class ButtonWidget(Widget):
    def set_enabled(self, value: bool) -> None:
        print(f"Button {'enabled' if value else 'disabled'}")

    def click(self) -> None:
        self.emit("clicked")

class TextInputWidget(Widget):
    def set_visible(self, value: bool) -> None:
        print(f"TextInput {'shown' if value else 'hidden'}")

class RegistrationDialog(DialogMediator):
    def __init__(self) -> None:
        # Build widgets with self as mediator
        self.checkbox = CheckboxWidget(self)
        self.submit_button = ButtonWidget(self)
        self.extra_info = TextInputWidget(self)

    def notify(self, sender: Widget, event: str) -> None:
        if sender is self.checkbox:
            checked = self.checkbox.is_checked()
            self.submit_button.set_enabled(checked)
            self.extra_info.set_visible(checked)

        if sender is self.submit_button and event == "clicked":
            print("Form submitted!")

dialog = RegistrationDialog()
dialog.checkbox.toggle()   # Button enabled, TextInput shown
dialog.checkbox.toggle()   # Button disabled, TextInput hidden
```

## Real-World Analogy

Air traffic control is the canonical mediator. Dozens of aircraft arrive and depart simultaneously, but pilots do not communicate directly with each other — they would talk over each other and collisions would be unavoidable. Instead, every pilot communicates only with the control tower, and the tower coordinates all movements. The tower knows the full picture and issues instructions to each aircraft in turn. Aircraft (colleagues) remain decoupled from one another; only the tower (mediator) holds the coordination logic.

## Related Patterns

- **Facade** — differs from Mediator in that a Facade merely abstracts the interface to a subsystem to make it easier to use, whereas a Mediator centralizes two-way communication between colleagues that are peers
- **Observer** — Colleagues can use the Observer pattern to communicate with the Mediator, treating the Mediator as a subscriber to their events
- **Command** — Commands can be sent through the Mediator, decoupling the sender of a command from the colleagues that execute it
