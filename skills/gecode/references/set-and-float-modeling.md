# Gecode Set and Float Modeling

## Set Variables
- Model set variables when membership, subset, cardinality, or partition structure is the natural shape of the problem.
- Keep lower and upper bounds on sets tight; loose envelope sets behave like wide integer domains and weaken propagation.
- Use cardinality constraints aggressively when the set size matters; they often provide the missing structure for branching and propagation.
- Channel set decisions to integer or Boolean views only when another constraint family becomes substantially stronger through that representation.

## Float Variables
- Treat float models differently from integer models: propagation is approximate, and branching intuition from integer domains often does not transfer directly.
- Use float variables when the problem is genuinely continuous or mixed continuous/discrete, not just because integer scaling feels inconvenient.
- Be careful with no-good assumptions and search behavior: not all branchers or search features available for integer models carry over the same way for float-heavy models.
- Inspect tolerances, bounds, and objective semantics before concluding that a float model is “wrong.”

## Mixed-Domain Reminders
- Keep the reason for each domain type explicit; mixed-domain models become hard to debug when variables exist only as translation artifacts.
- Channel across domains only when it enables stronger pruning, clearer objectives, or better branching.
- Re-check clone footprint and cache layout when mixed-domain support data becomes large.

## When Integer Intuition Fails
- Do not assume set or float domains shrink in the same way that integer intervals do.
- Do not assume the strongest-looking branching is best; mixed-domain models often need problem-structure-aware branching more than aggressive generic branching.
- When propagation quality is hard to judge, compare behavior on a tiny instance with tracing or profiling before scaling up.
