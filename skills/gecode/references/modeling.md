# Gecode Modeling

## Related References
- Read `modeling-cookbook.md` for recipe-style modeling patterns and concrete construction templates.
- Read `set-and-float-modeling.md` when the task depends on set vars, float vars, or mixed-domain behavior.
- Read `scheduling-patterns.md` for cumulative/resource-style models and sequencing-heavy schedules.

## Core
- Define the model as a `Space` subclass.
- Create typed variable arrays with tight domains early.
- Post constraints via post functions such as `rel`, `linear`, `distinct`, and the set/float variants.
- Post branching via `branch(...)`; variable and value strategy together define the tree shape.
- Use search engines such as `DFS`, `BAB`, or restart/portfolio variants according to the objective.
- MiniModel adds expression syntax via `expr(...)`, `rel(...)`, and matrix/channel helpers.
- Reified modeling supports full and half reification; decomposition semantics matter.

## Key Patterns
- Prefer global constraints over manual decompositions when available.
- Keep branchings explicit and problem-specific for scale.
- Use multiple branchers intentionally; creation order matters.
- Tune search options such as recomputation distance, restarts, no-goods, and stop objects.
- Use tracing, Gist, or CPProfiler for diagnostics.
- Add implied constraints when semantics stay unchanged but propagation improves.
- Break symmetry structurally with order constraints, fixed anchors, `precede`, or monotone bins.
- Use LDSB only with supported branching and value configurations, and validate symmetry assumptions.
- Match propagation level to complexity; use `IPL_DOM` only where the payoff exceeds the cost.
- Replace weak decompositions with stronger globals such as `count`, `binpacking`, `circuit`, or `extensional`.
- Cache reusable heavy artifacts such as tuple sets or shared arrays keyed by shape and parameters.
- For arrays requiring non-shared variables, call `unshare(...)` once and reuse the result.
- Use branch filters and print functions for targeted branching and observability.
- When executing code between branchers, remember propagation is still explicit on recomputation paths.
- For optimization models, branch on cost-driving variables first and tie-break with objective structure.
- Current main optionally exposes counting-based search branching through `cbsbranch(...)` when built with `GECODE_ENABLE_CBS`; treat it as an optional, model-dependent alternative to generic branching.

## Pitfalls
- Weak domains at model start causing huge trees.
- Forgetting to update every variable member in the cloning constructor.
- Assuming MiniModel nonlinear expressions stay monolithic; many decompose.
- Assuming reified non-functional decompositions imply `b=false`; they can fail instead.
- Treating Boolean variables as a subclass of integer variables.
- Ignoring exceptions from invalid arguments or overflow.
- Using domain propagation for `linear` indiscriminately when it can be exponential.
- Recomputing identical tuple sets or shared maps per post.
- Repeated implicit unsharing patterns that create unnecessary variables and propagators.
- Combining LDSB with unrelated static symmetry breaking without safety analysis.
- Leaving major value or variable symmetries unbroken.
