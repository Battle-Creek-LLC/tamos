# Tier 1 — Imperative register (human → agent)

Inherits `core.md`. Governs prompts, specs, instructions. Optimize for
constraint and disambiguation.

- Pin the goal and constraints, not the keystrokes.
- Lead and close with the highest-priority constraints; the middle gets the
  least weight. If there are more than two, list them as a numbered block.
- Attach a reason to every prohibition ("don't X; it breaks Y").
- Give one example over a paragraph of description.
- Provide a default and an escape hatch for every branch the agent might hit.
