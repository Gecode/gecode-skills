# Gecode General Knowledge

## Core
- Space is home for variables, propagators, branchers, and optimization order.
- Propagation is explicit: call `status()`.
- Search primitives are `status()`, `choice()`, `clone()`, `commit()`, and `constrain()`.
- Space status values are `SS_FAILED`, `SS_SOLVED`, and `SS_BRANCH`.
- Choice is a space-independent descriptor; alternatives are indexed `0..n-1`.
- Choice compatibility is clone-based: a choice is valid for its source space and clones.
- `choice()` invalidates previous choices for later `commit()` on that space.
- Clone only stable, non-failed spaces.
- Branchers run in posting order.
- Recomputation can be nondeterministic with weakly monotonic propagation while remaining sound and complete.

## Key Patterns
- Model as `class M : public Space`.
- Implement copy constructor and virtual `copy()`.
- In space cloning, clone variable arrays via `x.update(home, s.x)`; do not use a variable-array copy constructor.
- After `status()==SS_BRANCH`, compute `choice()` immediately.
- Seed the search engine with the model, then delete the seed model.
- Treat a solution as a space closure over member variables.
- Use groups and tracing for observability and selective control.
- Improve models in loops: baseline, stronger propagation, better branching, then tuned search.
- Measure with nodes, time, and restarts, not runtime alone.
- Treat symmetry handling as a first-class design concern, not post-processing.

## Pitfalls
- Assuming posting performs full propagation.
- Calling the `Space` copy constructor directly instead of `clone()`.
- Using stale choices after invalidating them with a later `choice()` call.
- Forgetting ownership and deletion of choices and returned solution spaces.
- Cloning unstable or failed spaces.
- Assuming parallel search preserves sequential solution order or runtime profile.
- Assuming one modeling pass is enough; most nontrivial case studies need staged refinement.
