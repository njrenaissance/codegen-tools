# Singleton

**Category:** Creational
**Refactoring Guru:** https://refactoring.guru/design-patterns/singleton

## Intent

Ensure a class has only one instance, and provide a global point of access to it.

## When to Use

- There must be exactly one instance of a class, and it must be accessible from a well-known access point
- The sole instance should be extensible by subclassing, and clients should be able to use an extended instance without modifying their code
- You need stricter control over global variables (the Singleton guarantees that no one can replace it)
- A shared resource (e.g., a configuration object, connection pool, or logger) must be consistent across the entire application

## When NOT to Use

- When unit testing is important and you cannot easily inject a substitute — Singletons make mocking and isolation very difficult
- When the "single instance" constraint is really just a convention that could be enforced at a higher level (e.g., dependency injection container)
- When your application is multi-threaded and you have not accounted for race conditions during instance creation
- When the class manages mutable state that different subsystems may inadvertently share, causing hidden coupling

## Structure

**Singleton** is the only participant. It defines a static `Instance()` operation (or getter) that lets clients access the unique instance, and it is responsible for creating its own unique instance. The constructor is private or protected so that no external code can call `new` directly.

## TypeScript Example

### Without the Pattern

```typescript
// Every module that needs configuration creates its own object,
// leading to inconsistent state and wasted memory.

class AppConfig {
  public dbHost: string;
  public dbPort: number;
  public featureFlags: Record<string, boolean>;

  constructor() {
    // Imagine this reads from env vars or a file
    this.dbHost = process.env.DB_HOST ?? "localhost";
    this.dbPort = Number(process.env.DB_PORT ?? 5432);
    this.featureFlags = { darkMode: true, betaFeatures: false };
    console.log("AppConfig constructed"); // fires multiple times
  }
}

// userService.ts
const configA = new AppConfig();
configA.featureFlags.darkMode = false; // mutates only this copy

// orderService.ts
const configB = new AppConfig(); // separate object — mutation above is lost
console.log(configB.featureFlags.darkMode); // true — inconsistent!
```

### With the Pattern

```typescript
class AppConfig {
  private static instance: AppConfig | null = null;

  public dbHost: string;
  public dbPort: number;
  public featureFlags: Record<string, boolean>;

  // Private constructor prevents direct instantiation
  private constructor() {
    this.dbHost = process.env.DB_HOST ?? "localhost";
    this.dbPort = Number(process.env.DB_PORT ?? 5432);
    this.featureFlags = { darkMode: true, betaFeatures: false };
    console.log("AppConfig constructed"); // fires exactly once
  }

  public static getInstance(): AppConfig {
    if (AppConfig.instance === null) {
      AppConfig.instance = new AppConfig();
    }
    return AppConfig.instance;
  }
}

// userService.ts
const configA = AppConfig.getInstance();
configA.featureFlags.darkMode = false;

// orderService.ts
const configB = AppConfig.getInstance(); // same object
console.log(configB.featureFlags.darkMode); // false — consistent!

console.log(configA === configB); // true
```

## Python Example

### Without the Pattern

```python
import os

class AppConfig:
    def __init__(self):
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_port = int(os.getenv("DB_PORT", 5432))
        self.feature_flags = {"dark_mode": True, "beta_features": False}
        print("AppConfig constructed")  # fires multiple times

# user_service.py
config_a = AppConfig()
config_a.feature_flags["dark_mode"] = False  # mutates only this copy

# order_service.py
config_b = AppConfig()  # completely separate object
print(config_b.feature_flags["dark_mode"])  # True — inconsistent!
```

### With the Pattern

```python
import os
from threading import Lock

class AppConfig:
    _instance: "AppConfig | None" = None
    _lock: Lock = Lock()

    def __new__(cls) -> "AppConfig":
        if cls._instance is None:
            with cls._lock:  # thread-safe double-checked locking
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_port = int(os.getenv("DB_PORT", 5432))
        self.feature_flags = {"dark_mode": True, "beta_features": False}
        self._initialized = True
        print("AppConfig constructed")  # fires exactly once

# user_service.py
config_a = AppConfig()
config_a.feature_flags["dark_mode"] = False

# order_service.py
config_b = AppConfig()
print(config_b.feature_flags["dark_mode"])  # False — consistent!
print(config_a is config_b)  # True
```

## Real-World Analogy

A country has exactly one official government registry of citizens. No matter which government department queries citizen records — the tax office, the immigration bureau, or the department of motor vehicles — they all consult the same single registry. It would be chaos if each department maintained its own separate copy of the registry, since updates in one place would not be reflected elsewhere. The Singleton pattern enforces this "one authoritative source" constraint in software.

## Related Patterns

- **Abstract Factory** — Abstract Factory classes are often implemented as Singletons, since only one factory is needed per application
- **Builder** — Builders are sometimes made Singletons when the construction process is stateless
- **Facade** — A Facade object is often a Singleton because only one Facade object is required
- **State** — State objects are sometimes Singletons when states carry no instance-specific data
