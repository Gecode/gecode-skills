# Gecode Search Engines

## Core
- This reference is for using built-in engines, not implementing custom engines.
- Base engines are `DFS`, `BAB`, and `LDS`.
- Meta engines are `RBS` for restart-based search and `PBS` for portfolio-based search.
- Key options live in `Search::Options`, including `threads`, `c_d`, `a_d`, `clone`, `stop`, `cutoff`, `nogoods_limit`, `assets`, `slice`, and `tracer`.
- For optimization, use `BAB`-style search with a valid model-side objective and constrain setup.

## Key Patterns
- Use `DFS` for baseline complete search and enumeration.
- Use `BAB` for best-solution search.
- Use `LDS` when the branching heuristic is strong and discrepancy-ordered exploration is desirable.
- Use `RBS` to improve robustness through cutoffs, restart policies, and optional no-goods.
- Use `PBS` to improve robustness through asset diversification across heuristics, models, engines, or options.
- In restart search, let `master()` decide restart behavior and optional no-good posting.
- In restart search, let `slave()` signal completeness intentionally: `true` for complete slave search, `false` for deliberate incompleteness such as LNS neighborhoods.
- In portfolio search, remember `slave()` return value has no meaning.
- For restart-based best-solution assets in portfolios, use `RBS<Script,BAB>`.
- Diversify assets intentionally; identical assets rarely justify portfolio overhead.

## Pitfalls
- Expecting deterministic behavior from restart, portfolio, or parallel runs.
- Treating restart or portfolio search as complete when stop conditions, cutoffs, or `slave()==false` make the run incomplete.
- Forgetting to diversify assets and then expecting portfolio gains.
- Assuming no-goods are always available or effective regardless of brancher mix and parallelism.
- Forgetting that `master()` and `slave()` policy choices directly change search completeness and restart behavior.

## No-Good and Parallel Nuances
- Restart no-goods are available from `DFS` and `BAB`, not `LDS`.
- Enable no-goods with `nogoods_limit > 0`; depth is a memory-versus-benefit tradeoff.
- Larger no-good depth limits reduce LAO effectiveness near the root and can raise memory use significantly.
- Not all branchers support no-goods; float branchers and execution branchers do not.
- Parallel search usually yields fewer extractable no-goods.
- Parallel search is intentionally nondeterministic in solution order, node counts, and runtime.
- In portfolios, `assets` and `threads` are allocated conservatively.
- Sequential portfolios use failure slices via `slice` for round-robin asset scheduling.
- With `threads > assets`, extra threads can be used inside asset engines.
