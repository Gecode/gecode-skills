# Gecode Scheduling Patterns

## Orientation

- Start with the tightest time windows, durations, and resource bounds you can justify.
- Represent resource structure explicitly. Prefer scheduling globals over hand-built overlap decompositions when their semantics match the problem.
- Add obvious implied constraints such as precedence, release/deadline tightening, or resource-balance bounds when they strengthen propagation without changing semantics.
- Separate feasibility from optimization. Establish a strong resource and precedence model before tuning makespan or cost search.

## Gecode Mechanics

- Represent a task with start `s`, processing time `p`, and, when needed, end `e`. Use a Boolean mandatory array for optional tasks; a value of one means the task is present.
- Use `order(home, s0, p0, s1, p1, b)` for one explicit pairwise ordering decision controlled by `b`.
- Use `unary(...)` when tasks share a capacity-one resource. Use `cumulative(...)` for one resource with capacity greater than one and per-task usage. Use `cumulatives(...)` when tasks choose among multiple machines or when usage can be positive, negative, or zero.
- Select overloads deliberately. Fixed durations need less state; variable-duration overloads accept start, processing-time, and end arrays; `TaskTypeArgs` expresses fixed-processing, fixed-start, or fixed-end task variants.
- Post `s[i] + p[i] == e[i]` separately when using an overload documented not to enforce that relationship, including `cumulatives(...)` and the start/processing/end overloads of `unary(...)` and `cumulative(...)`.
- Use optional-task overloads with `BoolVarArgs` instead of simulating absence through oversized time windows or zero durations.
- Choose `IntPropLevel` with measurements. For `unary(...)`, basic propagation includes overload checking and time-tabling, while advanced propagation adds detectable precedences, not-first/not-last, and edge finding. For `cumulative(...)`, basic propagation includes overload checking and time-tabling, while advanced propagation adds edge finding.

## Decision Guidance

- Use a resource global when capacity creates the main coupling; use explicit precedence or `order(...)` when relative order itself is the decision.
- Model setup and transition structure as feasibility constraints, durations, or explicit order-dependent costs according to its real semantics; do not hide mandatory setup behavior inside the objective.
- Branch on the decisions that expose the bottleneck: presence, machine assignment, task order, or start time. Avoid branching on derived end times unless they carry independent structure.
- Anchor interchangeable machines or tasks, order equivalent assignments canonically, or otherwise break schedule symmetry before relying on a heuristic to avoid it.
- Compare nodes, failures, propagation, and where branching occurs. A wide-window model with late failures usually needs stronger bounds or resource reasoning before a custom brancher.

## Pitfalls

- Do not assume a start/processing/end scheduling overload posts `s + p == e` unless its API documentation says so.
- Do not use pairwise non-overlap decompositions when `unary(...)` or `cumulative(...)` captures the whole resource and can propagate jointly.
- Do not encode optionality by weakening domains so far that absent and present tasks become indistinguishable to propagation.
- Do not leave identical machines or interchangeable tasks symmetric.
- Do not optimize makespan or cost before the feasibility model propagates resource pressure effectively.
