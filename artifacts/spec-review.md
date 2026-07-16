# Artifact — Spec review

Inherits `register-declarative.md`.

APPLIES WHEN:  producing a requirements-quality review of a specification (an `sp`
spec, an SRS/design-doc markdown file, or the spec-shaped changes in a diff).

RULES:
- Open with the spec id and title; close nothing else onto that line.
- Surface findings you can state as `verified` or `believed`; drop anything you
  would tag `guessed`. State what you checked and what you dropped.
- One finding per defect. Cite the spec section (`§"<heading>"`) it occurred in.
- Tag each finding with its lens AND the rule it breaks: a 29148 characteristic
  (`unambiguous`, `complete`, `consistent`, `verifiable`, `feasible`, `traceable`, …)
  or a named TAMOS rule (`specificity`, `communicate through structure`, …).
- Quote the offending spec text before critiquing it.
- Propose a concrete rewrite, not just the problem. A rewrite you suggest MUST itself
  conform to TAMOS.
- For a conflict finding, name the real accepted artifact it contradicts and confirm
  that artifact's text actually says so — an unverified conflict is a guess, mark it.
- Order findings by confidence, highest first. No emojis.

SHAPE:
```
### Spec review — s-<id> "<title>"

Found <n> issues:

1. [<Lens>] §"<section>" — <one-line defect>. Suggest: <rewrite>. (29148: <characteristic>)
   > <offending spec text quoted>

2. [Conflict] §"<section>" — contradicts <artifact-id> (accepted): <what it says>.
   Propose an amend/supersede before activating. (29148: conforming) [verified]

3. [Style/TAMOS] §"<section>" — <defect>. Suggest: <rewrite>. (TAMOS: <rule>)
```

Clean pass:
```
### Spec review — s-<id> "<title>"

No issues found. Checked ambiguity, completeness, consistency against accepted
artifacts, testability, design-leakage, feasibility, traceability, and TAMOS style.
```

AVOID:
- Inventing the missing requirement — report a completeness gap as a gap.
- Judging implementation code; a spec review never reads or rates the build.
- Flagging prose-polish or formatting nits that cause no ambiguity.
- Re-flagging unchanged sections, or detail explicitly deferred out of scope.
