---
description: Run the five TAMOS adversarial validators against the guide and emit a pass/fail verdict.
argument-hint: "[files or globs — defaults to all enforced-layer files] [--base <ref>]"
---

Run the TAMOS validator suite against the style guide.

## Target

If `$ARGUMENTS` names files or globs, validate those. Otherwise validate the
full enforced layer: `core.md`, `register-imperative.md`,
`register-declarative.md`, `AGENT-STYLE.md`, and `artifacts/*.md`.

## Scope

If `$ARGUMENTS` carries `--base <ref>`, run `git diff --unified=0 <ref>...HEAD`
and keep the changed line ranges. Every finding is then **blocking** or
**advisory**:

- **Blocking** — the finding sits on a line the diff added or changed, OR the
  diff introduced it elsewhere. A finding is diff-introduced when the rule it
  cites as the conflict, duplicate, or source was itself added or changed by
  this diff. Editing `core.md` to duplicate a rule an untouched artifact already
  states is blocking: the diff caused it.
- **Advisory** — everything else. A defect on lines this diff never touched,
  citing no rule this diff changed, pre-dates the PR.

Without `--base`, every finding is blocking; that is the full-layer audit.

Judge blocking-vs-advisory per finding, not per file. A changed file's untouched
lines stay advisory.

## Procedure

Launch all five validators defined in `agents/` against the target, in parallel
where possible. Each is a read-only adversarial check:

1. `contradiction-hunter` — cross-tier conflicts
2. `bloat-auditor` — rationale/filler in the enforced layer
3. `ambiguity-attacker` — unscoped quantifiers, dangling referents, vague terms
4. `cascade-breaker` — artifact modules re-litigating inherited rules; shape violations
5. `dogfood-inspector` — the guide violating its own rules

Collect each validator's findings. A **blocking** finding at severity **high**,
or a validator's **FAIL** verdict resting on a blocking finding, counts as a
defect. Advisory findings never count, whatever their severity.

## Output

First print a per-validator summary (one line each: validator — verdict —
blocking count — advisory count).

Then list the blocking defects. Then list the advisory findings under
`## Pre-existing (advisory)`, so the backlog stays visible without gating the
PR. State the advisory count even when it is zero.

Print exactly one machine-readable verdict as the **final line**, so CI can
parse it:

- `TAMOS-VALIDATE: PASS` — no blocking defects above the threshold
- `TAMOS-VALIDATE: FAIL` — one or more blocking defects; list them above the verdict line

A run with only advisory findings is a `PASS`.

Do not print anything after the verdict line.
