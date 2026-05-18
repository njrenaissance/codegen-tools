# /architecture-check

Verify that a file respects Clean Architecture layer boundaries (the Dependency Rule).

**Usage:**

```bash
/architecture-check
/architecture-check src/lib/orderService.ts
/architecture-check src/app/api/orders/route.ts
```

## What to do

1. **Identify the target file**
   - Use the argument if provided, else the currently open file

2. **Read the architecture rules**
   - Load `~/engineering-standards/CLEAN-ARCHITECTURE.md`
   - Key rule: dependencies must point **inward only**
     ```
     Entities ← Use Cases ← Interface Adapters ← Frameworks & Drivers
     ```

3. **Determine the file's layer** from its path

   | Path pattern | Layer | May import from |
   |---|---|---|
   | `domain/`, `entities/`, `models/` (no DB) | Entity | Nothing outside itself |
   | `lib/`, `use-cases/`, `usecases/`, `application/` | Use Case | Entities only (via interfaces) |
   | `controllers/`, `routes/`, `api/`, `presenters/` | Interface Adapter | Use Cases, Entities |
   | `services/` (infra), `adapters/`, `repositories/`, `providers/` | Framework/Driver | Anything |
   | `app/` (Next.js pages/routes) | Framework/Driver | Anything |

   If the layer is ambiguous, read the first 20 lines of the file to determine from context.

4. **Grep all imports** in the file

5. **Classify each import**

   For each import, determine which layer it comes from and whether the dependency direction is valid:

   | Import | Violation? |
   |---|---|
   | Framework import (`next/`, `express`, `prisma`, `mongoose`) in Entity or Use Case | ✅ VIOLATION |
   | Use Case importing from an Interface Adapter | ✅ VIOLATION |
   | Entity importing from a Use Case | ✅ VIOLATION |
   | Interface Adapter importing from Framework is fine | ✅ OK |
   | Use Case importing an interface defined in Use Case layer | ✅ OK |

6. **Output format**

   ```
   ## Architecture Check: src/lib/orderService.ts
   **Detected layer:** Use Case

   ### ✅ Clean imports (3)
   - `../domain/order` — Entity (inward ✓)
   - `../domain/interfaces/IOrderRepository` — Entity interface (inward ✓)
   - `../domain/interfaces/IPaymentGateway` — Entity interface (inward ✓)

   ### 🔴 Violations (2)

   **Line 3** — `import { prisma } from '@/lib/db'`
   Layer: Framework/Driver → imported into Use Case
   Fix: Define `IOrderRepository` interface in the Use Case layer.
        Create a `PrismaOrderRepository` in `repositories/` that implements it.
        Inject it via constructor: `constructor(private repo: IOrderRepository)`

   **Line 7** — `import { NextResponse } from 'next/server'`
   Layer: Framework/Driver → imported into Use Case
   Fix: Return a plain domain object `{ success: boolean, orderId: string }`.
        Let the route handler in `app/api/orders/route.ts` wrap it in NextResponse.
   ```

7. **After the report**
   - If violations exist: "Would you like me to introduce the necessary port interfaces and fix these violations?"
   - If clean: "This file respects all layer boundaries. ✅"
