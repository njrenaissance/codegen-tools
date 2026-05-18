# Abstract Factory

**Category:** Creational
**Refactoring Guru:** https://refactoring.guru/design-patterns/abstract-factory

## Intent

Provide an interface for creating families of related or dependent objects without specifying their concrete classes.

## When to Use

- A system should be independent of how its products are created, composed, and represented
- A system should be configured with one of multiple families of products
- A family of related product objects is designed to be used together, and you need to enforce that constraint
- You want to reveal only interfaces of a product library, not their implementations

## When NOT to Use

- You only need to create one type of object (use Factory Method instead)
- The product families are unlikely to change or extend — the pattern makes adding new product types costly (requires changing the abstract factory interface and all concrete factories)
- You have only one concrete factory — the abstraction adds complexity with no benefit

## Structure

- **AbstractFactory** — declares create methods for each product type
- **ConcreteFactory** — implements create methods to produce a family of products
- **AbstractProduct** — declares the interface for each product type
- **ConcreteProduct** — implements AbstractProduct; built by the matching ConcreteFactory
- **Client** — uses only AbstractFactory and AbstractProduct interfaces

## TypeScript Example

### ❌ Without the Pattern

```typescript
type Provider = 'aws' | 'azure';

function createStorage(provider: Provider) {
  if (provider === 'aws') {
    return new S3Storage();        // hard dependency on concrete classes
  }
  return new AzureBlobStorage();   // client must know every concrete class
}

function createQueue(provider: Provider) {
  if (provider === 'aws') {
    return new SQSQueue();
  }
  return new AzureServiceBusQueue(); // must be kept in sync with createStorage
}

// Nothing prevents mixing AWS storage with Azure queue
const storage = createStorage('aws');
const queue = createQueue('azure'); // mismatched family — runtime surprise
```

### ✅ With the Pattern

```typescript
interface Storage {
  upload(key: string, data: Buffer): Promise<void>;
  download(key: string): Promise<Buffer>;
}

interface Queue {
  publish(message: string): Promise<void>;
  consume(): AsyncIterable<string>;
}

interface CloudFactory {
  createStorage(): Storage;
  createQueue(): Queue;
}

class AwsFactory implements CloudFactory {
  createStorage(): Storage { return new S3Storage(); }
  createQueue(): Queue     { return new SQSQueue(); }
}

class AzureFactory implements CloudFactory {
  createStorage(): Storage { return new AzureBlobStorage(); }
  createQueue(): Queue     { return new AzureServiceBusQueue(); }
}

// Client works only with interfaces — family is always consistent
class FileProcessor {
  constructor(private factory: CloudFactory) {}

  async process(key: string) {
    const storage = this.factory.createStorage();
    const queue   = this.factory.createQueue();
    const data    = await storage.download(key);
    await queue.publish(`processed:${key}`);
  }
}

const processor = new FileProcessor(new AwsFactory());
// Swap to Azure: new FileProcessor(new AzureFactory())
```

## Python Example

### ❌ Without the Pattern

```python
def create_storage(provider: str):
    if provider == 'aws':
        return S3Storage()
    return AzureBlobStorage()

def create_queue(provider: str):
    if provider == 'aws':
        return SQSQueue()
    return AzureServiceBusQueue()

# Nothing prevents mixing families
storage = create_storage('aws')
queue = create_queue('azure')  # mismatched family
```

### ✅ With the Pattern

```python
from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def upload(self, key: str, data: bytes) -> None: ...
    @abstractmethod
    def download(self, key: str) -> bytes: ...

class Queue(ABC):
    @abstractmethod
    def publish(self, message: str) -> None: ...

class CloudFactory(ABC):
    @abstractmethod
    def create_storage(self) -> Storage: ...
    @abstractmethod
    def create_queue(self) -> Queue: ...

class AwsFactory(CloudFactory):
    def create_storage(self) -> Storage: return S3Storage()
    def create_queue(self) -> Queue:     return SQSQueue()

class AzureFactory(CloudFactory):
    def create_storage(self) -> Storage: return AzureBlobStorage()
    def create_queue(self) -> Queue:     return AzureServiceBusQueue()

class FileProcessor:
    def __init__(self, factory: CloudFactory):
        self.storage = factory.create_storage()
        self.queue   = factory.create_queue()

    def process(self, key: str) -> None:
        data = self.storage.download(key)
        self.queue.publish(f'processed:{key}')

processor = FileProcessor(AwsFactory())
# Swap: FileProcessor(AzureFactory())
```

## Real-World Analogy

A furniture manufacturer produces sofas, chairs, and coffee tables in matching styles — Victorian, Modern, or Art Deco. When you order a "Modern living room set," the factory produces all three pieces in the same style. You don't pick individual pieces from different factories because the constraint is that they must match. The Abstract Factory is like the order desk: you specify the family (Modern), and everything that comes out is consistent.

## Related Patterns

- **Factory Method** — Abstract Factory is often implemented using factory methods; Factory Method handles one product, Abstract Factory handles a family
- **Singleton** — Concrete factories are often singletons (only one factory instance is needed per family)
- **Prototype** — Can be used to implement an Abstract Factory when families are defined by cloning prototypes
