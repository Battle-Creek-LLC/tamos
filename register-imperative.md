# Tier 1 — Imperative register (human → agent)

Inherits `core.md`. Governs prompts, specs, instructions. Optimize for
constraint and disambiguation.

- Pin the goal and constraints, not the keystrokes. Over-specifying procedure
  boxes out better solutions; under-specifying outcome invites drift.
- Put non-negotiables first and last. Middle instructions get the least weight.
- Attach a reason to every prohibition. "Don't X" is weak; "don't X; it breaks
  Y" survives paraphrase.
- Give one example over a paragraph of description.
- Provide a default and an escape hatch for every branch the agent might hit.
- Scope every quantifier. "All/always/never" must name the set it ranges over.
