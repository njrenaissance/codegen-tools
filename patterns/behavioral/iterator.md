# Iterator

**Category:** Behavioral
**Refactoring Guru:** https://refactoring.guru/design-patterns/iterator

## Intent

Provide a way to access the elements of an aggregate object sequentially without exposing its underlying representation.

## When to Use

- You want to access a collection's contents without exposing its internal structure (array, tree, hash table, etc.)
- You want to support multiple simultaneous traversals of aggregate objects — each iterator keeps its own traversal state
- You want to provide a uniform interface for traversing different aggregate structures (supporting polymorphic iteration)
- The iteration logic is complex (e.g., depth-first vs breadth-first over a tree) and should be separated from the collection itself

## When NOT to Use

- When the language already provides a built-in iteration protocol (e.g., Python's `__iter__`/`__next__`, JavaScript's `Symbol.iterator`) that you could implement directly — wrapping it adds no value
- When the collection is a plain array or list and sequential access is the only traversal ever needed — just use a for loop
- When performance is critical and the overhead of repeated method dispatch per element is measurable

## Structure

- **Iterator** — Defines an interface for accessing and traversing elements (`hasNext()`, `next()`, optionally `reset()`).
- **ConcreteIterator** — Implements the Iterator interface. Tracks the current position in the traversal of the ConcreteAggregate.
- **Aggregate** — Defines an interface for creating an Iterator object.
- **ConcreteAggregate** — Implements the Aggregate interface and returns an instance of the proper ConcreteIterator.

## TypeScript Example

### Without the Pattern

```typescript
// Without Iterator, the client must know the internals of the collection.
// Switching from array-backed to tree-backed storage breaks all client code.

class PlaylistV1 {
  // Internal representation exposed
  public songs: string[] = [];

  add(song: string): void {
    this.songs.push(song);
  }
}

const p = new PlaylistV1();
p.songs.push("Song A");
p.songs.push("Song B");

// Client directly accesses internal array — tightly coupled
for (let i = 0; i < p.songs.length; i++) {
  console.log(p.songs[i]);
}
// If internal changes to a Set or Map, all clients break.
```

### With the Pattern

```typescript
// Iterator interface
interface Iterator<T> {
  hasNext(): boolean;
  next(): T;
  reset(): void;
}

// Aggregate interface
interface IterableAggregate<T> {
  createIterator(): Iterator<T>;
}

// ConcreteAggregate — internal representation is hidden
class Playlist implements IterableAggregate<string> {
  private songs: string[] = [];

  add(song: string): void {
    this.songs.push(song);
  }

  // Returns an iterator without exposing the array
  createIterator(): Iterator<string> {
    return new PlaylistIterator(this.songs);
  }

  // Bonus: a reverse iterator, same aggregate
  createReverseIterator(): Iterator<string> {
    return new PlaylistIterator([...this.songs].reverse());
  }
}

// ConcreteIterator
class PlaylistIterator implements Iterator<string> {
  private index = 0;

  constructor(private songs: string[]) {}

  hasNext(): boolean {
    return this.index < this.songs.length;
  }

  next(): string {
    if (!this.hasNext()) throw new Error("No more elements");
    return this.songs[this.index++];
  }

  reset(): void {
    this.index = 0;
  }
}

// Client — never sees the internal array
const playlist = new Playlist();
playlist.add("Bohemian Rhapsody");
playlist.add("Stairway to Heaven");
playlist.add("Hotel California");

const iter = playlist.createIterator();
while (iter.hasNext()) {
  console.log(iter.next());
}
// Bohemian Rhapsody
// Stairway to Heaven
// Hotel California

// JavaScript built-in iteration protocol integration
class Playlist2 implements Iterable<string> {
  private songs: string[] = [];
  add(song: string): void { this.songs.push(song); }

  [Symbol.iterator](): globalThis.Iterator<string> {
    let index = 0;
    const songs = this.songs;
    return {
      next(): IteratorResult<string> {
        if (index < songs.length) {
          return { value: songs[index++], done: false };
        }
        return { value: undefined as unknown as string, done: true };
      },
    };
  }
}

const p2 = new Playlist2();
p2.add("Song A");
p2.add("Song B");

for (const song of p2) {
  console.log(song); // works with for...of natively
}
```

## Python Example

### Without the Pattern

```python
class Playlist:
    def __init__(self) -> None:
        self.songs: list[str] = []  # exposed internals

    def add(self, song: str) -> None:
        self.songs.append(song)

playlist = Playlist()
playlist.add("Bohemian Rhapsody")

# Client directly accesses internal list
for i in range(len(playlist.songs)):
    print(playlist.songs[i])
```

### With the Pattern

```python
from __future__ import annotations
from typing import Iterator, Generic, TypeVar

T = TypeVar("T")

# Python's built-in iterator protocol — implement __iter__ and __next__
class Playlist:
    def __init__(self) -> None:
        self._songs: list[str] = []  # hidden

    def add(self, song: str) -> None:
        self._songs.append(song)

    def __iter__(self) -> PlaylistIterator:
        return PlaylistIterator(self._songs)

    def reversed_iter(self) -> PlaylistIterator:
        return PlaylistIterator(list(reversed(self._songs)))

class PlaylistIterator:
    def __init__(self, songs: list[str]) -> None:
        self._songs = songs
        self._index = 0

    def __iter__(self) -> "PlaylistIterator":
        return self

    def __next__(self) -> str:
        if self._index >= len(self._songs):
            raise StopIteration
        song = self._songs[self._index]
        self._index += 1
        return song

# Client — internal list is never exposed
playlist = Playlist()
playlist.add("Bohemian Rhapsody")
playlist.add("Stairway to Heaven")
playlist.add("Hotel California")

for song in playlist:
    print(song)

# Can have two simultaneous traversals with independent state
iter1 = iter(playlist)
iter2 = playlist.reversed_iter()
print(next(iter1))   # Bohemian Rhapsody (forward)
print(next(iter2))   # Hotel California (reverse)
```

## Real-World Analogy

A TV remote control's "channel up" button is an iterator over the channel list. You do not need to know that your cable provider stores channels in a sorted array, a sparse hash table, or a tree indexed by region. You just press "next" and the remote advances to the next available channel. The remote encapsulates traversal logic; you only see one channel at a time. Multiple people could hold separate remotes — each maintaining their own current channel — without interfering with each other.

## Related Patterns

- **Composite** — Iterators are frequently applied to Composite trees to traverse the structure; a recursive iterator on a Composite produces a flat sequence
- **Factory Method** — Polymorphic iterators rely on Factory Method to instantiate the appropriate ConcreteIterator for a given ConcreteAggregate
- **Memento** — can be used with Iterator to capture the state of an iteration and roll it back if needed
- **Visitor** — uses iteration internally to apply an operation to each element of a structure
