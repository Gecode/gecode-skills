# Gecode Brancher Implementation

## Core
- Brancher is the actor that implements branching behavior.
- Implement `status`, `choice(Space&)`, `choice(const Space&, Archive&)`, `commit`, `print`, `copy`, and `dispose`.
- Choice stores only space-independent commit data.
- `commit` must work with recomputed or cloned spaces using only the choice payload.
- Choices must be archive-compatible and deterministic.
- Branchers execute in queue order of posting.
- Optional `ngl()` adds no-good support.
- `status()==false` does not imply immediate disposal; commits for earlier choices must remain valid.

## Key Patterns
- Track the first candidate index such as `start` to avoid rescanning.
- Keep the choice payload minimal, for example `pos`, `val`, and alternative count, and archive it deterministically.
- Use binary alternatives such as `eq` versus `nq` unless an assignment brancher genuinely needs a single alternative.
- Implement an NGL class with `status`, `prune`, `subscribe`, `cancel`, `reschedule`, and `copy`; add `notice` and disposal handling when the literal owns resources.
- For complementary last alternatives, `ngl()` can return `NULL` when that is semantically valid.
- Reuse branchers through views, notably minus views for max-style variants.
- Encode the problem heuristic explicitly, such as Warnsdorff or best-fit slack.
- Mix assignment-style one-alternative choices with pruning alternatives only when the heuristic justifies it.
- Design second alternatives to embed symmetry breaking when safe.
- Pair the brancher with branch print callbacks for explainability and debugging.

## Pitfalls
- Storing views or pointers to space state inside choice objects.
- Disposing the brancher too early when `status()` becomes false.
- Depending on mutable brancher state not encoded in the choice for `commit()`.
- Using choices after invalidation by a later `choice()` call on the same space.
- Not skipping assigned views, causing repeated same choice or an infinite tree.
- Violating recomputation invariants and commit-order assumptions.
- Using generic variable-value branching when a structure-aware heuristic is required.
- Forgetting that brancher disposal is not automatic when external resources exist.
