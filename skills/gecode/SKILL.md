---
name: gecode
description: "Gecode architecture, modeling, cookbook-style modeling patterns, set-variable, float-variable, and scheduling guidance, propagators, branchers, memory management, search engine usage and implementation, recomputation/cloning behavior, debugging/performance diagnosis, and downstream CMake consumption. Use for any materially Gecode-specific task: building or refining Gecode models, implementing custom constraints or branchers, tuning DFS/BAB/RBS/PBS/LDS search, diagnosing weak propagation or search pathologies, reasoning about set, float, or resource-style models, or integrating Gecode into CMake projects."
---

# Gecode

Use this skill as the entry point for any Gecode-specific task. Carry the universal Gecode runtime model in mind for every response, then load only the additional reference files needed for the task.

## Constraint Programming in One Paragraph

Constraint programming represents each variable by a domain of still-possible values and repeatedly propagates constraints until no propagator can remove anything else or a domain becomes empty. Domain states form a lattice ordered by information (smaller domains contain more information). Treat a propagator as a contracting, weakly monotonic operation on that lattice: it can remove values but cannot restore them. Fair propagation reaches a simultaneous fixpoint, but with weakly monotonic propagators execution order can produce different, even incomparable, fixpoints and search-tree shapes. Weak monotonicity preserves the solution set, so complete search remains sound and complete even when the propagation trace, fixpoint strength, or solution order differs.

## Always-On Mental Model
- Space is the home for variables, propagators, branchers, and optimization order.
- Propagation is explicit: call `status()`.
- Search primitives are `status()`, `choice()`, `clone()`, `commit()`, and `constrain()`.
- Space status values are `SS_FAILED`, `SS_SOLVED`, and `SS_BRANCH`.
- Choice is a space-independent descriptor; alternatives are indexed `0..n-1`.
- Choice compatibility is clone-based: a choice is valid for its source space and clones.
- `choice()` invalidates previous choices for later `commit()` on that space.
- Clone only stable, non-failed spaces.
- Branchers run in posting order.
- Recomputation can be nondeterministic with weakly monotonic propagation while remaining sound and complete.
- Model as `class M : public Space`, implement a copy constructor and virtual `copy()`, and update variable arrays with `x.update(*this, s.x)` in the model copy constructor; reserve `home` for actor `copy(Space& home)` APIs.
- After `status()==SS_BRANCH`, compute `choice()` immediately.
- Treat returned solutions as owned `Space` objects and delete seed models, choices, and solution spaces explicitly.
- Do not assume posting performs full propagation.
- Do not call the `Space` copy constructor directly instead of `clone()`.
- Do not reuse stale choices after another `choice()` call.

## Default Gecode Heuristics
- Tighten variable domains as early as possible.
- Prefer global constraints over weak manual decompositions.
- Keep branching explicit and problem-specific rather than relying on generic defaults.
- Treat symmetry handling as first-class design work.
- Use `DFS` as the baseline complete search engine.
- Use `BAB` for optimization unless there is a concrete reason to move to restart or portfolio search.
- Treat restart, portfolio, and parallel search behavior as intentionally nondeterministic.
- Remember that clone footprint matters when designing actor state and cached data.
- Use explicit disposal discipline for external or heap-backed resources.

## Load References

- Read only the reference file or files needed for the current task.
- Combine references only when the task genuinely crosses boundaries, such as a custom propagator with nontrivial memory strategy or a search-engine bug tied to choice compatibility.
- Prefer the narrowest useful reference set first, then expand if the user asks for adjacent concerns.
- Keep answers Gecode-specific. If the request is generic CMake, generic C++ memory, or generic CP theory without a real Gecode angle, do not over-apply this skill.
- Use this `SKILL.md` alone for broad explanations, initial modeling guidance, and many runtime/debugging answers before reaching for extra references.

| Read | When the task involves |
| --- | --- |
| `references/modeling.md` | Model structure, variables, constraints, branching setup, or built-in search configuration |
| `references/modeling-cookbook.md` | Recipe-style guidance for globals versus decompositions, channeling, symmetry, branching, or optimization setup |
| `references/debugging-workflow.md` | Weak propagation, exploding search trees, stale choices, recomputation bugs, memory growth, tracing, or profiling |
| `references/set-variable-modeling.md` | Set variables, membership or partition models, set relations and operations, channeling, cardinality, or set branching |
| `references/float-variable-modeling.md` | Float variables, interval semantics, float relations and expressions, mixed integer/float models, float branching, or float optimization |
| `references/scheduling-patterns.md` | Cumulative or resource models, sequencing constraints, or scheduling-specific branching and symmetry |
| `references/propagator-implementation.md` | Custom propagator posting, lifecycle, propagation conditions, advisors, iteration, or rewriting |
| `references/brancher-implementation.md` | Custom branchers, choices, commits, archives, heuristics, or NGL support |
| `references/memory-handling.md` | Space, region, or heap allocation; handles; clone footprint; or disposal obligations |
| `references/search-engines.md` | Selecting or tuning built-in `DFS`, `BAB`, `LDS`, restart, or portfolio search |
| `references/search-engine-implementation.md` | Custom engine orchestration, ownership, replay, recomputation, LAO, or completeness invariants |
| `references/cmake-consumption.md` | `find_package(Gecode CONFIG)`, imported targets, version checks, components, or vendored fallback |
| `references/general-knowledge.md` | Constraint-programming foundations, propagation-versus-search reasoning, search architecture and restoration, model-strength tradeoffs, symmetry, or performance interpretation beyond the always-on summary |
