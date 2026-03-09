# Gecode Skills

Repository infrastructure for publishing Gecode-focused AI agent skills.

This branch sets up validation, CI, and release automation. It does not introduce a published skill yet.

## Infrastructure

Included here:

- GitHub Actions for validation and release publishing
- semver/version helper scripts
- release policy gating through `.release-policy.yml`
- generic skill validation that works before any skill is added

## Future Skill Layout

Skills will live under:

- `skills/<skill-name>/SKILL.md`

## Contributing

### Skill structure

Each skill must be under:

- `skills/<skill-name>/SKILL.md`

Optional metadata for UIs can be added at:

- `skills/<skill-name>/agents/openai.yaml`

### Required frontmatter

Each `SKILL.md` must include YAML frontmatter with:

- `name`
- `description`

The `name` must match the directory name (`<skill-name>`).

### Release bump labels

Auto-release determines semver bump from PR labels:

- `release:major` -> major bump
- `release:minor` -> minor bump
- no label -> patch bump

## Release Policy

Releases are controlled by `.release-policy.yml`.

- Initially: `auto_release: false`
- This means pushes to `main` do **not** auto-release.
- Manual release via workflow dispatch is enabled.

To enable auto-release later, set:

```yaml
auto_release: true
```

and merge that change with maintainer review.
