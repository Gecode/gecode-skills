---
name: gecode
description: "Gecode architecture, modeling, cookbook-style modeling patterns, set/float/scheduling guidance, propagators, branchers, memory management, search engine usage and implementation, recomputation/cloning behavior, debugging/performance diagnosis, and downstream CMake consumption. Use for any materially Gecode-specific task: building or refining Gecode models, implementing custom constraints or branchers, tuning DFS/BAB/RBS/PBS/LDS search, diagnosing weak propagation or search pathologies, reasoning about set/float/resource-style models, or integrating Gecode into CMake projects."
---

# Gecode

Use this skill as the entry point for any Gecode-specific task. Carry the universal Gecode runtime model in mind for every response, then load only the additional reference files needed for the task.

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
- Model as `class M : public Space`, implement copy constructor and virtual `copy()`, and update variable arrays with `x.update(home, s.x)` during cloning.
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

## Routing
- Read `references/modeling.md` for model structure, variables, constraints, branching setup, and built-in search configuration.
- Read `references/modeling-cookbook.md` when the user needs concrete recipe-style guidance for channeling, symmetry, branching, optimization setup, or choosing globals versus decompositions.
- Read `references/debugging-workflow.md` for weak propagation, exploding search trees, stale choices, recomputation bugs, memory growth, or tracing/profiling workflow.
- Read `references/set-and-float-modeling.md` for set-variable modeling, float-specific caveats, or mixed-domain modeling.
- Read `references/scheduling-patterns.md` for cumulative/resource-style models, sequencing/order constraints, and scheduling-oriented branching or symmetry choices.
- Read `references/propagator-implementation.md` for custom propagator design, posting, propagation lifecycle, advisors, and rewriting.
- Read `references/brancher-implementation.md` for custom branchers, choices, commits, archiving, and NGL support.
- Read `references/memory-handling.md` for space/region/heap allocation, handles, clone footprint, and disposal obligations.
- Read `references/search-engines.md` for using and tuning built-in engines such as `DFS`, `BAB`, `LDS`, restart, and portfolio search.
- Read `references/search-engine-implementation.md` for custom engine orchestration, recomputation strategy, LAO, and completeness invariants.
- Read `references/cmake-consumption.md` for `find_package(Gecode CONFIG)`, target usage, version checks, and vendored fallback patterns.
- Read `references/general-knowledge.md` only for broad conceptual explanations, tracing/observability guidance, or staged model-improvement workflow discussion that goes beyond the always-on mental model.

## Operating Rules
- Read only the reference file or files needed for the current task.
- Combine references only when the task genuinely crosses boundaries, such as a custom propagator with nontrivial memory strategy or a search-engine bug tied to choice compatibility.
- Prefer the narrowest useful reference set first, then expand if the user asks for adjacent concerns.
- Keep answers Gecode-specific. If the request is generic CMake, generic C++ memory, or generic CP theory without a real Gecode angle, do not over-apply this skill.
- Use this `SKILL.md` alone for broad explanations, initial modeling guidance, and many runtime/debugging answers before reaching for extra references.

## Reference Index
- `references/general-knowledge.md`: advanced observability, staged improvement workflow, and broad conceptual framing beyond the always-on core.
- `references/modeling.md`: variable selection, globals, reification, symmetry, branching, and search setup in ordinary models.
- `references/modeling-cookbook.md`: concrete modeling recipes for globals, channeling, symmetry, branching, optimization, and “propagation versus search” decisions.
- `references/debugging-workflow.md`: symptom-driven diagnosis for weak models, stale choices, recomputation issues, performance pathologies, and observability tooling.
- `references/set-and-float-modeling.md`: set-variable patterns, float-specific caveats, and mixed-domain modeling reminders.
- `references/scheduling-patterns.md`: scheduling/resource modeling patterns, sequencing constraints, and search guidance for schedule-like problems.
- `references/propagator-implementation.md`: actor lifecycle, `ExecStatus`, propagation conditions, iterators, advisors, and rewrite patterns.
- `references/brancher-implementation.md`: `status`, `choice`, `commit`, archive compatibility, NGLs, and heuristic encoding.
- `references/memory-handling.md`: memory areas, lazy vs eager allocation, shared/local handles, and `AP_DISPOSE` discipline.
- `references/search-engines.md`: engine selection, restart/portfolio tradeoffs, no-goods, parallel semantics, and completeness caveats.
- `references/search-engine-implementation.md`: custom engine state, replay/recomputation, ownership, branch-and-bound integration, and invariants.
- `references/cmake-consumption.md`: package-config integration, exported targets, component selection, and fetch fallback.
