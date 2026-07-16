# J9 — routing usability: test plan

Supersedes J8's design. J8 established the causal chain but measured only
**recall**, in a clean room. J9 closes both holes.

## The hole in J8

J8 scored `loaded = did the wanted module load?` A condition that fires the skill
on **every** prompt scores 100% and is terrible: it burns tokens, slows every
turn, and trains the user to distrust the trigger. J8 could not have detected
that. **Precision is the constraint that makes recall meaningful**, and J9's
negative controls are the point of the experiment, not a footnote.

## Research questions

| RQ | Question | Decides |
|----|----------|---------|
| RQ1 | Recall — does the wanted module load on realistic prompts? | whether a fix works |
| RQ2 | **Precision — does it stay OUT on lexical decoys?** | whether a fix is safe to ship |
| RQ3 | Does realistic context (real repo, mid-task) degrade routing vs clean room? | whether J8's 100% survives contact |
| RQ4 | Is `hook` alone as good as `hook+skills`? | scope: 15 lines vs 7 new skills |
| RQ5 | Does a `pairing` module change conversational turns? | whether rec D is real or hand-waving |

## Independent variables

**IV1 — condition (5 levels)**
- `baseline` — TAMOS as shipped (broken import, one skill, no always-on layer).
- `fixed_import` — always-on layer loaded via a *working* import (`@~/...`). Isolates the doc bug alone.
- `hook` — SessionStart injects core + register-declarative + AGENT-STYLE. No new skills.
- `skills` — one skill per module, rewritten descriptions. No hook.
- `both` — hook + skills.

**IV2 — context (2 levels)** — the fix for J8's clean-room caveat
- `clean` — empty dir, single turn. (J8's arena.)
- `loaded` — run inside a real repo, and `embedded` fixtures execute a `pre` turn
  that does real work first, so the trigger arrives mid-task with a working
  context competing for attention. This is the condition that matters.

## Fixtures (`fixtures-v2.json`, n=31)

| Group | n | want | Purpose |
|-------|---|------|---------|
| positive: tldr / commit / review / status | 15 | the module | recall across 4 phrasing registers |
| positive: elicitation / code-comment / spec-review | 4 | the module | coverage of untested modules |
| **negative controls** | **8** | `null` | **precision — lexical decoys** |
| pairing | 4 | `__pairing__` | RQ5 baseline |

**Phrasing registers** (the J8 finding was that register, not keyword, drives routing):
- `jargon` — "tl;dr this", "write a commit message"
- `natural` — "can you shorten this down", "what should I call this commit"
- `oblique` — "this is way too long", "anything wrong with this?"
- `embedded` — trigger arrives after a real `pre` turn ("ok now condense that")

**The negative controls are lexical decoys** — each contains the trigger word in a
context where the module is wrong: "**shorten** the timeout to 5s" (code edit),
"why is my **commit** failing" (debugging), "is there a **status** endpoint"
(code question), "**summarize** what this function does" (explaining code).
If a rewritten description over-fires, these catch it.

## Dependent variables

Mechanical (deterministic, parsed from transcript — no judge needed):
- `loaded` — wanted module reached context (Skill fired OR Read of `artifacts/<want>.md`).
- `fired_any` — any TAMOS module loaded. On negatives, `fired_any = false` is the win.
- `wrong_module` — a module loaded, but not the wanted one (e.g. pr-review on a commit ask).
- `cost_usd`, `duration_ms` — the tax a fix imposes on every turn.

Derived:
- **recall** = loaded / positives
- **precision** = 1 − (fired_any / negatives)
- Report both. Neither alone is a verdict.

Blind-judged (RQ5 only, and only if RQ1–4 pass):
- `quality` (1–5), `answer_first`, `certainty_tagged`, `no_throat_clearing`.
  Judge: cross-family, blind to condition, shuffled. (J7's judge design.)

## Hypotheses & kill criteria

- **H1** (recall): `hook` ≫ `baseline` on positives. J8 saw 6/6 vs 1/6 clean.
  *Kill:* if `loaded` under `loaded`-context < 60%, the pull model doesn't survive
  contact with a real working context → hooks must inject the module, not the map.
- **H2** (precision): all fix conditions hold precision ≥ 90% on the 8 decoys.
  *Kill:* any condition under 90% does not ship, regardless of recall. Over-firing
  is a worse failure than under-firing — it taxes every unrelated turn.
- **H3** (parsimony): `hook` ≈ `both` on recall AND precision.
  *If H3 holds → ship the hook alone and drop the 7 skills.* This is the cheapest
  outcome and J8 weakly supports it (hook hit 6/6 with no skills).
- **H4** (the doc bug): `fixed_import` ≫ `baseline` on its own.
  *If H4 alone clears the bar, the entire fix is a one-line docs change.*
- **H5** (pairing, RQ5): a `pairing` module beats no-module on `answer_first` +
  `certainty_tagged` with no cost/latency regression.
  *Kill (J7's rule): if H5 is null, the pairing module is hand-waving → drop it.*

## Staging — cheapest decisive test first

Measured basis: **$0.068/run, 8.2s median**, 6-way parallel.

| Stage | Runs | Cost | Answers | Gate |
|-------|------|------|---------|------|
| **S1 precision screen** | 5 cond × 8 neg × 2 trials = 80 | ~$5 | RQ2 / H2 | any condition <90% precision is cut here, before spending on recall |
| **S2 recall, loaded context** | survivors × 19 pos × 2 = ~76 | ~$5 | RQ1, RQ3 / H1, H4 | the number that decides ship / no-ship |
| **S3 parsimony** | hook vs both × 19 × 3 = 114 | ~$8 | RQ4 / H3 | decides scope: 15 lines or 7 skills |
| **S4 pairing A/B** | 2 arms × 4 × 4 = 32 + judge | ~$4 | RQ5 / H5 | only if S1–S3 pass |
| | **~300** | **~$21** | | **~10 min wall-clock** |

S1 runs first because it can *eliminate* candidates for ~$5. Never buy recall data
for a condition that is already disqualified on precision.

## Controls & known confounds

- **Trust confound (J8, nearly produced a false result):** untrusted dirs (fresh
  `/tmp` repos) do not load `CLAUDE.md` at all. All conditions must run inside a
  trusted tree. Verify with an inline-control probe per condition before trusting a run.
- **Cache confound (J8):** repeated `claude -p` in the same cwd with the same
  prompt appears to reuse context. Use a fresh dir per (condition, fixture, trial)
  or vary nothing but the fixture.
- **Tool-use confound (J8, nearly produced a false result):** an agent that *Reads*
  the file makes an import look like it worked. Any import test must assert
  `tools == []`.
- Model, day, and permission mode fixed across conditions.
- `wrong_module` is tracked separately so a fix cannot launder a miss into a hit.

## What this plan still will not tell you

- Whether the artifact is *better* once loaded — that is J7's question. J9 measures
  delivery only. A module can load 100% and still be bad prose.
- Multi-turn drift: whether a module loaded at turn 3 still governs turn 30.
- Real users. Every prompt here is written by the same person who wrote the fix,
  which is a bias no n fixes. Treat direction as `verified`, magnitude as `believed`.
