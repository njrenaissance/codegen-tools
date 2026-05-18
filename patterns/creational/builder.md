# Builder

**Category:** Creational
**Refactoring Guru:** https://refactoring.guru/design-patterns/builder

## Intent

Separate the construction of a complex object from its representation so that the same construction process can create different representations.

## When to Use

- The algorithm for creating a complex object should be independent of the parts that make up the object
- The construction process must allow different representations of the constructed object
- You need fine-grained control over the construction process (step by step, not all at once)
- A constructor would require too many parameters, making call sites unreadable

## When NOT to Use

- The object being built is simple — a constructor or factory method is cleaner
- You only ever need one representation — the Director/Builder separation is unnecessary overhead
- Construction order does not matter — plain setters or an options object suffice

## Structure

- **Builder** — abstract interface declaring steps to build parts of a product
- **ConcreteBuilder** — implements build steps and provides a method to retrieve the result
- **Director** — orchestrates the build steps in a fixed sequence; does not know the concrete builder
- **Product** — the complex object being assembled

## TypeScript Example

### ❌ Without the Pattern

```typescript
// Constructor telescoping — hard to read, easy to pass args in wrong order
const report = new Report(
  'Q4 Sales',
  true,       // includeHeader?
  false,      // includeFooter?
  true,       // includeCharts?
  'pdf',
  ['sales', 'marketing'],
  new Date('2024-01-01'),
  new Date('2024-12-31'),
);
```

### ✅ With the Pattern

```typescript
interface ReportBuilder {
  setTitle(title: string): this;
  addSection(name: string): this;
  withDateRange(from: Date, to: Date): this;
  withCharts(): this;
  withHeader(): this;
  build(): Report;
}

class PdfReportBuilder implements ReportBuilder {
  private report: Partial<Report> = { format: 'pdf', sections: [] };

  setTitle(title: string): this {
    this.report.title = title;
    return this;
  }
  addSection(name: string): this {
    this.report.sections!.push(name);
    return this;
  }
  withDateRange(from: Date, to: Date): this {
    this.report.from = from;
    this.report.to = to;
    return this;
  }
  withCharts(): this {
    this.report.includeCharts = true;
    return this;
  }
  withHeader(): this {
    this.report.includeHeader = true;
    return this;
  }
  build(): Report {
    return this.report as Report;
  }
}

// Readable, order-independent, optional steps are obvious
const report = new PdfReportBuilder()
  .setTitle('Q4 Sales')
  .addSection('sales')
  .addSection('marketing')
  .withDateRange(new Date('2024-01-01'), new Date('2024-12-31'))
  .withCharts()
  .withHeader()
  .build();
```

## Python Example

### ❌ Without the Pattern

```python
# Positional args — which bool is which?
report = Report('Q4 Sales', True, False, True, 'pdf',
                ['sales', 'marketing'],
                date(2024, 1, 1), date(2024, 12, 31))
```

### ✅ With the Pattern

```python
from dataclasses import dataclass, field
from datetime import date
from typing import Self

@dataclass
class Report:
    title: str = ''
    format: str = 'pdf'
    sections: list[str] = field(default_factory=list)
    include_charts: bool = False
    include_header: bool = False
    from_date: date | None = None
    to_date: date | None = None

class ReportBuilder:
    def __init__(self) -> None:
        self._report = Report()

    def set_title(self, title: str) -> Self:
        self._report.title = title
        return self

    def add_section(self, name: str) -> Self:
        self._report.sections.append(name)
        return self

    def with_date_range(self, from_date: date, to_date: date) -> Self:
        self._report.from_date = from_date
        self._report.to_date = to_date
        return self

    def with_charts(self) -> Self:
        self._report.include_charts = True
        return self

    def with_header(self) -> Self:
        self._report.include_header = True
        return self

    def build(self) -> Report:
        return self._report

report = (ReportBuilder()
    .set_title('Q4 Sales')
    .add_section('sales')
    .add_section('marketing')
    .with_date_range(date(2024, 1, 1), date(2024, 12, 31))
    .with_charts()
    .with_header()
    .build())
```

## Real-World Analogy

When you order a custom sandwich at a deli, the counter staff (Director) follows a sequence: bread first, then protein, then toppings, then sauce. You tell them what you want at each step. The result is your specific sandwich (Product). The same process can be used to build a vegetarian sandwich or a club sandwich — the construction process is the same, but the ingredients differ at each step.

## Related Patterns

- **Abstract Factory** — both construct complex objects; Builder does it step-by-step and returns the product at the end, Abstract Factory returns products immediately
- **Composite** — Builders often assemble Composite trees as their final product
- **Factory Method** — when the construction logic is simple enough for a single method, prefer Factory Method
