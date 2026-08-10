# Constraint Programming Foundations for Gecode

## Orientation

- Treat a constraint model as a description of feasible combinations, not as an algorithm that dictates an execution order.
- Use propagation to remove values that cannot participate in a solution; use search to split the remaining possibilities when propagation alone cannot decide them.
- Judge a model by how early it exposes useful information. Equivalent formulations can produce radically different search trees.
- Expect modeling, propagation, branching, and search configuration to interact. A change in one can alter which choices are best in the others.

## Constraint-Programming Mechanics

- Give every variable a domain of currently possible values. Failure occurs when a domain becomes empty; assignment occurs when the domain represents one value.
- Let propagators contract domains until the space reaches a fixpoint. Events, priorities, and dynamic fixpoint information help the engine avoid unnecessary executions; scheduling can change cost and, for weakly monotonic propagators, which sound fixpoint is reached.
- Require a correct propagator both to preserve every solution of its constraint and to reject a complete assignment that violates that constraint.
- Distinguish propagation strength from correctness. A weak propagator can be correct yet leave a large search tree; a stronger propagator removes at least as many values but can cost more per execution.
- View a brancher as a partition of the remaining solution set. Completeness requires the alternatives together to cover every remaining solution.
- Separate search-tree shape from exploration and state restoration. Branching creates alternatives, an engine chooses how to traverse them, and restoration recovers earlier mutable solver states; Gecode combines space cloning with recomputation to manage that cost.
- Prefer global constraints when they reason about shared structure that a decomposition cannot see jointly. Keep a decomposition when its maintenance or runtime advantage outweighs the lost pruning.
- Treat reification as a logical relationship with explicit direction. Full and half reification, implication, and failure of a decomposed relation are not interchangeable.
- For optimization, let each incumbent add a stronger bound through `constrain()`. The objective model and feasibility propagation still determine whether branch-and-bound is effective.

## Decision Guidance

- Strengthen domains and constraints when failures occur deep in the tree or many branches reach nearly identical contradictions.
- Compare propagation levels by their effect on the explored search space and total cost, not only by how much each intermediate fixpoint prunes. Weaker propagation can be equivalent under the chosen branching while being cheaper to execute.
- Improve variable and value selection when propagation reaches useful fixpoints but the search still explores many equivalent or unpromising alternatives.
- Treat semantic symmetry explicitly before tuning heuristics. Choose static constraints, dynamic search procedures, or symmetry-aware filtering according to the symmetry class and its maintenance cost.
- Compare changes with nodes, failures, propagations, restarts, memory, and runtime. Runtime alone hides whether an improvement came from a smaller tree, cheaper nodes, or noise.
- Use groups, tracing, Gist, or CPProfiler to connect aggregate statistics to the model region or branch decision that produced them.
- Use a reproducible default diagnostic sequence: strengthen propagation, improve branching, then tune restart, portfolio, parallel, or recomputation options. Revisit earlier choices when later measurements expose an interaction.

## Pitfalls

- Do not infer propagator correctness from posting or execution order.
- Do not assume the strongest available propagation level is automatically the fastest overall choice.
- Do not mistake a late failure for solver malfunction before checking model strength and missing implied constraints.
- Do not compare parallel or restart runs by solution order; these modes are intentionally nondeterministic.
- Do not stop after the first correct formulation. Nontrivial CP models usually require measured refinement.
