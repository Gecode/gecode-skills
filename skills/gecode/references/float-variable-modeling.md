# Gecode Float-Variable Modeling

## Orientation

- Use float variables for genuinely continuous or mixed continuous/discrete quantities where interval propagation matches the intended semantics.
- Treat every float domain as an interval enclosure, not as an exact mathematical real or a finite enumeration of candidate values.
- Keep initial intervals tight and make the required numerical resolution explicit. Wide intervals can make both propagation and interval-splitting search ineffective.
- Prefer scaled integers when the model requires exact discrete increments and safe scaling fits within integer limits.

## Gecode Mechanics

- Represent float decisions with `FloatVar`, `FloatVarArray`, and `FloatVarArgs`; inspect `min()`, `max()`, `med()`, `size()`, and `domain()` rather than assuming a single scalar value.
- Post direct relations with `rel(...)`, linear relations with `linear(...)`, and arithmetic expressions through MiniModel. Use `channel(...)` when a float variable must equal an integer or Boolean variable.
- Expect interval arithmetic and outward rounding. A propagated result encloses possible real values; it is not evidence that every point in the interval is a solution.
- Branch by splitting intervals, for example with `FLOAT_VAL_SPLIT_MIN()` or `FLOAT_VAL_SPLIT_MAX()`, combined with a `FLOAT_VAR_*` selector for arrays.
- Use `FloatMinimizeSpace` or `FloatMaximizeSpace` for float objectives. Choose the improvement `step` deliberately: it controls how much better a later solution must be.

## Decision Guidance

- Use float variables when nonlinear relations, transcendental expressions, or continuous bounds are central and interval reasoning is acceptable.
- Use an integer channel when an otherwise continuous model contains an exact integral decision. Keep the float view only if it enables useful float constraints.
- Choose split direction and variable order from model structure. Branch first on intervals that drive feasibility or the objective rather than splitting every float uniformly.
- Report solution intervals or a documented representative such as `med()`. Tie stopping and presentation precision to the domain widths the application accepts.

## Pitfalls

- Do not compare float results as though they were exact point values; inspect interval bounds and tolerances.
- Do not assume integer branching intuition transfers unchanged. Float value branching partitions an interval rather than selecting from a finite domain.
- Do not use interval-valued linear coefficients that straddle zero; `linear(...)` rejects mixed-sign `FloatVal` coefficients.
- Do not call `val()` until the variable is assigned to a singleton interval.
- Do not choose a zero optimization step by habit when the application requires a meaningful minimum improvement.
