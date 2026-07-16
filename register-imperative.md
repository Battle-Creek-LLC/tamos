# Tier 1 — Imperative register (human → agent)

Inherits `core.md`. Governs prompts, specs, instructions. Optimize for
constraint and disambiguation.

- Pin the goal and constraints, not the keystrokes.
- Lead and close with the highest-priority constraints. When the prompt carries
  more than two constraints of any priority, list every constraint as a numbered
  block so none is buried in the middle.
- Attach a reason to every prohibition ("don't X; it breaks Y").
- Provide a default and an escape hatch for every branch the agent might hit.
