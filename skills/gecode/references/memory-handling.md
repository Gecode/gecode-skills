# Gecode Memory Handling

## Core
- Memory areas are space, region, heap, and space freelists.
- `alloc`, `realloc`, and `free` follow C++ object lifecycle semantics.
- Space memory is reclaimed automatically on space deletion and fits stable-size actor data.
- Region is a temporary arena with implicit free on region destruction.
- Heap is for frequently resized or dynamic structures.
- Search memory profile favors pristine clones, so allocation timing matters.
- Shared handles point to cross-space or cross-thread shared heap objects with reference counting.
- Local handles point to per-space shared objects copied on cloning.

## Key Patterns
- Allocate fixed actor members in home space.
- Allocate resize-heavy buffers on the heap and free them in `dispose()`.
- Build heavy internal state lazily on first propagation when possible.
- Choose eager, lazy, or hybrid allocation based on clone footprint and expected hit rate.
- Use regions for short-lived iterators and temporary buffers.
- Call `Region::free()` at clear control-flow boundaries to maximize reuse.
- Use `SharedHandle` for immutable or global lookup data.
- Use `LocalHandle` for shared per-space mutable state.
- Use `IntSharedArray` or related shared arrays for read-only large data reused across clones.
- For brancher choices using heap buffers, pair allocation and free, and register `AP_DISPOSE`.
- Use `Region` for per-choice scratch arrays to avoid heap churn.

## Exception Safety and Fault Injection
- Treat allocation, actor-copy, `AP_DISPOSE` registration, and partial-clone failures as normal exception paths.
- Make custom `copy()` and `dispose()` logic leave both the source and partially constructed clone recoverable when an allocation throws.
- Current Gecode main provides the CMake-only `GECODE_ENABLE_FAULT_INJECTION` option and an isolated single-threaded `check-fault` suite; use it to exercise ownership and clone-recovery paths rather than relying only on successful allocations.

## Pitfalls
- Frequent resize in space memory causing fragmentation.
- Forgetting `home.notice(..., AP_DISPOSE)` for external or heap resources.
- Forgetting the matching `home.ignore(..., AP_DISPOSE)` in the dispose path.
- Assuming identical alignment guarantees across space, heap, and region memory.
- Leaking ownership assumptions across cloning boundaries.
- Allocating per-choice temporary arrays on the heap in hot paths.
