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
- Prefer iterator-based domain operations such as `inter_r`, `narrow_r`, or `minus_r` for domain propagation.
- Use fixpoint reasoning deliberately; return `ES_FIX` only when justified.
- Use `ModEventDelta` and staging to combine cheap and expensive propagation phases.
- Use advisors for incremental change localization.
- Maintain council lifecycle correctly when advisors are present, including rescheduling and subscription completeness.
- Rewrite propagators with `GECODE_REWRITE` when state simplifies enough to switch representation.
- Use reified and rewriting patterns to remove reification overhead once control literals decide the mode.
- Template propagators on view types for reuse.
- If decomposition is propagation-weak, prefer a dedicated propagator or an extensional surrogate.
- Treat expensive support data as a cacheable object rather than recomputing it per post.

## Pitfalls
- Modifying a view while iterating its domain iterator.
- Returning `ES_FIX` when the propagator is not actually at fixpoint.
- Returning `ES_NOFIX` when the propagator is idempotent and could finish inside the same `propagate()` call.
- Missing view updates or subscription cancellation during cloning or disposal.
- Using external resources without `AP_DISPOSE` notice/ignore discipline.
- Continuing execution after subsuming or disposing the actor.
- Failing to check modification-event failure after view updates.
- Breaking subscription completeness when using advisors or dynamic subscriptions.
- Expecting two weak propagators such as `distinct` plus `linear` to match the joint reasoning of one stronger constraint.
