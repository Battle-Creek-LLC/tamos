# J8 — routing efficacy (does the module get LOADED at all?)

## Why this is not J7

J7 pre-concatenated module text into the prompt and measured whether the module
*helped once loaded*. It bypassed routing by construction. J8 measures the step
before: does a natural user prompt cause the module to reach context at all?
A module that never loads has no efficacy to measure.

## Research questions

1. Baseline: with TAMOS installed as it ships today, how often does the wanted
   module load on a natural prompt?
2. Does one-skill-per-module (rec A) raise it?
3. Does a SessionStart hook injecting the always-on layer (rec B) raise it?
4. Does the documented install step (`@${CLAUDE_PLUGIN_ROOT}/core.md` in
   `~/.claude/CLAUDE.md`) actually load the always-on layer?

## Independent variable — condition (4 levels)

- `baseline`  — TAMOS as shipped: the single `tldr` skill, no always-on layer.
- `skills`    — one skill per module (tldr, commit-message, pr-review, status-update),
                each skill's body Reads its artifact module. Descriptions rewritten.
- `hook`      — shipped `tldr` skill + SessionStart hook injecting
                core.md + register-declarative.md + AGENT-STYLE.md.
- `both`      — skills + hook.

## Control variables

- Model: session default (Opus 4.8), one call per cell, no conversation history.
- Invocation: `claude -p <prompt> --output-format stream-json --dangerously-skip-permissions`,
  cwd = the condition dir. Conditions are separate dirs so `.claude/` cannot leak.
- Fixtures: 6 fixed natural prompts (`fixtures.json`), 3 tldr phrasings + commit/review/status.

## Dependent variable

`loaded` (binary, deterministic, parsed from the transcript): the wanted module
reached context by EITHER path —
- the `Skill` tool fired with the wanted skill, OR
- `Read`/`Grep` touched `artifacts/<wanted>.md`.

Both paths count because TAMOS documents both (skill-loaded and agent-pulled).

## Results

| condition | loaded | n |
|-----------|--------|---|
| baseline  | 1/6 (17%) | 6 |
| skills    | 6/6 (100%) | 6 |
| hook      | 6/6 (100%) | 6 |
| both      | 6/6 (100%) | 6 |

Replicated on the tldr fixtures only (4 trials each, description is the only
delta between conditions since routing sees description only):

| fixture         | prompt                            | baseline | skills |
|-----------------|-----------------------------------|----------|--------|
| tldr_summarize  | "summarize: …"                    | 0/4      | 4/4    |
| tldr_explicit   | "tl;dr this: …"                   | 1/4      | 4/4    |
| tldr_natural    | "can you shorten this down for me?" | 4/4    | 4/4    |
| **total**       |                                   | **5/12 (41%)** | **12/12 (100%)** |

## Findings

- **F1.** The shipped `tldr` description lists `summarize`, `condense`, `"tl;dr"`
  verbatim, yet "summarize:" fired it 0/4 and "tl;dr this:" 1/4. Verbatim keyword
  presence in the description does not drive routing. Rewriting the description
  (routing sees description only) took it 41% → 100%.
- **F2.** `hook` reached 6/6 with **no skills** for commit/review/status — the agent
  read the registry and pulled the module itself. The registry works as designed;
  it just never loads, because the install step is broken (F3).
- **F3.** [verified, no tools used] In `~/.claude/CLAUDE.md`:
  `@${CLAUDE_PLUGIN_ROOT}/core.md` → does NOT expand, loads nothing, fails silently.
  `@/abs/path/core.md` and `@~/path/core.md` → both work.
  A user following `docs/user-guide.md` verbatim gets an inert TAMOS.
- **F4.** A SessionStart hook injecting the three always-on files works and needs
  no user hand-editing. [verified — probe returned core.md's first bullet]

## Causal chain (all links verified)

broken `@import` → always-on layer never loads → registry never loads → agent has
no map → never pulls any artifact module → and the one existing skill fires ~41%.

## Limitations

- **Clean room.** Empty project dirs, no competing codebase context, single-turn.
  Real sessions have a large working context contending for attention; the 100%
  figures are almost certainly optimistic. Direction is `verified`; magnitude is `believed`.
- n=1 per cell for the non-tldr fixtures; only tldr is replicated (n=4).
- `loaded` is necessary, not sufficient — it does not measure whether the artifact
  got better. That is J7's question.
- Single model, single day, `--dangerously-skip-permissions`.
- Untrusted dirs (e.g. fresh `/tmp` repos) do not load `CLAUDE.md` at all; all
  reported runs are inside the trusted repo tree. Beware this confound when extending.

## Reproduce

```
python3 run.py baseline                              # baseline, all 6 fixtures
python3 run.py baseline,skills tldr_explicit,tldr_natural,tldr_summarize 4
python3 run.py skills,hook,both                      # all fixes
```
Results cache per (condition, fixture, trial) in `results/*.jsonl`; delete a file to re-run it.
