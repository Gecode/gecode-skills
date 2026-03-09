# Gecode Scheduling Patterns

## Resource-Style Models
- Start with the tightest time windows, durations, and resource bounds you can justify.
- Prefer cumulative or other structure-aware scheduling constraints over hand-built overlap decompositions when the resource semantics are standard.
- Add obvious implied constraints such as precedence, release/deadline tightening, or resource-balance bounds when they strengthen propagation without changing semantics.

## Sequencing and Ordering
- Use explicit sequencing or order constraints when the model’s main difficulty is relative position rather than raw resource usage.
- Anchor interchangeable tasks or machines when symmetry would otherwise multiply equivalent schedules.
- When setup or transition structure matters, make it explicit in the model rather than burying it inside a weak objective.

## Branching Guidance
- Branch first on bottleneck tasks, scarce resources, or tasks that most affect the objective.
- Prefer branchers that expose schedule structure over generic variable-value selection when the schedule has obvious critical-path or packing bottlenecks.
- If a schedule model has wide windows and weak propagation, strengthen the model before inventing a custom search strategy.

## Common Failure Modes
- Weak overlap decompositions that fail to propagate resource pressure.
- Symmetric machines or interchangeable tasks creating huge equivalent subtrees.
- Objective-driven search without enough feasibility structure, causing the engine to explore many nearly identical schedules.
- Diagnosing schedule problems only by runtime rather than failures, nodes, and where the tree actually branches.
