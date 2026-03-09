# Gecode Skills

Canonical skill repository for the umbrella Gecode AI agent skill.

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
- custom propagators
- custom branchers
- memory management
- built-in search engines
- custom search engine implementation
- downstream CMake consumption

## Contributing

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
