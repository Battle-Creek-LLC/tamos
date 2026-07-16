# Changelog

Versions follow the plugin's `version` in `.claude-plugin/plugin.json`. Each
release is tagged `v<version>` and published by `.github/workflows/release.yml`.

## Upgrading

```
claude plugin marketplace update battle-creek    # refresh the catalog first,
                                                 # or update won't see the release
claude plugin update tamos@battle-creek
```

Then restart Claude Code, or run `/reload-plugins --force` in-session.

**Use `update`, not `install`.** On an existing install, `claude plugin install`
prints `"already installed"` and does nothing — you stay on the old version
believing you upgraded.

If TAMOS is not installed at all:

```
claude plugin marketplace add https://github.com/Battle-Creek-LLC/tamos.git
claude plugin install tamos@battle-creek
```

### Verify the upgrade

Check behaviour, not status text — `claude plugin list` reported `✘ failed to
load` for a v0.3.0 install that worked, and reports `✔ enabled` for configs whose
hook never fires. Run this in any directory:

```
claude -p "Reply with the first bullet of Tier 0 Core if visible, else exactly NOCONTEXT"
```

| Result | Meaning |
|--------|---------|
| `One name per thing. Pick a term, reuse it.` with **no tool calls** | pass — the hook injected the always-on layer |
| `NOCONTEXT` | fail — the `SessionStart` hook did not fire |
| correct answer **but a `Read` tool was used** | fail — the agent read `core.md` itself. That is not the hook working, and it won't happen in a real session where nothing points at the file. |

Then confirm 9 `tamos:` skills register in a session: `tldr`, `pr-review`,
`commit-message`, `status-update`, `elicitation`, `spec-review`,
`research-report`, `code-comment`, `tamos-validate`. Fewer means a partial load.

### Upgrading from v0.2.0 or earlier

Delete any lines like these from `~/.claude/CLAUDE.md`:

```
@${CLAUDE_PLUGIN_ROOT}/core.md
@${CLAUDE_PLUGIN_ROOT}/register-declarative.md
@${CLAUDE_PLUGIN_ROOT}/AGENT-STYLE.md
```

They never worked — `${CLAUDE_PLUGIN_ROOT}` does not expand in a CLAUDE.md
`@import`, so they silently loaded nothing. v0.3.0 replaced them with a
`SessionStart` hook that needs no hand-editing. If you have no
`~/.claude/CLAUDE.md`, there is nothing to clean up.

---

## v0.3.1

Fixes a v0.3.0 install reporting itself broken while working correctly.

- **`claude plugin list` showed `✘ failed to load`.** `plugin.json` declared
  `"hooks": "./hooks/hooks.json"` for a file that is already auto-discovered.
  With both present the hook fires and the skills register, but the loader
  reports failure. Dropping the key: `✔ enabled`, hook still fires, 9 skills
  still register.
- Documents both `hooks/hooks.json` traps in `docs/runtime.md`. They fail
  silently in opposite directions, and both pass `claude plugin validate
  --strict`:

  | Mistake | Symptom |
  |---------|---------|
  | events not wrapped in a `hooks` key | validates clean, **never runs** |
  | also declared in `plugin.json` | runs fine, **reports "failed to load"** |

## v0.3.0

Fixes the always-on layer never loading, and gives every artifact module a
trigger. Measured recall of the wanted module: **34% → 97%**, precision 100%.

### Fixed

- **The documented install step never worked.** `docs/user-guide.md` told users
  to put `@${CLAUDE_PLUGIN_ROOT}/core.md` in `~/.claude/CLAUDE.md`. That variable
  does not expand in a CLAUDE.md import — it is available to hook commands only —
  so the always-on layer silently loaded nothing for every user who followed the
  guide. Without core, the declarative register, or the registry in context, an
  agent had no map to pull artifact modules from.
- `docs/runtime.md` referenced a `battle-review` skill that does not exist.
- `artifacts/code-comment.md` declared `APPLIES WHEN: writing an inline comment`
  — a trigger nothing implements. Narrowed to `asked for an inline comment` so
  the module, the registry and the skill agree.

### Added

- **`SessionStart` hook** (`hooks/hooks.json`) injects `core.md`,
  `register-declarative.md` and `AGENT-STYLE.md`. Installing the plugin turns the
  always-on layer on; no hand-editing, and it follows plugin updates.
- **A producing skill per artifact module** (8), described in *intent* language
  ("does this look ok?") rather than *artifact* language ("producing a code
  review"). Skill routing only ever sees the description.
- **`docs/use-cases.md`** — what each module governs, the words that engage it,
  measured per-module reliability, and the known gap.

### Changed

- `core.md` and the registry now name the `SessionStart` hook as the always-on
  mechanism, replacing "inline into CLAUDE.md".
- `docs/runtime.md`'s "one decision" reworked. Provisioning a *universal* layer
  was never a pull problem — nothing about it is task-specific. `SessionStart`
  fires once per session, not per tool call, so it can carry the layer without
  paying per turn.
- `.github/workflows/validate.yml`: `guide-review` staged the repo's own command
  and validators into `.claude/` (they ship as plugin components, but the plugin
  is not installed in CI, so `/tamos-validate` was an unknown command and the job
  failed before reaching a verdict). Added a fail-fast when `ANTHROPIC_API_KEY`
  is unset.

### Known gap

`code-comment` engages when **you ask** for a comment. Comments the agent writes
unprompted mid-edit are still governed only by the always-on layer — a skill
fires on a request, and there is no request. Needs a `PostToolUse` hook on
Edit/Write; not built. See `docs/use-cases.md`.

### Measurements

38 asks + 16 decoys against the shipped plugin in a live repo, plus 224 sessions
across the configurations that produced the design. Method, harness and caveats:
`.exp/routing/`.

| | v0.2.0 | v0.3.0 |
|---|--------|--------|
| recall | 13/38 — 34% | 37/38 — 97% |
| precision | 100% | 100% (0/16 false fires) |
| cost | $0.090/turn | $0.117/turn |

By phrasing register: jargon 4/10 → 10/10, natural 4/12 → 12/12, oblique 3/10 →
10/10, embedded 2/6 → 5/6.

Direction is `verified`; magnitudes are `believed` — n=2 per fixture, one model,
and the prompts were written by the author of the fix.

## v0.2.0

- `artifacts/tldr.md` and the `tldr` producing skill.
- Efficacy A/B of the tldr module against control and core-only conditions (J7).

## v0.1.0

- Initial release: the tier cascade (`core.md`, both registers, `AGENT-STYLE.md`),
  artifact modules for pr-review, spec-review, commit-message, research-report,
  status-update, code-comment and elicitation, the five adversarial validators in
  `agents/`, and `/tamos-validate`.
