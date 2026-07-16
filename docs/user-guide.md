# User guide

TAMOS ships as a Claude Code plugin. This guide covers installing it, what you
get, how the layers reach an agent, how to validate the guide, and how to cut a
release.

## Install

The repo is its own marketplace, so one repo gives you both.

```
/plugin marketplace add Battle-Creek-LLC/tamos   # or the full git URL
/plugin install tamos@battle-creek
```

Pin a version by installing from a tagged release; a git-based source pins to
the tag/SHA. Update with `/plugin marketplace update battle-creek`.

## What you get

| Component | Delivered as | Loads |
|-----------|--------------|-------|
| always-on layer (`core`, `register-declarative`, `AGENT-STYLE`) | `SessionStart` hook | every session, automatically |
| 8 producing skills (`skills/`) | plugin skills, one per artifact module | when you ask for that artifact |
| 5 adversarial validators (`agents/`) | plugin subagents (auto-discovered) | when you run validation |
| `/tamos-validate` (`commands/`) | slash command | on demand / in CI |
| artifact modules (`artifacts/`) | reference files | pulled by the producing skill |

> A plugin cannot inject text into your CLAUDE.md — but its `SessionStart` hook
> can inject context directly, which is how the always-on layer arrives. Nothing
> needs hand-editing.

See `docs/use-cases.md` for what each skill governs and the words that engage it.

## The always-on layer

The enforced layer (`core.md` + `register-declarative.md` + the `AGENT-STYLE.md`
registry) applies to every turn. **Installing the plugin turns it on** — a
`SessionStart` hook (`hooks/hooks.json`) injects the three files at the start of
every session. No hand-editing, and it follows plugin updates.

> **Upgrading from 0.2.0 or earlier:** delete these lines from your
> `~/.claude/CLAUDE.md` — they never worked. `${CLAUDE_PLUGIN_ROOT}` does not
> expand in a CLAUDE.md `@import`, so they silently loaded nothing:
> ```
> @${CLAUDE_PLUGIN_ROOT}/core.md            # <- delete: expands to nothing
> @${CLAUDE_PLUGIN_ROOT}/register-declarative.md
> @${CLAUDE_PLUGIN_ROOT}/AGENT-STYLE.md
> ```
> The hook replaces them. If you prefer an import, only absolute (`@/abs/path`)
> or home-relative (`@~/path`) forms resolve.

Do **not** copy these files into each project's CLAUDE.md — that re-creates the
drift TAMOS exists to prevent. See `docs/runtime.md` for the full
provisioning/enforcement model.

The layer costs roughly +$0.03 and +1s per turn, including turns that have
nothing to do with TAMOS. That is the rent for calibrated prose on every output.
To opt out, disable the hook in `hooks/hooks.json`; the skills still load their
modules on request. Routing numbers: `docs/use-cases.md`.

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
