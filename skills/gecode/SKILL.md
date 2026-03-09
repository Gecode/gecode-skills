---
name: gecode
description: "Gecode architecture, modeling, propagators, branchers, memory management, search engine usage and implementation, recomputation/cloning behavior, and downstream CMake consumption. Use for any materially Gecode-specific task: building or refining models, implementing custom constraints or branchers, tuning DFS/BAB/RBS/PBS/LDS search, debugging solver behavior, reasoning about space memory/lifecycle semantics, or integrating Gecode into CMake projects."
---

# Gecode

Use this skill as the entry point for any Gecode-specific task. Keep the body lean: route to the relevant reference file, load only what the task needs, and avoid pulling unrelated topic docs into context.

## Routing
- Start with `references/general-knowledge.md` when the task is broad, diagnostic, or about solver/runtime semantics.
- Read `references/modeling.md` for model structure, variables, constraints, branching setup, and built-in search configuration.
- Read `references/propagator-implementation.md` for custom propagator design, posting, propagation lifecycle, advisors, and rewriting.
- Read `references/brancher-implementation.md` for custom branchers, choices, commits, archiving, and NGL support.
- Read `references/memory-handling.md` for space/region/heap allocation, handles, clone footprint, and disposal obligations.
- Read `references/search-engines.md` for using and tuning built-in engines such as `DFS`, `BAB`, `LDS`, restart, and portfolio search.
- Read `references/search-engine-implementation.md` for custom engine orchestration, recomputation strategy, LAO, and completeness invariants.
- Read `references/cmake-consumption.md` for `find_package(Gecode CONFIG)`, target usage, version checks, and vendored fallback patterns.

## Operating Rules
- Read only the reference file or files needed for the current task.
- Combine references only when the task genuinely crosses boundaries, such as a custom propagator with nontrivial memory strategy or a search-engine bug tied to choice compatibility.
- Prefer the narrowest useful reference set first, then expand if the user asks for adjacent concerns.
- Keep answers Gecode-specific. If the request is generic CMake, generic C++ memory, or generic CP theory without a real Gecode angle, do not over-apply this skill.
- When a task spans modeling and runtime behavior, anchor the explanation in `references/general-knowledge.md` and then pull in the specialized topic doc.

## Reference Index
- `references/general-knowledge.md`: spaces, propagation/search lifecycle, cloning, recomputation, choices, and debugging mental model.
- `references/modeling.md`: variable selection, globals, reification, symmetry, branching, and search setup in ordinary models.
- `references/propagator-implementation.md`: actor lifecycle, `ExecStatus`, propagation conditions, iterators, advisors, and rewrite patterns.
- `references/brancher-implementation.md`: `status`, `choice`, `commit`, archive compatibility, NGLs, and heuristic encoding.
- `references/memory-handling.md`: memory areas, lazy vs eager allocation, shared/local handles, and `AP_DISPOSE` discipline.
- `references/search-engines.md`: engine selection, restart/portfolio tradeoffs, no-goods, parallel semantics, and completeness caveats.
- `references/search-engine-implementation.md`: custom engine state, replay/recomputation, ownership, branch-and-bound integration, and invariants.
- `references/cmake-consumption.md`: package-config integration, exported targets, component selection, and fetch fallback.
