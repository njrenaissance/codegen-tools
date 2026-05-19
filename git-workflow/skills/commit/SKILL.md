---
name: commit
description: Stage and commit changes with a message that follows the Conventional Commits v1.0.0 spec. Use whenever the user asks to commit, "make the commit", "commit this", commit changes, or otherwise save work to git.
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git add:*), Bash(git commit:*), Read, Edit
---

Stage and commit the current changes with a message that follows the
[Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) spec.

## What to do

1. Run `git status` and `git diff` (and `git diff --staged`) to see what changed.
   If nothing is staged, stage the relevant files; never commit unrelated changes together.
2. Run `git log --oneline -10` to match the repo's existing scope and style conventions.
3. Bump the version (see **Versioning** below) if the repo tracks one.
4. Write the message in the format below, then commit.
5. If the changes cover two unrelated concerns, make **two** commits — one per concern.

## Versioning

If the repository tracks a version (`package.json`, `plugin.json`, `pyproject.toml`,
`Cargo.toml`, etc.), bump it **before committing**, following [SemVer](https://semver.org/):

- `fix:` (and other non-feature changes like `docs:`, `refactor:`, `chore:`) → **PATCH** (`0.1.0` → `0.1.1`)
- `feat:` → **MINOR** (`0.1.0` → `0.2.0`)
- `!` / `BREAKING CHANGE:` → **MAJOR** (`0.1.0` → `1.0.0`)

Bump only the version file(s) for the component that actually changed. Include the
version bump in the same commit as the change.

## Message format

```text
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

- **type** — one of: `feat` (new feature, → MINOR), `fix` (bug fix, → PATCH),
  `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
- **scope** — optional, in parentheses: the area touched, e.g. `feat(auth):`.
- **description** — imperative mood, lowercase, no trailing period.
  "add retry to upload", not "Added retry." or "Adds retry".
- **body** — optional; explain *why*, not *what*. Wrap at ~72 chars.
- **footer** — `Token: value` lines, e.g. `Refs: #123`, `Reviewed-by: …`.

## Breaking changes

A breaking change is signalled **either** way (both is fine):

- a `!` before the colon — `feat(api)!: drop v1 endpoints`
- a `BREAKING CHANGE: <description>` footer

Either one means a MAJOR version bump.

## Examples

```text
feat(parser): support scoped package names

fix: prevent race condition on concurrent writes

Acquire the lock before reading the offset so two writers
cannot interleave.

Refs: #482

refactor!: rename `Client.fetch` to `Client.request`

BREAKING CHANGE: `fetch` is removed; callers must use `request`.

docs: fix broken link in README

chore(deps): bump ruff to 0.6.0
```

## Rules

- One logical change per commit. Split unrelated work.
- Never use a bare `update`, `wip`, or `misc` as the description.
- Don't invent a scope — omit it if there isn't a clear one.
- Keep the description under ~72 characters.
