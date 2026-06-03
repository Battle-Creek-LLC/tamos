# Artifact — elicitation

Inherits `register-declarative.md`.

APPLIES WHEN:  soliciting a decision from a human (`/spec.questions`, an ambiguous
requirement, any "pick A or B").

RULES:
- Emit one block per decision — separate blocks when several are pending.
- The recommendation is the answer — lead with it, tagged with its certainty (`verified` / `believed` / `guessed`).
- Options as a table, `Option | Gives up`, one row each.
- Research only enough to fill the `Gives up` column with a real trade-off.
- Name what the decision blocks downstream (ids / phases).
- End with a one-line `Ask:` only when no picker follows; a picker poses the choice, so omit it then — never the recommendation or table.

SHAPE:
```
### Q1 — Per-firm configurable hub links, or one hardcoded set?
**Recommend:** firm-configurable — each tool is one optional URL, no special-casing. [believed]
**Blocks:** hub coherence (which links render)

| Option | Gives up |
|---|---|
| Firm-configurable list | a curated native integration — it's just a link |
| Hardcoded fixed set | dead links for firms that don't use a listed tool |
```

AVOID:
- A `Gives up` cell that lists features instead of what the option forgoes.
- Repeating the choice in prose when a picker already poses it.
