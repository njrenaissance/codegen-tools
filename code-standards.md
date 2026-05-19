# Code Standards

## General Principles

1. **Readability over cleverness** - Code is read more than written
2. **Explicit over implicit** - Be clear about intent
3. **Fail fast** - Validate early, surface errors immediately

## Error Handling

- Catch specific exceptions, not generic catches
- Log errors with context (operation, input, user)
- Fail gracefully with user-friendly messages
- Don't swallow exceptions silently

## Security Requirements

- Always return general authentication/authorization errors so you do not leak information for enumeration attacks
- Never log sensitive information - instead obfuscate the value
- Validate and sanitize all external input
- Always Use secrets management, no hardcoded credentials
- Apply principle of least privilege

## Logging Guidelines

- **Use structured logging** - Never use print statements in production code
- **Child loggers** - Always create child loggers with service/module names
- **Structured context** - Always pass context as objects, not string interpolation

## Testing Principles

- **Test-Driven Development (TDD)** - Always Write unit tests before writing implementation code
- **Table-driven tests** Always use tables for parameterized cases
- **Meaningful test names** - Always describe what is being tested and expected outcome
- **Use fixtures for shared test objects** - Always create fixtures for test data shared across two or more tests
- **Mock external services** - Always use mocks for external/third-party services to ensure reliable, fast, and isolated unit tests
