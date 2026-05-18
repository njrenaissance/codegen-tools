# Template Method

**Category:** Behavioral
**Refactoring Guru:** https://refactoring.guru/design-patterns/template-method

## Intent

Define the skeleton of an algorithm in an operation, deferring some steps to subclasses, so that subclasses can redefine certain steps of an algorithm without changing the algorithm's structure.

## When to Use

- You want to implement the invariant parts of an algorithm once and leave it up to subclasses to provide the behavior that can vary.
- You have several classes that contain nearly identical algorithms with only small differences — refactor to move common behavior into a shared superclass using Template Method to eliminate duplication.
- You want to control which parts of an algorithm subclasses can extend — the template method calls hook methods that subclasses can override, while non-hook steps remain fixed.
- You are building a framework and want to let application developers plug in behavior at specific, well-defined extension points without changing the framework's core flow.

## When NOT to Use

- The algorithm structure itself varies across subclasses — if the sequence of steps differs, Template Method forces an artificial common skeleton that doesn't fit. Use Strategy instead (composition over inheritance).
- You only have one or two concrete implementations and the abstraction adds no clarity — a simple function with optional callbacks is lighter.
- The subclass needs to override too many steps — if nearly everything is abstract, the "template" provides no value and Strategy or plain delegation is simpler.
- You want to change the algorithm at runtime — Template Method relies on inheritance which is fixed at compile time. Use Strategy for runtime algorithm swapping.

## Structure

**AbstractClass** defines abstract primitive operations that concrete subclasses define to implement steps of an algorithm. It implements a `templateMethod()` that defines the skeleton — calling primitive operations in a fixed sequence. It may also define hook operations (with default implementations) that subclasses can override if needed.

**ConcreteClass** implements the primitive operations to carry out subclass-specific steps of the algorithm. Each ConcreteClass assumes that the invariant steps in the template will be performed correctly.

The template method itself should not be overridden (declared `final` in some languages). Only the designated abstract or hook methods are meant to be customized.

## TypeScript Example

### ❌ Without the Pattern

```typescript
// Report generation with duplicated structure across every report type.
// The fetch → transform → format → deliver sequence is copy-pasted everywhere.

// Sales Report
async function generateSalesReport(startDate: Date, endDate: Date): Promise<void> {
  console.log("[SalesReport] Fetching data from sales_transactions table...");
  const rawData = [{ date: "2024-01-15", amount: 1200, rep: "Alice" }]; // simulated

  console.log("[SalesReport] Transforming: grouping by sales rep...");
  const transformed = rawData.reduce((acc: Record<string, number>, row) => {
    acc[row.rep] = (acc[row.rep] ?? 0) + row.amount;
    return acc;
  }, {});

  console.log("[SalesReport] Formatting as HTML table...");
  const html = `<table><tr><th>Rep</th><th>Total</th></tr>${
    Object.entries(transformed)
      .map(([rep, total]) => `<tr><td>${rep}</td><td>$${total}</td></tr>`)
      .join("")
  }</table>`;

  console.log("[SalesReport] Emailing to sales@company.com...");
  console.log("[SalesReport] Done. Output:", html.slice(0, 60));
}

// Inventory Report — same structure, different details, entirely duplicated
async function generateInventoryReport(): Promise<void> {
  console.log("[InventoryReport] Fetching data from inventory table...");
  const rawData = [{ sku: "WGT-001", stock: 150, warehouse: "East" }]; // simulated

  console.log("[InventoryReport] Transforming: filtering low stock...");
  const lowStock = rawData.filter(r => r.stock < 200);

  console.log("[InventoryReport] Formatting as CSV...");
  const csv = "SKU,Stock,Warehouse\n" +
    lowStock.map(r => `${r.sku},${r.stock},${r.warehouse}`).join("\n");

  console.log("[InventoryReport] Uploading to S3...");
  console.log("[InventoryReport] Done. Output:", csv.slice(0, 60));
}

// Adding a new report type means copy-pasting this structure again.
await generateSalesReport(new Date("2024-01-01"), new Date("2024-01-31"));
await generateInventoryReport();
```

### ✅ With the Pattern

