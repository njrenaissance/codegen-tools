# Composite

**Category:** Structural
**Refactoring Guru:** https://refactoring.guru/design-patterns/composite

## Intent

Compose objects into tree structures to represent part-whole hierarchies, letting clients treat individual objects and compositions of objects uniformly.

## When to Use

- You want to represent part-whole hierarchies of objects
- You want clients to be able to ignore the difference between compositions of objects and individual objects — clients will treat all objects in the composite structure uniformly
- The structure can have any depth of nesting (e.g., a file system with arbitrarily nested folders)
- Operations on composites should recursively propagate to their children without the client needing to know whether it is dealing with a leaf or a branch

## When NOT to Use

- When the hierarchy is fixed and shallow — the extra abstraction adds complexity without benefit
- When leaf nodes and composite nodes have very different interfaces that cannot be cleanly unified — forcing a common interface causes awkward no-op implementations on leaves
- When type safety is critical and you need to distinguish at compile time between leaves and composites (the pattern intentionally blurs this distinction)

## Structure

- **Component** — Declares the interface for objects in the composition, including default behavior for the interface common to all classes. May declare an interface for accessing and managing child components.
- **Leaf** — Represents leaf objects in the composition (has no children). Defines behavior for primitive objects in the composition.
- **Composite** — Defines behavior for components having children. Stores child components and implements child-related operations in the Component interface. Delegates work to its children and combines the results.
- **Client** — Manipulates objects in the composition through the Component interface.

## TypeScript Example

### Without the Pattern

```typescript
// Without Composite, the client must check types and handle
// files vs folders separately — the logic explodes with nesting.

class File {
  constructor(public name: string, public size: number) {}
}

class Folder {
  constructor(
    public name: string,
    public files: File[],
    public subFolders: Folder[]
  ) {}
}

// Client code has to know the structure deeply
function getTotalSize(folder: Folder): number {
  let total = 0;
  for (const file of folder.files) {
    total += file.size;
  }
  for (const sub of folder.subFolders) {
    total += getTotalSize(sub); // recursive, but only works for Folder type
  }
  return total;
}

// Cannot call getTotalSize on a single File — different types, different treatment
const file = new File("readme.txt", 1024);
const folder = new Folder("docs", [file], []);
console.log(getTotalSize(folder)); // 1024 — but cannot unify with a single File
```

### With the Pattern

```typescript
// Component interface — uniform treatment for both File and Folder
interface FileSystemNode {
  name: string;
  getSize(): number;
  print(indent?: string): void;
}

// Leaf
class File implements FileSystemNode {
  constructor(public name: string, private size: number) {}

  getSize(): number {
    return this.size;
  }

  print(indent = ""): void {
    console.log(`${indent}- ${this.name} (${this.size} bytes)`);
  }
}

// Composite
class Folder implements FileSystemNode {
  private children: FileSystemNode[] = [];

  constructor(public name: string) {}

  add(node: FileSystemNode): void {
    this.children.push(node);
  }

  remove(node: FileSystemNode): void {
    this.children = this.children.filter((c) => c !== node);
  }

  getSize(): number {
    return this.children.reduce((sum, child) => sum + child.getSize(), 0);
  }

  print(indent = ""): void {
    console.log(`${indent}+ ${this.name}/`);
    this.children.forEach((c) => c.print(indent + "  "));
  }
}

// Client treats FileSystemNode uniformly — no type checking needed
const root = new Folder("root");
const docs = new Folder("docs");
docs.add(new File("readme.txt", 1024));
docs.add(new File("design.pdf", 204800));
root.add(docs);
root.add(new File("config.json", 512));

root.print();
// + root/
//   + docs/
//     - readme.txt (1024 bytes)
//     - design.pdf (204800 bytes)
//   - config.json (512 bytes)

console.log(root.getSize()); // 206336 — works the same on a single File too
const singleFile: FileSystemNode = new File("solo.txt", 100);
console.log(singleFile.getSize()); // 100 — uniform interface
```

## Python Example

### Without the Pattern

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class File:
    name: str
    size: int

@dataclass
class Folder:
    name: str
    files: List[File] = field(default_factory=list)
    sub_folders: List["Folder"] = field(default_factory=list)

def get_total_size(folder: Folder) -> int:
    total = sum(f.size for f in folder.files)
    for sub in folder.sub_folders:
        total += get_total_size(sub)
    return total

# Cannot unify File and Folder — the client always needs to know the type
file = File("readme.txt", 1024)
folder = Folder("docs", files=[file])
print(get_total_size(folder))  # 1024 — but cannot call on a bare File
```

### With the Pattern

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

# Component
class FileSystemNode(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def get_size(self) -> int: ...

    @abstractmethod
    def print(self, indent: str = "") -> None: ...

# Leaf
class File(FileSystemNode):
    def __init__(self, name: str, size: int) -> None:
        super().__init__(name)
        self._size = size

    def get_size(self) -> int:
        return self._size

    def print(self, indent: str = "") -> None:
        print(f"{indent}- {self.name} ({self._size} bytes)")

# Composite
class Folder(FileSystemNode):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._children: List[FileSystemNode] = []

    def add(self, node: FileSystemNode) -> None:
        self._children.append(node)

    def remove(self, node: FileSystemNode) -> None:
        self._children.remove(node)

    def get_size(self) -> int:
        return sum(child.get_size() for child in self._children)

    def print(self, indent: str = "") -> None:
        print(f"{indent}+ {self.name}/")
        for child in self._children:
            child.print(indent + "  ")

# Client — uniform treatment
root = Folder("root")
docs = Folder("docs")
docs.add(File("readme.txt", 1024))
docs.add(File("design.pdf", 204800))
root.add(docs)
root.add(File("config.json", 512))

root.print()
print(root.get_size())  # 206336

single_file: FileSystemNode = File("solo.txt", 100)
print(single_file.get_size())  # 100 — same interface
```

## Real-World Analogy

Think of a corporate org chart. A team lead has direct reports, and each direct report may themselves manage sub-teams of any depth. When HR wants to count total headcount under a given manager, they do not need to know how deeply nested the hierarchy is — they simply ask the manager "how many people report to you?" and each manager recursively asks their own direct reports. A single individual contributor answers "1". A manager answers the sum of all their reports' answers. The client (HR system) treats managers and individual contributors through the same "headcount" interface.

## Related Patterns

- **Decorator** — often used with Composite; a Decorator is like a Composite with only one child component, and adds responsibilities rather than aggregating results
- **Flyweight** — lets you share components so they can have many parents; works well when leaf nodes are memory-intensive
- **Iterator** — can be used to traverse Composite trees
- **Visitor** — can apply an operation across an entire Composite tree without changing the component classes
- **Chain of Responsibility** — uses tree-like structures; parent components can act as successors
