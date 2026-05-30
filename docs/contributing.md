# Contributing a module

How to add or change a TAMOS module without breaking the cascade.

## Adding a Tier-2 artifact module

1. **Confirm it is a delta.** If your new rules are just core/register rules
   restated, you do not need a module. A module earns its place only by saying
   something *specific* to one kind of output.
2. **Create `artifacts/<name>.md`** using the fixed four-slot shape:
   `APPLIES WHEN`, `RULES`, `SHAPE`, `AVOID`. No other sections.
3. **Write RULES as imperatives only.** No rationale — rationale goes in a
   `docs/` note or a comment in your PR, never in the module. If a rule needs a
   *why* to be followed, the why is a paraphrase risk; bake it into the rule
   ("don't X" → "don't X; it breaks Y").
4. **Never contradict an inherited rule.** If your delta conflicts with the
   register or core, the inherited rule is wrong or this is the wrong home —
   refactor, don't carve out an exception.
5. **Add one row** to the registry table in `AGENT-STYLE.md`.
6. **Bind delivery.** Note in `APPLIES WHEN` the trigger that loads the module,
   and wire it to the producing skill/tool.

## Changing core or a register

Changes here ripple to everything below. Before editing:

- Check that no artifact module silently depends on the rule you are changing.
- Keep the enforced layer dense — if your edit adds rationale, it belongs in
  `docs/principles.md`, not in `core.md`.

## Validation

Run the adversarial agents in `agents/` against your change before merging.
Each attacks one property of the guide:

| Agent                  | Attacks                                          |
|------------------------|--------------------------------------------------|
| `contradiction-hunter` | undeclared conflicts across tiers                |
| `bloat-auditor`        | rationale/filler leaking into the enforced layer |
| `ambiguity-attacker`   | unscoped "all/never", dangling referents, vagueness |
| `cascade-breaker`      | artifact modules that re-litigate inherited rules|
| `dogfood-inspector`    | the guide violating its own rules                |

A module that survives all five is ready to merge.
