# User guide

TAMOS ships as a Claude Code plugin. This guide covers installing it, what you
get, how the layers reach an agent, how to validate the guide, and how to cut a
release.

## Install

The repo is its own marketplace, so one repo gives you both.

```
/plugin marketplace add Battle-Creek-LLC/tamos   # or the full git URL
/plugin install tamos@tamos
```

Pin a version by installing from a tagged release; a git-based source pins to
the tag/SHA. Update with `/plugin marketplace update tamos`.

## What you get

| Component | Delivered as | Loads |
|-----------|--------------|-------|
| 5 adversarial validators (`agents/`) | plugin subagents (auto-discovered) | when you run validation |
| `/tamos-validate` (`commands/`) | slash command | on demand / in CI |
| style modules (`core`, registers, `artifacts/`) | reference files in the plugin | pulled by producing skills |

> A plugin does **not** auto-inject text into your CLAUDE.md. The always-on
> layer is opted in by import (next section). Everything else loads on demand.

## Turn on the always-on layer

The enforced layer (`core.md` + `register-declarative.md` + the `AGENT-STYLE.md`
registry) is the high-ROI piece and applies to every turn. Import it once into
your **global** `~/.claude/CLAUDE.md` so it lives in one source and edits
propagate:

```
@${CLAUDE_PLUGIN_ROOT}/core.md
@${CLAUDE_PLUGIN_ROOT}/register-declarative.md
@${CLAUDE_PLUGIN_ROOT}/AGENT-STYLE.md
```

Do **not** copy these files into each project's CLAUDE.md — that re-creates the
drift TAMOS exists to prevent. Import, never paste. See `docs/runtime.md` for
the full provisioning/enforcement model.

## Pull an artifact module

When producing a specific artifact, the producing skill reads its module as
step 0 (the runtime's "pull to provision"). To wire a skill, point it at the
module path, e.g. a review skill reads
`${CLAUDE_PLUGIN_ROOT}/artifacts/pr-review.md` before drafting. Where no skill
owns the action, an agent consults `AGENT-STYLE.md`, matches `APPLIES WHEN`, and
opens the module itself.

## Validate the guide

Run the five adversarial validators against the enforced layer:

```
/tamos-validate                      # all enforced-layer files
/tamos-validate artifacts/pr-review.md   # a specific file
```

It prints a per-validator summary and a final `TAMOS-VALIDATE: PASS|FAIL` line.
Run this whenever you edit `core.md`, a register, or an artifact module — that
is the only time the validators need to run.

## CI/CD

Two workflows under `.github/workflows/`:

- **`validate.yml`** (on every PR):
  - `structure` — `claude plugin validate . --strict`. Cheap, no API key.
  - `guide-review` — runs `/tamos-validate` on changed enforced-layer files
    only. Costs API tokens and a few minutes, so it is path-filtered and skips
    PRs that don't touch the guide.
- **`release.yml`** (on a `v*` tag): validates structure, checks the tag matches
  `plugin.json` `version`, and publishes a GitHub release.

**Required secret:** `ANTHROPIC_API_KEY` (repo settings → Secrets) for the
`guide-review` job. The structural and release validation steps don't need it.

If you'd rather not spend tokens in CI, delete the `guide-review` job and run
`/tamos-validate` locally before pushing — the structural gate still protects
the plugin manifest.

## Cut a release

1. Bump `version` in `.claude-plugin/plugin.json` (and the marketplace entry).
2. Commit, then tag: `git tag v0.2.0 && git push --tags`.
3. `release.yml` validates and publishes. Consumers pinned to a tag get the new
   version on `/plugin marketplace update`.

## Add a module

See `docs/contributing.md` for the fixed four-slot artifact shape and the
cascade rules. After adding a module, run `/tamos-validate` before opening the PR.
