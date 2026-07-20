# Gecode Search Engine Implementation

## Core
- Implement engines against the `Space` interface: `status`, `choice`, `clone`, and `commit`.
- Maintain explicit ownership for all `Space*` and `Choice*` objects.
- Respect compatibility invariants: choices are valid only for clone-related spaces.
- Treat `choice()` as invalidating earlier choices on that space.
- Handle all `SpaceStatus` cases: `SS_FAILED`, `SS_SOLVED`, and `SS_BRANCH`.

## Key Patterns
- Keep a clear split between exploration mode and recomputation mode.
- Use edge or path state to store choices, alternatives, and optional clones.
- For recomputation, replay commits from the nearest stored clone or the root clone.
- Apply LAO, the last-alternative optimization, to avoid unnecessary stored choices and commits.
- Use hybrid recomputation with a commit distance to cap replay cost.
- Use adaptive recomputation to add clones where repeated failures show that recomputation is too expensive.
- Integrate branch-and-bound by constraining future spaces against the current best solution.
- Keep restart and meta-engine hooks explicit, such as `master` and `slave`, when required.
- Wire statistics and stop-object checks consistently.
- In current main, stop objects and no-good state are copyable and parallel search uses atomic stop coordination plus completion handshakes; do not share mutable stop state non-atomically or destroy PBS workers before their completion signal.

## Pitfalls
- Reusing stale choices after another `choice()` call.
- Mixing incompatible choices and spaces and triggering `SpaceNoBrancher`.
- Forgetting to delete choices and returned solution spaces.
- Assuming deterministic node order under parallel execution.
- Overusing no-good depth without accounting for memory and LAO tradeoffs.
- Reporting completeness when stop, cutoff, or meta-engine policy makes the run incomplete.

## Invariants
- Recomputed spaces must follow the same decision path as the stored edge choices.
- Commit order must match original choice generation order.
- If recomputation fails due to nondeterminism or weak monotonicity effects, recover path state safely and continue search.
- Cloning and copying must never mutate model state outside the allowed operations.
