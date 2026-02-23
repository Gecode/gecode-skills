---
name: gecode-cmake-consumption
description: "Consume Gecode from CMake using exported package config (`find_package(Gecode CONFIG)`), aggregate/component targets, version checks, and source-fetch fallback patterns. Use when integrating Gecode into downstream CMake projects or migrating custom `FindGecode.cmake` logic. Assume Gecode 6.3.0 or newer."
---

# Gecode CMake Consumption

## Core
- Prefer config-package consumption: `find_package(Gecode CONFIG REQUIRED)`.
- Link downstream targets to `Gecode::gecode` unless explicit component granularity is required.
- Require `Gecode_VERSION >= 6.3.0`; use package version checks rather than parsing `gecode/support/config.hpp`.
- Hint package location with `Gecode_ROOT` or `CMAKE_PREFIX_PATH`.
- Keep `cmake_minimum_required(VERSION 3.21)` or newer for parity with Gecode's build.

## Canonical Patterns
- Minimal integration:
  ```cmake
  find_package(Gecode CONFIG REQUIRED)
  target_link_libraries(app PRIVATE Gecode::gecode)
  ```
- Component-specific integration:
  ```cmake
  find_package(Gecode CONFIG REQUIRED COMPONENTS driver)
  target_link_libraries(app PRIVATE Gecode::gecodedriver)
  ```
- Version guard:
  ```cmake
  if(SOME_STRICT_OPTION AND Gecode_VERSION VERSION_LESS "6.3.0")
    message(FATAL_ERROR "Gecode >= 6.3.0 required, found ${Gecode_VERSION}")
  endif()
  ```

## Dependency Resolution Workflow
- Try installed package first via `find_package(Gecode CONFIG QUIET)` when optional discovery is desired.
- If not found and project policy allows vendoring, use `FetchContent` to obtain Gecode source and call `FetchContent_MakeAvailable(...)`.
- Set Gecode cache options before `FetchContent_MakeAvailable(...)` to limit dependency surface (for example disable `GECODE_ENABLE_GIST`, examples, tests, or optional modules).
- Require `TARGET Gecode::gecode` after resolution; fail fast with actionable error text if absent.
- Mark Gecode target as `SYSTEM` in strict-warning projects to isolate third-party headers from local warning policy.
- For source-pinned fallback builds, prefer stable release tags or commits over long-lived feature branches.
- For migration away from custom discovery modules, remove manual imported-target composition and library probing once package config is the baseline path.
- Keep strict-version toggles if desired, but enforce them against `Gecode_VERSION`.

## Pitfalls
- Calling `find_package(Gecode REQUIRED)` without `CONFIG` and accidentally resolving old/module-mode shims.
- Assuming optional components exist without checking enabled modules in the installed build.
- Mixing custom imported-target composition with package-provided targets in the same code path.
- Parsing headers for version when package metadata already provides `Gecode_VERSION`.
