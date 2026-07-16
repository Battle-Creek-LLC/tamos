# J9 — results

144 sessions (64 precision + 80 recall), loaded context, fresh dir per cell. ~$12.

## S1 — precision (H2): PASS, all conditions

8 lexical decoys × 2 trials × 4 conditions = 64 runs. **Zero false fires anywhere.**
"shorten the timeout to 5s", "why is my commit failing", "is there a status
endpoint", "summarize what this function does" — none over-triggered.

H2 holds. Over-firing is not a risk; nothing is disqualified. Note the screen did
not discriminate between conditions, so it establishes a safety property rather
than a preference.

## S2 — recall (H1, H3): the clean room was lying

19 positive fixtures × 2 trials, real repo, `embedded` fixtures fire mid-task.

| condition | recall | vs J8 clean room |
|-----------|--------|------------------|
| baseline  | 13/38 — **34%** | (J8: 17%) |
| hook      | 28/38 — **73%** | J8: 100% |
| skills    | 30/38 — **78%** | J8: 100% |
| both      | 32/38 — **84%** | J8: 100% |

**H1 survives** (73% > the 60% kill line) — the pull model does survive contact
with a working context, but with a 16–27 point haircut. J8's 100% was an artifact
of the clean room, exactly as flagged.

**H3 is REJECTED.** `hook` (73%) is *not* equivalent to `both` (84%). The J8-based
guess that the hook alone might be sufficient — and that the 7 skills could be
dropped — is falsified by this data. Ship both.

## The headline: recall degrades as speech gets more natural

| condition | jargon | natural | oblique | embedded |
|-----------|--------|---------|---------|----------|
| baseline  | 4/10   | 4/12    | 3/10    | 2/6      |
| hook      | 10/10  | 8/12    | 6/10    | 4/6      |
| skills    | 9/10   | 9/12    | 8/10    | 4/6      |
| both      | **10/10** | **11/12** | **7/10** | **4/6** |

Best condition: 100% on "tl;dr this" / "write a commit message for this diff",
falling to 67% on "anything wrong with this?" and "ok that's a lot — condense it".

**TAMOS routes when you talk like a manual and misses when you talk like a person.**
That is the direct, quantified answer to "how do we encourage this style in
pairing / common speech": the trigger surface is tuned to jargon, and pairing is
conducted in oblique and embedded register.

## Per-module recall (fix conditions pooled) — the failure is concentrated

| module | recall | |
|--------|--------|--|
| tldr           | 24/24 — 100% | ✅ |
| status-update  | 18/18 — 100% | ✅ |
| commit-message | 23/24 — 95%  | ✅ |
| spec-review    | 5/6 — 83%   | ok |
| elicitation    | 7/12 — 58%  | ⚠️ |
| pr-review      | 12/24 — 50% | ⚠️ |
| **code-comment** | **1/6 — 16%** | ❌ dead on arrival |

"TAMOS doesn't load" is not uniform. Three modules carry it; three are failing.

- **`code-comment` (16%)** is a mechanism mismatch, not a wording problem. It should
  fire *while the agent writes code* — but nothing consults a prose-style module
  mid-edit. A skill cannot fix this; it needs a different hook (PostToolUse on
  Edit/Write) or to live in the always-on layer.
- **`pr-review` (50%)** misses precisely on `oblique` and `embedded` — "anything
  wrong with this?", "go back over what you just wrote and give me your honest
  take". That is how review is actually requested while pairing. Its `APPLIES WHEN`
  ("producing a code review (any diff, PR, or changeset)") describes an artifact;
  users describe an intent.
- **`elicitation` (58%)** misses on "A or B?" — the most compressed form of the
  exact thing it governs.

## The rent (from S1 negatives — turns where TAMOS does nothing)

| condition | $/turn | median latency |
|-----------|--------|----------------|
| baseline  | $0.0904 | 8.1s |
| skills    | $0.0933 | 9.0s |
| hook      | $0.1106 | 8.2s |
| both      | $0.1107 | **12.6s** |

The always-on layer costs **~+22% per turn and ~+4.5s**, charged on *every*
turn including ones with nothing to do with TAMOS. `skills` is nearly free
(+3%) because its cost is only paid when it fires.

This is the guide's own "context is rent" principle billing it: `both` buys +11
recall points over `skills` for +19% cost on every unrelated turn.

## Verdict against the plan's hypotheses

| H | claim | verdict |
|---|-------|---------|
| H1 | hook ≫ baseline on recall, survives loaded context | **hold** (73% vs 34%) |
| H2 | all fixes hold precision ≥90% | **hold** (100% everywhere) |
| H3 | hook ≈ both → drop the skills | **REJECTED** (73% vs 84%) |
| H4 | the doc bug alone explains it | **partial** — baseline 34% is bad but the fix only reaches 84%, so the import bug is necessary-not-sufficient |
| H5 | pairing module helps | not yet run |

## What's still unproven

- Recall is `loaded`, not *good*. No judge has looked at the artifacts (J7's question).
- n=2 per cell. Treat direction as `verified`, magnitude as `believed`.
- Every prompt was written by the same person who wrote the fix.
- Single model, single day.

---

## S5 — the shipped plugin (v0.3.0, commit a5fe27e)

All numbers above came from hand-built `.claude/` mock conditions. This ran the
same suite against the **actually-installed plugin**, nothing local.

| | baseline | shipped plugin |
|---|---|---|
| recall | 13/38 — 34% | **37/38 — 97%** |
| precision | 100% | **100%** (0/16 false fires) |
| rent | $0.0904/turn, 8.1s | $0.1165/turn, 9.4s |

By register: jargon 4/10→10/10, natural 4/12→12/12, **oblique 3/10→10/10**,
embedded 2/6→5/6. By module, everything ≥ 7/8.

The plugin beats the best mock condition (`both`, 84%) because the mock only
carried 4 skills; the plugin ships all 8, which recovered `elicitation`,
`spec-review` and `code-comment`.

### Two packaging defects found only by testing the real install

1. **`hooks/hooks.json` must wrap in a `hooks` key.** The unwrapped
   `{"SessionStart": [...]}` form parses, passes `claude plugin validate --strict`,
   and **silently never executes**. Correct: `{"hooks": {"SessionStart": [...]}}`.
2. **`${CLAUDE_PLUGIN_ROOT}` expands in hook commands but NOT in CLAUDE.md
   `@import`.** This asymmetry is the original bug and its fix in one sentence.

### Correction to J9's headline

J9 concluded "TAMOS routes when you talk like a manual and misses when you talk
like a person," and treated the register gradient as a design boundary. **The
shipped build largely closes it** — oblique went 3/10 → 10/10. The gradient was an
artifact of thin skill coverage and artifact-language descriptions, not an
inherent property of how people speak. Only `embedded` (5/6) still lags.

### Correction to J9's H3

J9 rejected H3 (`hook` ≈ `both`) and the rejection stands, but the margin was
mis-attributed: the gap was mostly **missing skills**, not the hook. With all 8
skills present the plugin reaches 97%. The hook's real job is always-on prose
quality — which this suite never measured.
