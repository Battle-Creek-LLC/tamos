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
  same finding fails to hold against `<ref>`. Test the second case: read the
  rule the finding cites as `<ref>` has it, and ask whether the finding still
  stands. A finding that still stands pre-dates the PR.
- **Advisory** — everything else, including a finding that cites a rule this
  diff changed but holds against `<ref>` just as well.

Run the `<ref>` test on every finding outside a changed line. Editing a register
puts all nine modules in citing range, and most of what surfaces there is the
layer's standing backlog: a module that conflicts only with the new wording is
blocking, a module that conflicted with the old wording too is advisory.

Without `--base`, every finding is blocking; that is the full-layer audit.

Judge blocking-vs-advisory per finding, not per file. A changed file's untouched
lines stay advisory.

## Severity

Rate each finding by what it does to the artifact its rule governs:

- **high** — an agent following the rule emits a materially wrong artifact, or
  two rules leave a required slot unsatisfiable. Name the wrong output.
- **medium** — the rule admits two readings that change the artifact's shape,
  and a competent agent could land on either.
- **low** — wording, naming, wrapping, or a count. The artifact comes out the
  same.

If you cannot name the wrong output a finding produces, it is not high.

## Procedure

Launch all five validators defined in `agents/` against the target, in parallel
where possible. Each is a read-only adversarial check:

1. `contradiction-hunter` — cross-tier conflicts
2. `bloat-auditor` — rationale/filler in the enforced layer
3. `ambiguity-attacker` — unscoped quantifiers, dangling referents, vague terms
4. `cascade-breaker` — artifact modules re-litigating inherited rules; shape violations
5. `dogfood-inspector` — the guide violating its own rules

Collect each validator's findings. A defect is a **blocking** finding at
severity **high**. Nothing else counts — not a blocking finding at medium or
low, not an advisory finding at any severity, and not a validator's own verdict
line. Each validator returns FAIL whenever it finds anything at all; the verdict
below is yours to compute from the findings.

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
