# Gecode Skills

Canonical skill repository for the umbrella Gecode AI agent skill.

[Gecode](https://www.gecode.org/) 6.4.0 is the current knowledge and compatibility baseline. Repository releases use an independent semantic version because the skill can evolve between Gecode releases.

Install with:

```bash
npx skills add Gecode/gecode-skills
```

List available skills:

```bash
npx skills add Gecode/gecode-skills --list
```

Install a single skill:

```bash
npx skills add Gecode/gecode-skills --skill gecode
```

## Available Skill

- `gecode`

The skill routes internally to focused reference documents for:
- Gecode architecture and runtime semantics
- modeling and search setup
- set-variable, float-variable, and scheduling models
- custom propagators
- custom branchers
- memory management
- built-in search engines
- custom search engine implementation
- downstream CMake consumption

## Versioning and distribution

- GitHub releases are immutable snapshots of this repository, starting with `v1.0.0`.
- The standard `npx skills add Gecode/gecode-skills` command installs from the public repository's default branch.
- A new Gecode release normally causes a minor skill release when it adds or changes substantial guidance; corrections and refinements are patch releases.
- Major releases are reserved for incompatible skill structure or behavior changes.
- skills.sh discovers the public skill automatically after an installation through the `skills` CLI; there is no separate package upload.

## Contributing

### Verification

Run the structural validator and repository regression tests locally:

```bash
python scripts/validate_skills.py
python -m unittest discover -s tests -v
```

The CI smoke test also checks that the skill is discoverable by the skills CLI:

```bash
npx --yes skills add . --list
```

### Skill structure

The skill must be under:

- `skills/<skill-name>/SKILL.md`

Optional metadata for UIs can be added at:

- `skills/<skill-name>/agents/openai.yaml`

### Required frontmatter

`SKILL.md` must include YAML frontmatter with:

- `name`
- `description`

The `name` must match the directory name (`<skill-name>`).

### Release bump labels

Auto-release determines semver bump from PR labels:

- `release:major` -> major bump
- `release:minor` -> minor bump
- no label -> patch bump

## Release policy

Releases are controlled by `.release-policy.yml`.

- Initially: `auto_release: false`
- This means pushes to `main` do **not** auto-release.
- Manual release via workflow dispatch is enabled.

To enable auto-release later, set:

```yaml
auto_release: true
```

and merge that change with maintainer review.
