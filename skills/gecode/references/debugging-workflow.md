# Gecode Debugging Workflow

## Symptom: Search Tree Explodes
- First ask whether the model is weak or the branching is weak; the fix is often different.
- Check initial domains, missing implied constraints, and whether a stronger global can replace a weak decomposition.
- Compare nodes and failures before and after modeling changes; do not trust runtime alone.
- If propagation looks adequate but the tree is still huge, inspect branching order, value choice, and symmetry breaking.
- Use `DFS` as a baseline before judging restart or portfolio search.

## Symptom: Branching or Recomputation Looks Wrong
- Suspect stale choices if behavior changes after another `choice()` call on the same space.
- Recheck choice compatibility: choices must be valid only for the originating space and its clones.
- Confirm `commit()` uses only archived, space-independent choice payload.
- If a bug appears only after deeper search, compare direct-clone behavior versus replayed recomputation behavior.
- When a custom brancher is involved, inspect queue order, assigned-view skipping, and brancher disposal timing.

## Symptom: Propagation Is Wrong or Too Weak
- Separate correctness bugs from strength issues. Wrong answers or unexplained failure usually mean correctness; huge trees with valid answers usually mean weak propagation.
- Re-check subscriptions, propagation conditions, and whether the propagator actually reaches fixpoint when it should.
- Replace weak decompositions with stronger globals or a dedicated propagator when two ordinary constraints do not reason jointly enough.
- Use advisor-based localization only when the extra complexity is justified by change locality.
- If reification is involved, verify the exact semantics of the chosen decomposition rather than assuming the control literal forces a benign fallback.

## Symptom: Memory or Clone Footprint Is Too Large
- Inspect what state is copied into every clone and move resize-heavy data away from space memory when appropriate.
- Prefer lazy construction for heavy internal state when many branches will never need it.
- Check external-resource ownership and `AP_DISPOSE` discipline before assuming the issue is search alone.
- Watch for per-choice heap allocations in hot paths, especially inside custom branchers.
- If recomputation is cheaper than cloning the current state, revisit search options and state layout together.

## Observability Tools
- Use groups and tracing to narrow which parts of the model or search are active at the wrong time.
- Use Gist or CPProfiler when you need to see search-tree shape, branching behavior, and failure concentration rather than just counters.
- Measure nodes, failures, restarts, and memory-related symptoms alongside runtime.
- Improve in loops: baseline, strengthen propagation, improve branching, then tune search and memory strategy.

## Escalation Paths
- For custom propagation mechanics, continue into `propagator-implementation.md`.
- For stale-choice, commit, or NGL issues, continue into `brancher-implementation.md`.
- For memory ownership and clone-footprint problems, continue into `memory-handling.md`.
- For restart, no-good, and completeness behavior, continue into `search-engines.md` or `search-engine-implementation.md` depending on whether you are using or implementing engines.
