---
name: clean-code
description: Uncle Bob's Clean Code and formatting rules — the primary coding standard for all engineering work on this project
---

# Clean Code Standard

These rules apply to every file you touch. They are not guidelines — violations are grounds for task rejection.

## Clean Code (Robert C. Martin)

**Small functions**: 5–10 lines. One function does one thing. If you need "and" to describe it, split it.

**Single level of abstraction**: Every line inside a function operates at the same abstraction level. No mixing high-level orchestration with low-level detail in the same function.

**Boy Scout Rule**: Always leave code cleaner than you found it. Every touch is an opportunity for a small improvement.

**DRY**: No duplicated logic. Extract shared behavior into well-named abstractions.

**Self-documenting code**: Code explains itself through naming. Comments explain *why*, never *what*.

**Meaningful names**: Names are pronounceable, searchable, and describe the problem domain. No abbreviations. No single letters outside loop counters.

**No flag arguments**: Never pass a boolean to control function behavior. Split into two functions with descriptive names instead.

**Prefer fewer arguments**: 0–2 is the target. 3 is acceptable. More than 3 requires a named parameter object.

**Vertical separation**: Related concepts are vertically close. Caller appears above callee in the file. Unrelated concepts are separated by whitespace.

**Delete commented-out code**: Remove it immediately. Version control keeps history.

## Formatting Rules

**File size**: Max 200 lines (hard limit 500). Approaching 200 means consider splitting.

**Line length**: Max 120 characters (target 100).

**Blank lines**: Separate package declarations, imports, and each function. Unrelated concepts get whitespace between them.

**Variable placement**: Declare variables as close to their usage as possible.

**Caller above callee**: When function A calls function B, A appears above B. Read top-to-bottom like a newspaper.

**Group related functions**: Conceptually related functions live close together.

**Operator whitespace**: Whitespace around operators. No trailing whitespace.

**Indentation**: Each nested level indented one step right. Indentation communicates structure.

**No unnecessary alignment**: Do not pad code to align columns across lines.

## SOLID

**Single Responsibility**: One reason to change per module, service, or function.

**Open/Closed**: Extend behavior via new interface implementations. Never modify existing code to add behavior.

**Liskov Substitution**: Every interface implementation is fully substitutable. No stub `NotImplemented` methods.

**Interface Segregation**: Narrow interfaces. No component depends on methods it does not use.

**Dependency Inversion**: Domain logic depends on abstractions. Infrastructure implements them. Never the reverse.

## Clean Architecture

Dependencies point inward: `domain ← services ← infrastructure ← delivery (MCP/API)`.

The domain layer has zero framework, DB, or HTTP imports. MCP tools and HTTP handlers are thin adapters — no business logic in them.

## TDD

Write tests before implementation. Red → green → refactor.

A test that never fails is not a test.

Test names describe behavior: `"returns error when stock is insufficient"` not `"test_checkStock_fail"`.
