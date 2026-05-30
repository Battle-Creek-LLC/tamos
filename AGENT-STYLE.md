# AGENT-STYLE — index & cascade rule

This file is the only Tier-2 map that is ever always-on. It lists every
module and the one rule that binds them.

## The cascade rule

> A module inherits every rule from the tier above it. A module states only
> its **delta** — what differs from what it inherits. On conflict, the more
> specific module wins, **and it must say so explicitly** (`OVERRIDES: <rule>`).
> A silent contradiction is a bug, not an override.

## Registry

| Tier | Module                       | Governs                                   | Loaded when                     |
|------|------------------------------|-------------------------------------------|---------------------------------|
| 0    | `core.md`                    | all agent prose, both directions          | always (inline into CLAUDE.md)  |
| 1    | `register-imperative.md`     | writing **to** agents (prompts, specs)    | authoring instructions          |
| 1    | `register-declarative.md`    | writing **from** agents (any output)      | producing output                |
| 2    | `artifacts/pr-review.md`     | code review output                        | reviewing a PR                  |
| 2    | `artifacts/commit-message.md`| commit subjects & bodies                  | committing                      |
| 2    | `artifacts/research-report.md`| multi-source findings reports            | producing research              |
| 2    | `artifacts/status-update.md` | progress / handoff updates                | reporting status                |
| 2    | `artifacts/code-comment.md`  | inline code comments                      | writing code                    |

## The fixed artifact shape

Every Tier-2 module has exactly these four slots, in this order:

```
APPLIES WHEN:  trigger — so the agent knows to load this module
RULES:         imperatives only; the delta over the register
SHAPE:         one skeleton of the finished artifact
AVOID:         the 2–3 anti-patterns specific to this artifact
```

## Adding a module

See `docs/contributing.md`. New row here, new file under `artifacts/`,
nothing more.
