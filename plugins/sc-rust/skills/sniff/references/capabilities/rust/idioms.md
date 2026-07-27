---
paths:
  - "**/*.rs"
  - "!**/target/**"
---
# Rust Idioms — Code Quality Pivot

Criteria for `/sc-rust:audit`. Loaded at audit time, never installed to `.claude/rules/`.

## Ownership and borrowing

- Prefer borrowing (`&T`, `&mut T`) over cloning unless the value must be owned.
- Never call `.clone()` to satisfy the borrow checker without first considering lifetime restructuring.
- Use `Cow<'_, T>` when data may be either borrowed or owned depending on context.
- Prefer `&str` over `&String` and `&[T]` over `&Vec<T>` in function signatures.

## Lifetimes

- Annotate explicit lifetimes only when the compiler cannot elide them.
- Avoid `'static` bounds unless the value genuinely lives for the program's lifetime.
- Prefer `Arc<T>` over manual lifetime threading when sharing across async tasks.

## Error handling

- Use `?` for error propagation. `.unwrap()` / `.expect()` are a defect **only** where `?` is possible (the function returns `Result`/`Option`) **and** the call is genuinely fallible — exempt the idiomatic-infallible cases (`write!` to a `String`, `Mutex::lock()` poison-only, regex on a `const` literal). Not every `.unwrap()` is a bug.
- The runtime-agnostic rule is: **errors crossing an API boundary should be typed, not stringly-typed.** Name a specific error crate (`thiserror` for libraries, `anyhow`/`eyre`/`snafu`/`miette` for applications) **only if `Cargo.toml` declares it** — do not prescribe `thiserror`/`anyhow` on a project that chose another stack.

## Iterators

- Prefer iterator chains (`.map()`, `.filter()`, `.fold()`, `.collect()`) over `for` loops that build collections.
- Use `.iter()` for immutable iteration, `.iter_mut()` for mutable, `.into_iter()` for consuming.
- Prefer `.any()` / `.all()` / `.find()` over manual loop flags.
- Avoid `.collect::<Vec<_>>()` followed by `.iter()` — chain directly.

## Traits and generics

- Prefer `impl Trait` in function arguments over `Box<dyn Trait>` when dynamic dispatch is not required.
- Use `Box<dyn Trait>` only when the concrete type is unknown at compile time.
- Implement standard traits (`Display`, `From`, `Into`, `TryFrom`, `Default`) before inventing custom ones.
- Use `#[derive]` for `Clone`, `Debug`, `PartialEq`, `Hash` when semantically correct.

## Async

These rules apply **only when `Cargo.toml` declares an async runtime**, and name crates measured from it — never by default. The runtime-agnostic defects (left of the arrow) hold regardless of stack; the crate names (right) are illustrative of a tokio project.

- Never block the async runtime — offload CPU-bound work to the runtime's blocking pool (`tokio::spawn_blocking`, `smol::unblock`, …).
- Prefer structured concurrency over sequential `await` chains where futures are independent (`tokio::select!`, `futures::select!`, …).
- Shared mutable state across tasks uses a `Send + Sync` container (`Arc<Mutex<T>>` / `Arc<RwLock<T>>`), never `Rc<RefCell<T>>` — this one is runtime-agnostic.
- Observability annotation (`#[tracing::instrument]`, …) applies **only if the project uses that instrumentation crate** — do not require `tracing` on a project that does not depend on it.

## Clippy compliance

- All public items must pass `clippy::pedantic` without `#[allow]` suppressions unless justified by a comment.
- Suppress specific lints at the item level, not the crate level.
- Prefer `clippy::must_use` annotation on functions with non-trivial return values.