```typescript
// The report generation algorithm (fetch → validate → transform → format → deliver → notify)
// is defined once in the abstract base class. Each report type only overrides what differs.

interface RawRecord {
  [key: string]: unknown;
}

interface ReportResult {
  title: string;
  output: string;
  recordCount: number;
  generatedAt: Date;
}

// AbstractClass — defines the template
abstract class ReportGenerator {
  // Template method — the invariant algorithm skeleton
  // Not intended to be overridden
  async generate(): Promise<ReportResult> {
    console.log(`\n[${this.reportName}] Starting report generation...`);

    const raw = await this.fetchData();
    console.log(`[${this.reportName}] Fetched ${raw.length} raw record(s)`);

    this.validateData(raw); // hook: default does nothing, subclass can override

    const transformed = this.transform(raw);
    console.log(`[${this.reportName}] Transformed to ${transformed.length} record(s)`);

    const output = this.format(transformed);

    await this.deliver(output);

    this.onComplete(transformed.length); // hook: default does nothing

    return {
      title: this.reportName,
      output,
      recordCount: transformed.length,
      generatedAt: new Date(),
    };
  }

  // Must be implemented by subclass
  protected abstract get reportName(): string;
  protected abstract fetchData(): Promise<RawRecord[]>;
  protected abstract transform(raw: RawRecord[]): RawRecord[];
  protected abstract format(data: RawRecord[]): string;
  protected abstract deliver(output: string): Promise<void>;

  // Hooks — optional overrides with sensible defaults
  protected validateData(raw: RawRecord[]): void {
    if (raw.length === 0) {
      console.warn(`[${this.reportName}] Warning: no data found for report.`);
    }
  }

  protected onComplete(recordCount: number): void {
    // Default: do nothing. Subclass can override for notifications, metrics, etc.
  }
}

// ConcreteClass: Sales Report
class SalesReport extends ReportGenerator {
  constructor(
    private readonly startDate: Date,
    private readonly endDate: Date
  ) {
    super();
  }

  protected get reportName() { return "SalesReport"; }

  protected async fetchData(): Promise<RawRecord[]> {
    console.log(`[${this.reportName}] Querying sales_transactions...`);
    return [
      { date: "2024-01-10", amount: 1200, rep: "Alice" },
      { date: "2024-01-14", amount: 850,  rep: "Bob"   },
      { date: "2024-01-20", amount: 2100, rep: "Alice" },
    ];
  }

  protected transform(raw: RawRecord[]): RawRecord[] {
    const grouped: Record<string, number> = {};
    for (const row of raw) {
      const rep = row.rep as string;
      grouped[rep] = (grouped[rep] ?? 0) + (row.amount as number);
    }
    return Object.entries(grouped).map(([rep, total]) => ({ rep, total }));
  }

  protected format(data: RawRecord[]): string {
    const rows = data
      .map(r => `  <tr><td>${r.rep}</td><td>$${r.total}</td></tr>`)
      .join("\n");
    return `<table>\n  <tr><th>Sales Rep</th><th>Total</th></tr>\n${rows}\n</table>`;
  }

  protected async deliver(output: string): Promise<void> {
    console.log(`[${this.reportName}] Emailing report to sales-team@company.com`);
  }

  // Override hook to send Slack notification on completion
  protected onComplete(recordCount: number): void {
    console.log(`[${this.reportName}] Slack: report with ${recordCount} entries sent to #sales-reports`);
  }
}

// ConcreteClass: Inventory Report
class InventoryReport extends ReportGenerator {
  protected get reportName() { return "InventoryReport"; }

  protected async fetchData(): Promise<RawRecord[]> {
    console.log(`[${this.reportName}] Querying inventory table...`);
    return [
      { sku: "WGT-001", stock: 150,  warehouse: "East"  },
      { sku: "GDG-002", stock: 12,   warehouse: "West"  },
      { sku: "DOO-003", stock: 400,  warehouse: "North" },
      { sku: "THG-004", stock: 5,    warehouse: "East"  },
    ];
  }

  // Override validate hook — inventory needs stricter checks
  protected validateData(raw: RawRecord[]): void {
    super.validateData(raw);
    const invalid = raw.filter(r => typeof r.stock !== "number" || (r.stock as number) < 0);
    if (invalid.length > 0) {
      throw new Error(`Invalid stock values in ${invalid.length} record(s)`);
    }
  }

  protected transform(raw: RawRecord[]): RawRecord[] {
    return raw.filter(r => (r.stock as number) < 50); // only low-stock items
  }

  protected format(data: RawRecord[]): string {
    const header = "SKU,Stock,Warehouse";
    const rows = data.map(r => `${r.sku},${r.stock},${r.warehouse}`).join("\n");
    return `${header}\n${rows}`;
  }

