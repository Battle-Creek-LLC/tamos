---
description: Run the five TAMOS adversarial validators against the guide and emit a pass/fail verdict.
argument-hint: "[files or globs — defaults to all enforced-layer files]"
---

Run the TAMOS validator suite against the style guide.

## Target

If `$ARGUMENTS` names files or globs, validate those. Otherwise validate the
full enforced layer: `core.md`, `register-imperative.md`,
`register-declarative.md`, `AGENT-STYLE.md`, and `artifacts/*.md`.

## Procedure

Launch all five validators defined in `agents/` against the target, in parallel
where possible. Each is a read-only adversarial check:

1. `contradiction-hunter` — cross-tier conflicts
2. `bloat-auditor` — rationale/filler in the enforced layer
3. `ambiguity-attacker` — unscoped quantifiers, dangling referents, vague terms
4. `cascade-breaker` — artifact modules re-litigating inherited rules; shape violations
5. `dogfood-inspector` — the guide violating its own rules

Collect each validator's findings. A finding at severity **high** or a
**FAIL** verdict from any validator counts as a defect.

## Output

First print a per-validator summary (one line each: validator — verdict —
defect count). Then, as the **final line of your response**, print exactly one
of these machine-readable verdicts so CI can parse it:

- `TAMOS-VALIDATE: PASS` — no defects above the threshold
- `TAMOS-VALIDATE: FAIL` — one or more defects; list them above the verdict line

Do not print anything after the verdict line.
