# Proxy

**Category:** Structural
**Refactoring Guru:** https://refactoring.guru/design-patterns/proxy

## Intent

Provide a surrogate or placeholder for another object to control access to it.

## When to Use

- **Remote Proxy** — provides a local representative for an object in a different address space (e.g., a network stub that marshals calls to a remote service)
- **Virtual Proxy** — creates expensive objects on demand; the proxy defers creation of the real subject until it is truly needed (lazy initialization)
- **Protection Proxy** — controls access to the original object; useful when different clients should have different levels of access rights
- **Smart Reference** — replaces a bare pointer and performs additional actions when an object is accessed, such as reference counting, loading persistent objects on first access, or locking an object before it is accessed to ensure exclusive access
- You want to add cross-cutting concerns (logging, caching, metrics, authorization) around an existing object without modifying it

## When NOT to Use

- When the added indirection noticeably hurts performance and no cross-cutting concern justifies it
- When the real subject is simple enough that a thin wrapper adds more maintenance overhead than value
- When you control the subject's source code — consider simply adding the behavior there, or using a decorator if composability matters more than access control

## Structure

- **Subject** — Defines the common interface for RealSubject and Proxy so that a Proxy can be used anywhere a RealSubject is expected.
- **RealSubject** — Defines the real object that the proxy represents.
- **Proxy** — Maintains a reference to the RealSubject and implements the Subject interface. Controls access to the RealSubject and may be responsible for its creation and deletion. Performs additional duties (lazy init, logging, access control, caching) before or after forwarding a request.

## TypeScript Example

### Without the Pattern

```typescript
// Without a proxy, every call site must manually handle caching,
// authorization, and logging — duplicated across the codebase.

class UserService {
  async getUserById(id: string): Promise<{ id: string; name: string }> {
    console.log(`[DB] Fetching user ${id}`); // simulate DB hit
    return { id, name: "Alice" };
  }
}

// Call site A — manually caches
const cacheA: Map<string, { id: string; name: string }> = new Map();
const svc = new UserService();

async function getUser(id: string) {
  if (!cacheA.has(id)) {
    cacheA.set(id, await svc.getUserById(id));
  }
  return cacheA.get(id)!;
}

// Call site B — also manually caches (duplicate)
const cacheB: Map<string, { id: string; name: string }> = new Map();
// ... same pattern repeated
```

### With the Pattern

```typescript
interface IUserService {
  getUserById(id: string): Promise<{ id: string; name: string }>;
}

// RealSubject
class UserService implements IUserService {
  async getUserById(id: string): Promise<{ id: string; name: string }> {
    console.log(`[DB] Fetching user ${id}`);
    return { id, name: "Alice" };
  }
}

// Proxy — adds caching and logging transparently
class CachingUserServiceProxy implements IUserService {
  private cache = new Map<string, { id: string; name: string }>();

  constructor(private realService: IUserService) {}

  async getUserById(id: string): Promise<{ id: string; name: string }> {
    if (this.cache.has(id)) {
      console.log(`[CACHE] Cache hit for user ${id}`);
      return this.cache.get(id)!;
    }

    console.log(`[CACHE] Cache miss for user ${id} — delegating to real service`);
    const user = await this.realService.getUserById(id);
    this.cache.set(id, user);
    return user;
  }
}

// Protection Proxy example
class AuthorizedUserServiceProxy implements IUserService {
  constructor(
    private realService: IUserService,
    private currentUserRole: string
  ) {}

  async getUserById(id: string): Promise<{ id: string; name: string }> {
    if (this.currentUserRole !== "admin" && this.currentUserRole !== "viewer") {
      throw new Error("Access denied: insufficient permissions");
    }
    return this.realService.getUserById(id);
  }
}

// Client code — works with IUserService; never knows about caching or auth
const real = new UserService();
const cached = new CachingUserServiceProxy(real);
const guarded = new AuthorizedUserServiceProxy(cached, "admin");

async function main() {
  await guarded.getUserById("42"); // [DB] Fetching user 42
  await guarded.getUserById("42"); // [CACHE] Cache hit for user 42
}
main();
```

## Python Example

### Without the Pattern

```python
import asyncio

class UserService:
    async def get_user_by_id(self, user_id: str) -> dict:
        print(f"[DB] Fetching user {user_id}")
        return {"id": user_id, "name": "Alice"}

# Every call site duplicates caching logic
_cache: dict[str, dict] = {}
svc = UserService()

async def get_user(user_id: str) -> dict:
    if user_id not in _cache:
        _cache[user_id] = await svc.get_user_by_id(user_id)
    return _cache[user_id]
```

### With the Pattern

```python
from __future__ import annotations
import asyncio
from abc import ABC, abstractmethod
from typing import Optional

class IUserService(ABC):
    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> dict: ...

# RealSubject
class UserService(IUserService):
    async def get_user_by_id(self, user_id: str) -> dict:
        print(f"[DB] Fetching user {user_id}")
        return {"id": user_id, "name": "Alice"}

# Caching Proxy
class CachingUserServiceProxy(IUserService):
    def __init__(self, real_service: IUserService) -> None:
        self._real = real_service
        self._cache: dict[str, dict] = {}

    async def get_user_by_id(self, user_id: str) -> dict:
        if user_id in self._cache:
            print(f"[CACHE] Hit for user {user_id}")
            return self._cache[user_id]
        print(f"[CACHE] Miss for user {user_id}")
        user = await self._real.get_user_by_id(user_id)
        self._cache[user_id] = user
        return user

# Protection Proxy
class AuthorizedUserServiceProxy(IUserService):
    def __init__(self, real_service: IUserService, role: str) -> None:
        self._real = real_service
        self._role = role

    async def get_user_by_id(self, user_id: str) -> dict:
        if self._role not in ("admin", "viewer"):
            raise PermissionError("Access denied: insufficient permissions")
        return await self._real.get_user_by_id(user_id)

# Client — depends only on IUserService
async def main() -> None:
    real = UserService()
    cached = CachingUserServiceProxy(real)
    guarded = AuthorizedUserServiceProxy(cached, role="admin")

    await guarded.get_user_by_id("42")  # [DB] Fetching user 42
    await guarded.get_user_by_id("42")  # [CACHE] Hit for user 42

asyncio.run(main())
```

## Real-World Analogy

A corporate receptionist acts as a proxy for the executives behind them. Visitors (clients) do not walk directly into the CEO's office — they speak to the receptionist first. The receptionist may check credentials (protection proxy), look up whether the visitor has been seen before (caching proxy), or forward calls to the CEO's assistant who is physically located elsewhere (remote proxy). The visitor's interface with "the executive" remains the same regardless of how many layers of delegation occur.

## Related Patterns

- **Adapter** — provides a different interface to the subject; a Proxy provides the same interface but controls or augments access
- **Decorator** — adds responsibilities to an object without changing its interface, similar to Proxy, but focused on feature addition rather than access control; Proxy often manages the lifecycle of the subject while Decorator does not
- **Facade** — simplifies the interface to a complex subsystem; a Proxy does not simplify — it uses the same interface as the subject