  protected async deliver(output: string): Promise<void> {
    console.log(`[${this.reportName}] Uploading CSV to s3://reports-bucket/inventory/`);
    console.log(`[${this.reportName}] Content preview: ${output.slice(0, 80)}...`);
  }
}

// ConcreteClass: Audit Report — minimal overrides, uses inherited hooks as-is
class AuditReport extends ReportGenerator {
  protected get reportName() { return "AuditReport"; }

  protected async fetchData(): Promise<RawRecord[]> {
    return [
      { user: "alice", action: "DELETE", resource: "/api/users/42", ts: "2024-01-15T10:00Z" },
      { user: "bob",   action: "PATCH",  resource: "/api/orders/7",  ts: "2024-01-15T11:30Z" },
    ];
  }

  protected transform(raw: RawRecord[]): RawRecord[] {
    return raw; // no transformation needed
  }

  protected format(data: RawRecord[]): string {
    return data.map(r => `${r.ts} | ${r.user} | ${r.action} | ${r.resource}`).join("\n");
  }

  protected async deliver(output: string): Promise<void> {
    console.log(`[${this.reportName}] Archiving to compliance audit log...`);
  }
}

// Usage — identical interface for all report types
const reports: ReportGenerator[] = [
  new SalesReport(new Date("2024-01-01"), new Date("2024-01-31")),
  new InventoryReport(),
  new AuditReport(),
];

for (const report of reports) {
  const result = await report.generate();
  console.log(`Result: "${result.title}" — ${result.recordCount} records\n`);
}
```

## Python Example

### ❌ Without the Pattern

```python
# Data import pipeline with copy-pasted structure for CSV and JSON imports.

from pathlib import Path

def import_csv(filepath: str) -> None:
    print(f"[CSV] Opening file: {filepath}")
    # Simulated content
    lines = ["id,name,email", "1,Alice,alice@example.com", "2,Bob,bob@example.com"]
    headers, *rows = [l.split(",") for l in lines]
    print(f"[CSV] Parsed {len(rows)} records")
    # Validate
    for row in rows:
        if len(row) != len(headers):
            raise ValueError("Column mismatch")
    print("[CSV] Validation passed")
    # Transform
    records = [dict(zip(headers, row)) for row in rows]
    # Load
    print(f"[CSV] Inserting {len(records)} records into DB: {records}")

def import_json(filepath: str) -> None:
    print(f"[JSON] Opening file: {filepath}")
    data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]  # simulated
    print(f"[JSON] Parsed {len(data)} records")
    # Validate
    for item in data:
        if "id" not in item or "name" not in item:
            raise ValueError("Missing required fields")
    print("[JSON] Validation passed")
    # Transform
    records = [{k: str(v) for k, v in item.items()} for item in data]
    # Load
    print(f"[JSON] Inserting {len(records)} records into DB: {records}")

