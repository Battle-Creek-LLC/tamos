# Runtime

The runtime gets the rules into an agent's context as it writes and checks that
it complied — without it, TAMOS is a binder no one opens at the keyboard. The
static structure (tiers, cascade, the four-slot shape) says *what* the rules
are; the runtime says *how* they apply.

## The one decision

> **Per-task style is pull. The always-on layer and enforcement are push.**
> Getting a *specific* artifact's style into context → load on demand (the
> producing skill). Getting the *universal* layer in, and checking that the agent
> followed it → a deterministic hook that fires on the event.

Why split them: per-task provisioning wants to be cheap and quiet, so it loads
only what the current task needs. The always-on layer and enforcement want to be
unskippable, so neither can depend on the agent choosing to run it. A skill that
*enforced* style could be skipped by the agent it's meant to police.

The push half is bounded by *which event*. A hook on every tool call would flood
context, which is why no hook injects per-artifact style. `SessionStart` fires
once per session, so it can carry the few-hundred-token always-on layer without
paying per turn — measured at roughly +$0.03 and +1s per turn, on turns where no
module loads at all.

The earlier version of this doc put the always-on layer under "pull" and asked
the user to `@import` it into CLAUDE.md. That was the wrong call twice over: the
import silently didn't work, and provisioning a *universal* layer was never a
pull problem — nothing about it is task-specific, so there is nothing to decide
on demand.

## What loads where

| Module                      | Mechanism                    | When                          |
|-----------------------------|------------------------------|-------------------------------|
| `core.md`                   | **SessionStart hook**        | always — every turn           |
| `register-declarative.md`   | **SessionStart hook**        | always — every turn produces output |
| `AGENT-STYLE.md` (registry) | **SessionStart hook**        | always — it's the pull map    |
| `register-imperative.md`    | **skill / pull**             | when authoring a prompt or spec |
| `artifacts/*.md`            | **same-named skill**         | when producing that artifact  |
| `agents/*.md` (validators)  | **hook**                     | on commit / pre-merge — as a gate |

### Always-on (SessionStart hook)
Core, the declarative register, and the one-line registry. Together a few
hundred tokens. They are always-on because *every* turn produces output, so the
declarative rules and core invariants always apply, and the registry is how an
agent discovers which artifact module to pull next. Nothing else is always-on.

`hooks/hooks.json` cats the three files at session start; installing the plugin
turns this on. An earlier version asked the user to `@import` them into
`~/.claude/CLAUDE.md` using `${CLAUDE_PLUGIN_ROOT}`. That never worked — the
variable is expanded for hook commands, not for CLAUDE.md imports — so the
always-on layer silently loaded nothing. Measured recall of the wanted artifact
module was 34%; with the hook and the per-module skills it is 97%
(`docs/use-cases.md`).

### Pull / skill-loaded (provisioning)
Artifact modules and the imperative register load only when their work starts.
The producing skill `Read`s its module as step 0 — the `pr-review` skill
opens `artifacts/pr-review.md` before drafting; a commit flow opens
`artifacts/commit-message.md`. Where no skill owns the action, the agent pulls
it itself: consult the registry, match `APPLIES WHEN`, open the module. Cost is
zero until the work happens.

### Hook (enforcement)
The adversarial validators in `agents/` are not provisioning — they are a gate.
Wire them as a hook on the event that finalizes an artifact:

- **Authoring TAMOS itself** (editing `core.md`, a register, an artifact): a
  pre-commit hook runs `contradiction-hunter`, `bloat-auditor`,
  `cascade-breaker`, `dogfood-inspector`, `ambiguity-attacker` against the
  changed files. A defect blocks the commit.
- **Producing an artifact in a real repo**: a `PreToolUse` hook on `git commit`
  can check the message against `commit-message.md`; a PR-review post can be
  checked against `pr-review.md` before it's published.

A hook is right here precisely because it is *not optional* and *fires on the
event*, not on the agent's goodwill.

## `APPLIES WHEN` is the trigger contract

The first slot of every artifact module is its runtime trigger. "APPLIES WHEN:
committing" is the line a skill, hook, or pulling agent reads to decide whether
this module is in scope. The static shape and the runtime meet exactly there:
the shape *declares* the trigger; the runtime *consumes* it.

## Worked example — a commit, end to end

1. Agent finishes a change, goes to commit. (Always-on context already holds
   core + declarative register + registry.)
2. The commit flow (skill or the agent reading the registry) matches
   `APPLIES WHEN: committing` and **pulls** `artifacts/commit-message.md`.
3. Agent writes the message against core + declarative + the commit delta.
4. A pre-commit **hook** checks the message: subject ≤50 chars, imperative
   mood, no attribution trailer, body explains *why*. A violation blocks and
   reports which rule failed.
5. Clean → commit proceeds. The artifact module leaves context; nothing it
   contributed pays rent on the next turn.

Provisioning got the rules in at step 2; enforcement kept them honest at step 4;
neither did the other's job.
