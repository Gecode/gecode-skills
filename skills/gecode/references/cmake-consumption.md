# Gecode CMake Consumption

## Core
- Prefer config-package consumption: `find_package(Gecode CONFIG REQUIRED)`.
- Link downstream targets to `Gecode::gecode` unless explicit component granularity is required.
- Current Gecode `main` is building version `6.4.0`; when targeting that line, require `Gecode_VERSION >= 6.4.0` and use package version checks rather than parsing `gecode/support/config.hpp`. If supporting older releases too, document `6.3.0` as the minimum compatibility policy separately.
- Hint package location with `Gecode_ROOT` or `CMAKE_PREFIX_PATH`.
- Keep `cmake_minimum_required(VERSION 3.21)` or newer for parity with Gecode's build.
- Use a C++17-capable compiler; current main exports that requirement through the Gecode targets.

## Key Patterns
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
  if(SOME_STRICT_OPTION AND Gecode_VERSION VERSION_LESS "6.4.0")
    message(FATAL_ERROR "Gecode >= 6.4.0 required, found ${Gecode_VERSION}")
  endif()
  ```
- Try installed package first with `find_package(Gecode CONFIG QUIET)` when discovery is optional.
- If the package is absent and project policy allows vendoring, use `FetchContent` and set Gecode cache options before `FetchContent_MakeAvailable(...)`. For a subproject, explicitly set `GECODE_INSTALL=OFF`, `GECODE_ENABLE_EXAMPLES=OFF`, and `BUILD_TESTING=OFF`; disable `GECODE_ENABLE_QT`, `GECODE_ENABLE_GIST`, or `GECODE_ENABLE_FLATZINC` when their dependencies are outside project scope.
- Require `TARGET Gecode::gecode` after resolution and fail fast with actionable error text if it is missing.
- Mark Gecode targets as `SYSTEM` in strict-warning projects to isolate third-party headers from local warning policy.
- For pinned source fallbacks, prefer stable release tags or commits over long-lived feature branches.
- When migrating away from custom discovery modules, remove manual imported-target composition and library probing once package config is the baseline.
- Keep strict version toggles if desired, but enforce them against `Gecode_VERSION`.

## Pitfalls
- Calling `find_package(Gecode REQUIRED)` without `CONFIG` and accidentally resolving old module-mode shims.
- Assuming optional components exist without checking enabled modules in the installed build.
- Mixing custom imported-target composition with package-provided targets in the same code path.
- Parsing headers for version when package metadata already provides `Gecode_VERSION`.