# Same 4-step structure duplicated — add XML import? Copy again.
import_csv("users.csv")
import_json("users.json")
```

### ✅ With the Pattern

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

Record = dict[str, Any]

@dataclass
class ImportResult:
    source_format: str
    records_imported: int
    warnings: list[str] = field(default_factory=list)

# AbstractClass
class DataImporter(ABC):
    """
    Template method: open → parse → validate → transform → load → finalize.
    Subclasses implement parse(), validate(), and transform().
    """

    def run(self, source: str) -> ImportResult:
        """Template method — invariant import pipeline."""
        print(f"\n[{self.format_name}] Starting import from: {source}")

        raw = self._open(source)
        records = self.parse(raw)
        print(f"[{self.format_name}] Parsed {len(records)} record(s)")

        warnings = self.validate(records)
        for w in warnings:
            print(f"[{self.format_name}] Warning: {w}")

        transformed = self.transform(records)
        self._load(transformed)
        self.on_success(len(transformed))  # hook

        return ImportResult(
            source_format=self.format_name,
            records_imported=len(transformed),
            warnings=warnings,
        )

    # Invariant steps — defined here, not overridden
    def _open(self, source: str) -> str:
        print(f"[{self.format_name}] Opening source...")
        return f"SIMULATED_CONTENT({source})"

    def _load(self, records: list[Record]) -> None:
        print(f"[{self.format_name}] Loading {len(records)} record(s) into database...")
        for rec in records:
            print(f"  INSERT: {rec}")

    # Abstract primitive operations — subclass must implement
    @property
    @abstractmethod
    def format_name(self) -> str: ...

    @abstractmethod
    def parse(self, raw_content: str) -> list[Record]: ...

    @abstractmethod
    def validate(self, records: list[Record]) -> list[str]:
        """Return list of warning strings (empty = no warnings)."""
        ...

    @abstractmethod
    def transform(self, records: list[Record]) -> list[Record]: ...

    # Hook — optional override
    def on_success(self, count: int) -> None:
        print(f"[{self.format_name}] Import complete: {count} record(s) loaded.")

# ConcreteClass: CSV Importer
class CsvImporter(DataImporter):
    format_name = "CSV"

    def parse(self, raw_content: str) -> list[Record]:
        # Simulated: parse CSV lines
        lines = [
            "id,name,email,age",
            "1,Alice,alice@example.com,30",
            "2,Bob,bob@example.com,25",
            "3,Carol,carol@example.com,-1",  # intentionally bad age
        ]
        headers, *rows = [l.split(",") for l in lines]
        return [dict(zip(headers, row)) for row in rows]

    def validate(self, records: list[Record]) -> list[str]:
        warnings = []
        for rec in records:
            if int(rec.get("age", 0)) < 0:
                warnings.append(f"Record {rec['id']}: negative age ({rec['age']})")
        return warnings

    def transform(self, records: list[Record]) -> list[Record]:
        return [
            {
                "id": int(rec["id"]),
                "name": rec["name"].strip(),
                "email": rec["email"].strip().lower(),
                "age": max(0, int(rec["age"])),
            }
            for rec in records
        ]

    def on_success(self, count: int) -> None:
        super().on_success(count)
        print(f"[{self.format_name}] Sending import summary to data-team@company.com")

# ConcreteClass: JSON Importer
class JsonImporter(DataImporter):
    format_name = "JSON"

    def parse(self, raw_content: str) -> list[Record]:
        # Simulated JSON payload
        return [
            {"id": "u10", "full_name": "Dave",  "contact": {"email": "dave@example.com"}},
            {"id": "u11", "full_name": "Eve",   "contact": {"email": "eve@example.com"}},
            {"id": "u12", "full_name": "",       "contact": {}},  # missing data
        ]

    def validate(self, records: list[Record]) -> list[str]:
        warnings = []
        for rec in records:
            if not rec.get("full_name"):
                warnings.append(f"Record {rec['id']}: missing full_name")
            if not rec.get("contact", {}).get("email"):
                warnings.append(f"Record {rec['id']}: missing email")
        return warnings

    def transform(self, records: list[Record]) -> list[Record]:
        # Flatten nested contact, skip records missing required fields
        result = []
        for rec in records:
            email = rec.get("contact", {}).get("email", "")
            name = rec.get("full_name", "").strip()
            if name and email:
                result.append({"id": rec["id"], "name": name, "email": email})
        return result

# Usage — identical interface regardless of format
importers: list[DataImporter] = [CsvImporter(), JsonImporter()]

for importer in importers:
    result = importer.run("data/users")
    print(f"Summary: {result}\n")
```

## Real-World Analogy

House construction follows a Template Method: every house goes through the same phases in the same sequence — lay the foundation, erect the structural frame, install plumbing and electrical, fit the walls and roofing, paint and decorate. The sequence is fixed (the template). But the details vary: a log cabin uses timber framing while a concrete house uses reinforced slabs; interior decoration can be Victorian or minimalist. The construction company (abstract class) defines the invariant build order; each specific house type (concrete subclass) fills in the steps that are unique to it. No step can be reordered — you can't decorate before the frame is up — but each step has latitude in how it is executed.

## Related Patterns

- **Strategy** — both define a family of algorithms, but Template Method uses inheritance to vary part of an algorithm while keeping the skeleton fixed in the superclass; Strategy uses composition to replace the entire algorithm at runtime. Prefer Strategy when you need runtime flexibility; prefer Template Method when the invariant skeleton is the dominant concern.
- **Factory Method** — often called by template methods. Factory Method is a specialization of Template Method: the "create object" step of a template is a factory method that subclasses override to produce different product types.
- **Hook methods** — template methods often call hook operations (with default do-nothing implementations) alongside abstract operations. Hooks give subclasses finer-grained extension points without making them implement everything.
