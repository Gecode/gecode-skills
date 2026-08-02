# Gecode Propagator Implementation

## Core

- Propagators compute on views, not model variables.
- Implement a post function and the actor lifecycle: `copy`, `dispose`, `cost`, `reschedule`, and `propagate`.
- Use `Home` for posting context and use fail/check macros.
- Return honest `ExecStatus`: `ES_FAILED`, `ES_FIX`, or `ES_NOFIX`; when a propagator is subsumed, return `home.ES_SUBSUMED(*this)` (or `home.ES_SUBSUMED_DISPOSED(...)` when the disposal size is part of the return). Never use the internal `ES_SUBSUMED_` enum value directly.
- Respect obligations around correctness, checking, contracting, monotonicity or waived monotonicity, subscription completeness, and update completeness.
- Respect implementation obligations: subsumption complete, cloning conservative, and subscription correct.
- Use standard patterns such as `Unary`, `Binary`, `Ternary`, `Nary`, or mixed variants to reduce boilerplate.

## Key Patterns

- Do cheap pruning in `post()` and skip posting when already subsumed or failed.
- Select the weakest sound propagation condition: `*_VAL`, `*_BND`, or `*_DOM`.
- Prefer range iterators and range operations whenever the data can be represented as intervals. Build or expose the complete candidate set as ranges, then apply one iterator-based domain operation such as `inter_r`, `narrow_r`, or `minus_r`.
- Prefer `IntSetRanges`, `Int::ViewRanges`, and `Iter::Ranges` combinators such as `Inter` over repeated `in(value)` probes or value-by-value updates. Prefer the `_r` operation (`inter_r`, for example) over its `_v` counterpart when a range iterator is suitable. Range work is proportional to the number of ranges rather than the number of represented values and avoids accidental quadratic scans of sparse or repeatedly queried domains.
- Use value iterators and `_v` operations only when the algorithm inherently produces isolated values and converting them to canonical ranges would not reduce work. Make that tradeoff explicit in hot propagation code.
- Use fixpoint reasoning deliberately; return `ES_FIX` only when justified.
- Stage mixed-cost propagators so cheap event-specific pruning runs in an early queue and only the remaining expensive work waits for a high-cost queue.
- Use advisors for incremental change localization.
- Maintain council lifecycle correctly when advisors are present, including rescheduling and subscription completeness.
- Rewrite propagators with `GECODE_REWRITE` when state simplifies enough to switch representation.
- Use reified and rewriting patterns to remove reification overhead once control literals decide the mode.
- Template propagators on view types for reuse.
- If decomposition is propagation-weak, prefer a dedicated propagator or an extensional surrogate.
- Treat expensive support data as a cacheable object rather than recomputing it per post.

## Staged Propagation and Cost

- Stage by algorithmic cost, not only by consistency level or modification-event kind. Scheduling propagators often have cheap incremental checks and expensive passes such as not-first/not-last or edge finding, even though all phases react to the same bound changes.
- Run cheap filtering and failure checks before the high-cost queue. They can fail, subsume the actor, shrink the task set, or make an expensive pass unnecessary.
- Make `cost(home, med)` describe the next phase that will actually run. Do not assign the whole propagator the cost of its most expensive algorithm.
- Use event-driven staging when `ModEventDelta` naturally identifies the phase. Inspect the delta with the view's `me(med)`, perform the cheap work, and return `home.ES_FIX_PARTIAL(*this, remaining_med)` to consume the handled events and reschedule the remaining work at its own cost.
- Use explicit stage state when cheap and expensive algorithms respond to the same event. Store a small phase enum or pending-work flags in the propagator, copy them during cloning, and let `cost()` consult that state. After the cheap phase, mark the expensive phase pending and return `ES_FIX_PARTIAL` with a valid nonzero delta compatible with the subscriptions. The next scheduling decision then uses the expensive phase's cost.
- Return `home.ES_NOFIX_PARTIAL(*this, remaining_med)` when the completed phase is not at fixpoint and its events must be combined with the remaining work. Never return the internal `ES_PARTIAL_` value directly.
- Keep subscriptions and `reschedule()` sufficient for every phase. Clear or advance phase state on every exit path, and preserve it in the propagator's copy constructor.
- Use separate propagators when phases have independent state, subscriptions, lifetimes, or useful standalone fixpoints. Use partial propagation when the phases implement one constraint and share substantial state.

Event-driven staging can use different deltas and costs for value, bound, or domain events. Algorithm-driven staging uses the same principle with explicit state:

```cpp
enum class Stage { Cheap, Expensive };
Stage stage = Stage::Cheap;

PropCost cost(const Space&, const ModEventDelta& med) const {
  return (stage == Stage::Cheap)
    ? cheap_cost(med)
    : expensive_cost(med);
}

ExecStatus propagate(Space& home, const ModEventDelta& med) {
  if (stage == Stage::Cheap) {
    GECODE_ES_CHECK(propagate_cheap_to_fixpoint(home));
    if (!expensive_needed())
      return ES_FIX;
    stage = Stage::Expensive;
    return home.ES_FIX_PARTIAL(*this, expensive_med(med));
  }
  stage = Stage::Cheap;
  return propagate_expensive(home);
}
```

## Testing New Propagators

- Use Gecode's test infrastructure as the primary test harness. Extend `Test::Int::Test`, `Test::Set::SetTest`, or `Test::Float::Test`, provide an independent solution predicate, and post the constraint through the harness.
- Let the harness exercise assignments and partial assignments before and after posting, randomized incremental pruning, intermittent fixpoint computation, cloning, disabled/re-enabled propagators, reification modes, failure, and subsumption. Run focused deterministic regression cases in the same infrastructure for every discovered bug.
- Test semantics against an independent oracle; do not reproduce the propagator algorithm in the test.
- Re-run failing randomized cases with the reported seed and test selector, then add a minimal regression case if the failure exposed a distinct edge case.
- Add a small direct unit test only for isolated helper logic that the propagator harness cannot reach economically. Do not replace the Gecode harness with a bespoke `Space`, search loop, or random simulator.
- Do not post every permutation of propagators to test correctness. A correct propagator cannot depend on scheduler order; permutation tests add combinatorial cost while missing the lifecycle, cloning, fixpoint, disable/enable, and subsumption checks already provided by the harness.

## Pitfalls

- Modifying a view while iterating its domain iterator.
- Repeatedly probing `in(value)` for a collected set of candidates, causing repeated domain scans or quadratic behavior instead of a single range intersection.
- Returning `ES_FIX` when the propagator is not actually at fixpoint.
- Returning `ES_FIX` after only the cheap stage when expensive work remains, thereby consuming pending events and skipping required propagation.
- Reporting only the propagator's worst-case cost, thereby delaying cheap filtering until the high-cost queue runs.
- Forgetting to clone or reset explicit stage state, causing recomputation or later propagation rounds to enter the wrong phase.
- Returning `ES_NOFIX` when the propagator is idempotent and could finish inside the same `propagate()` call.
- Missing view updates or subscription cancellation during cloning or disposal.
- Using external resources without `AP_DISPOSE` notice/ignore discipline.
- Continuing execution after subsuming or disposing the actor.
- Failing to check modification-event failure after view updates.
- Breaking subscription completeness when using advisors or dynamic subscriptions.
- Expecting two weak propagators such as `distinct` plus `linear` to match the joint reasoning of one stronger constraint.
- Writing a custom propagator test runner instead of integrating the test into Gecode's test suite.
- Treating propagator ordering as a semantic requirement or attempting to force every ordering in tests.
