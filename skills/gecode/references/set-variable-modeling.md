# Gecode Set-Variable Modeling

## Orientation

- Use set variables when membership, subset, cardinality, partition, or coverage is the natural shape of a decision.
- Think of a set domain as two bounds: the greatest lower bound contains required elements, and the least upper bound contains every still-possible element.
- Tighten both element bounds and cardinality bounds early. A broad upper bound with unconstrained cardinality leaves many independent membership decisions for search.
- Channel to integer or Boolean variables only when another representation enables stronger constraints, clearer branching, or a simpler objective.

## Gecode Mechanics

- Represent decisions with `SetVar`, `SetVarArray`, and `SetVarArgs`. Construct each variable with a lower bound, an upper bound, and optional minimum and maximum cardinalities.
- Inspect `glbSize()`, `lubSize()`, `unknownSize()`, `cardMin()`, and `cardMax()` when diagnosing propagation or designing a brancher.
- Use `dom(...)` and `cardinality(...)` to restrict membership and size. Use `rel(...)` with relations such as `SRT_EQ`, `SRT_SUB`, `SRT_SUP`, and `SRT_DISJ`, and operations such as `SOT_UNION`, `SOT_DUNION`, `SOT_INTER`, and `SOT_MINUS`.
- Use structure-aware constraints such as `sequence(...)`, `atmostOne(...)`, `precede(...)`, and set `element(...)` when they match the model.
- Use `channel(home, bools, set)` for a Boolean membership view, or the integer/set and set/set channel overloads when the alternate view pays for its extra variables.
- Branch by choosing both a set variable and an unknown element. For example, `branch(home, sets, SET_VAR_SIZE_MIN(), SET_VAL_MIN_INC())` selects a small set domain and tries inclusion of its smallest unknown element first.

## Decision Guidance

- Prefer one `SetVar` over many Booleans when constraints reason about whole-set relations, cardinality, union, intersection, disjointness, or partition structure.
- Prefer Booleans when most constraints are propositional and no set global uses the combined membership structure. Channel both views when each side contributes substantial pruning.
- Use `SOT_DUNION` rather than ordinary union when disjointness is part of the semantics; stating both facts together can expose more structure.
- Select inclusion-first or exclusion-first branching according to expected set density. Choose variable selectors by unknown membership count or a problem-specific merit when array order is not informative.

## Pitfalls

- Do not confuse the greatest lower bound with a numeric minimum or the least upper bound with a numeric maximum; both are sets.
- Do not create illegal domains: the lower bound must be contained in the upper bound, and cardinality bounds must be compatible with both.
- Do not channel representations automatically. Extra variables and propagators must earn their clone footprint and propagation cost.
- Do not treat set branching like integer value assignment; each alternative normally includes or excludes one currently unknown element.
