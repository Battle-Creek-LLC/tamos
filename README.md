# TAMOS — The Agent Manual of Style

A style guide for prose written **to** agents and **by** agents.

Chicago tells one writer how to address one reader. TAMOS governs two
directions at once: how humans write *to* agents (prompts, specs,
instructions) and how agents write *back* (reviews, reports, commits, docs).
Those are different registers with different failure modes, and most bad
"agent writing" comes from conflating them.

## How TAMOS is organized

A **cascade**. General rules at the top; specialized overrides below; the
more specific rule wins on conflict.

```
Tier 0 — CORE          universal invariants, both directions   → core.md
Tier 1 — REGISTERS     imperative (to agents) / declarative (from agents)
Tier 2 — ARTIFACTS     per-output deltas (PR review, commit, report…)
```

A Tier-2 module states only its *delta* over the register it inherits. The
PR-review module does not re-explain how to cite or hedge — it says only what
is special about a PR review. ("Style" names the discipline as a whole; a
single unit is always a "module".)

## Two layers, by token cost

| Layer        | Lives in            | Loaded        | Style                       |
|--------------|---------------------|---------------|-----------------------------|
| **Enforced** | CLAUDE.md / prompt  | every turn    | terse imperatives, no *why* |
| **Reference**| this repo           | on demand     | prose, rationale, examples  |

Rationale never goes in the enforced layer. The *why* is for the human
maintaining the guide and lives in `docs/`.

## Install

TAMOS ships as a Claude Code plugin (the repo is its own marketplace):

```
/plugin marketplace add Battle-Creek-LLC/tamos
/plugin install tamos@battle-creek
```

Then opt the always-on layer into your global `~/.claude/CLAUDE.md` by import.
Full steps, CI/CD, and release flow are in `docs/user-guide.md`.

## Start here

- `docs/principles.md` — the philosophy (two registers, token economy, dogfooding)
- `docs/structure.md` — the tier cascade, the fixed artifact shape, delivery
- `docs/runtime.md` — how modules load (pull/skill) and get enforced (hook)
- `docs/user-guide.md` — install, always-on import, validation, CI/CD, releases
- `docs/contributing.md` — how to add a new artifact module
- `AGENT-STYLE.md` — the index/registry of every module
- `docs/use-cases.md` — what each module governs and the words that engage it
- `agents/` — adversarial validators that attack this guide for defects
