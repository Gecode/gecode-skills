# Gecode General Knowledge

## Advanced Framing
- Use groups and tracing for observability and selective control.
- Improve models in loops: baseline, stronger propagation, better branching, then tuned search.
- Measure with nodes, time, and restarts, not runtime alone.
- Treat symmetry handling as a first-class design concern, not post-processing.

## Conceptual Pitfalls
- Assuming parallel search preserves sequential solution order or runtime profile.
- Assuming one modeling pass is enough; most nontrivial case studies need staged refinement.
