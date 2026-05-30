# Structure

How TAMOS is assembled. Reference-layer prose.

## The three tiers

```
Tier 0 — CORE          always-on, tiny, universal invariants
            │ inherits  (applies to every agent, both directions)
Tier 1 — REGISTERS     imperative (human→agent) · declarative (agent→human)
            │ inherits
Tier 2 — ARTIFACTS     per-output deltas: pr-review, commit-message,
                       research-report, status-update, code-comment …
```

Each tier is narrower and longer-lived than the one below it. Core changes
rarely and touches everything. An artifact module changes often and touches
one kind of output.

## The cascade

A module **inherits** every rule above it and states only its **delta**. This
is what keeps the always-on footprint tiny while still giving a precise answer
for any specific task: the PR-review module is ~15 lines because it does not
re-litigate citation or hedging — it inherits those.

Conflict resolution: the more specific module wins, **but the override is
explicit**. A Tier-2 rule that contradicts its register must carry
`OVERRIDES: <the inherited rule>`. A silent contradiction is a defect — the
`contradiction-hunter` agent hunts for exactly these.

## Delivery binding

A tier is only worth its design if it loads at the right moment. Each tier
binds to a delivery mechanism:

| Tier      | Delivery                                   | Cost            |
|-----------|--------------------------------------------|-----------------|
| Core      | inlined into CLAUDE.md / system prompt     | every turn      |
| Registers | loaded with the broad activity, or in core | per activity    |
| Artifacts | loaded by the skill/tool that produces them| zero until used |

The PR-review style attaches to the review skill; the commit-message style
loads when committing. Style is enforced by being *read at the right moment*,
not by existing.

## The fixed artifact shape

Every Tier-2 module has the same four slots so they are predictable to write
and to read:

```
APPLIES WHEN:  the trigger that should cause this module to load
RULES:         imperatives only — the delta over the register
SHAPE:         one skeleton/example of the finished artifact
AVOID:         the 2–3 anti-patterns specific to this artifact
```

`SHAPE` matters most: one concrete skeleton constrains more than a paragraph
of description. Show, don't tell.

## The index

`AGENT-STYLE.md` is the registry — one row per module — and the only Tier-2
artifact that is ever always-on. It is how an agent discovers which module to
load for the task in front of it.
