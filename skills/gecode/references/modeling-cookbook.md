# Gecode Modeling Cookbook

## Strong Initial Domains
- Start with the tightest semantically correct domains you can justify; domain width is often the first-order search cost.
- Introduce helper variables only when they buy propagation, symmetry handling, or cleaner branching.
- Reuse shared arrays and tuple sets when structure repeats across many constraints.

## Globals Versus Decompositions
- Prefer globals such as `distinct`, `count`, `binpacking`, `circuit`, or `extensional` when they capture the intended structure directly.
- Decompose only when there is no suitable global or when the decomposition is easier to maintain and the propagation loss is acceptable.
- When a decomposition is kept for simplicity, add implied constraints that recover some lost strength.

## Channeling and Reification
- Use channeling when two views of the same decision space support different strong constraints or different branchers.
- Keep reification semantics explicit: full reification, half reification, and decomposed reification behave differently under failure.
- If Boolean control logic starts dominating the model, verify that the introduced structure is paying for its propagation cost.

## Symmetry Templates
- Break symmetry structurally before trying heuristic tricks.
- Use anchors, ordering constraints, `precede`, or canonical placement rules to collapse equivalent solutions early.
- Re-check symmetry assumptions when mixing LDSB with static symmetry breaking or custom branchers.

## Branching Playbooks
- Put branchers in intentional order; creation order matters.
- For optimization models, branch first on variables that drive the objective or major feasibility bottlenecks.
- When a generic brancher underperforms, ask whether the issue is value choice, variable choice, or missing model structure before jumping to a custom brancher.

## Optimization Setup
- Use `BAB` as the default exact optimization engine.
- If best-solution search stalls, improve bounds and cost-driving propagation before assuming a different engine will rescue the model.
- Tune restart or portfolio search only after you understand the baseline `DFS` or `BAB` behavior.

## Propagation Versus Search
- If failures come late and trees are wide, strengthen propagation first.
- If failures are early but node count is still high, the model may be fine and the branching may be poor.
- When a model already has strong globals and tight domains, branching quality often dominates the next gain.
